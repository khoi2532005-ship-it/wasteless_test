from django.shortcuts import render
from wagtail.models import Page
from .models import ArticlePage
from .search_ai import search_ai
from django.core.cache import cache
from concurrent.futures import ThreadPoolExecutor


def ai_powered_search(request):
    """
    Smart search with Vietnamese AI support using Wagtail's built-in search.
    Handles abbreviations like "cf" -> "cà phê"
    Optimized with caching, limits, and parallel processing.
    """
    query_string = request.GET.get('query', '').strip()
    
    context = {
        'query': query_string,
        'results': [],
        'suggestions': [],
        'did_you_mean': None,
        'search_terms': [],
        'total_results': 0,
    }
    
    if not query_string:
        return render(request, 'website/search_results.html', context)
    
    # Cache candidates for 1 hour
    candidates = cache.get('search_candidates')
    if candidates is None:
        candidates = []
        
        # Get titles from existing articles
        article_titles = list(ArticlePage.objects.live().values_list('title', flat=True))
        candidates.extend(article_titles)
        
        # Add common Vietnamese food/drink terms
        common_terms = [
            'cà phê', 'cafe', 'coffee', 'cà phê đen', 'cà phê sữa',
            'trà', 'trà sữa', 'milk tea', 'trà đào',
            'bánh mì', 'bánh mì thịt', 'sandwich',
            'cơm', 'cơm tấm', 'cơm chiên',
            'phở', 'phở bò', 'phở gà',
            'bún', 'bún bò', 'bún chả',
            'nước', 'nước ngọt', 'soda',
            'kem', 'ice cream',
        ]
        candidates.extend(common_terms)
        candidates = list(set(candidates))
        cache.set('search_candidates', candidates, 3600)
    
    # Run AI operations in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_suggestions = executor.submit(
            search_ai.find_similar, 
            query_string, candidates, 3, 0.4  # Reduced from 5 to 3
        )
        future_expanded = executor.submit(
            search_ai.expand_search_query,
            query_string, candidates, 3
        )
        
        ai_suggestions = future_suggestions.result()
        expanded_terms = future_expanded.result()
    
    # Use Wagtail's built-in search with limits
    results = []
    seen_ids = set()
    
    for term in expanded_terms:
        pages = Page.objects.live().public().search(term)[:20]  # Limit per term
        
        for page in pages:
            if page.id not in seen_ids:
                results.append(page.specific)
                seen_ids.add(page.id)
            
            if len(results) >= 30:  # Max 30 results
                break
        
        if len(results) >= 30:
            break
    
    # Determine "did you mean" suggestion
    show_suggestion = (
        len(results) == 0 or 
        (len(query_string) < 3 and len(ai_suggestions) > 0)
    )
    
    did_you_mean = None
    if show_suggestion and ai_suggestions:
        best = ai_suggestions[0]
        if best['term'].lower() != query_string.lower() and best['score'] > 0.4:  # Increased threshold
            did_you_mean = best['term']
    
    context.update({
        'results': results,
        'suggestions': ai_suggestions,
        'did_you_mean': did_you_mean,
        'search_terms': expanded_terms,
        'total_results': len(results),
    })
    
    return render(request, 'website/search_results.html', context)
