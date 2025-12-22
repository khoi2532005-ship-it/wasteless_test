from django.shortcuts import render
from wagtail.models import Page
from wagtail.search.backends import get_search_backend
from .models import ArticlePage
from .search_ai import search_ai


def ai_powered_search(request):
    """
    Smart search with Vietnamese AI support using Wagtail's built-in search.
    Handles abbreviations like "cf" -> "cà phê"
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
    
    # Build candidate terms from your content
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
    
    # Remove duplicates
    candidates = list(set(candidates))
    
    # Get AI suggestions
    ai_suggestions = search_ai.find_similar(query_string, candidates, top_k=5, threshold=0.35)
    
    # Expand search terms (includes manual abbreviations + AI)
    expanded_terms = search_ai.expand_search_query(query_string, candidates, max_terms=3)
    
    # Use Wagtail's built-in search
    results = []
    seen_ids = set()
    
    # Search using all expanded terms
    for term in expanded_terms:
        pages = Page.objects.live().public().search(term)
        
        # Add results without duplicates
        for page in pages:
            if page.id not in seen_ids:
                results.append(page.specific)
                seen_ids.add(page.id)
    
    # Determine "did you mean" suggestion
    show_suggestion = (
        len(results) == 0 or 
        (len(query_string) < 3 and len(ai_suggestions) > 0)
    )
    
    did_you_mean = None
    if show_suggestion and ai_suggestions:
        best = ai_suggestions[0]
        if best['term'].lower() != query_string.lower() and best['score'] > 0.35:
            did_you_mean = best['term']
    
    context.update({
        'results': results,
        'suggestions': ai_suggestions,
        'did_you_mean': did_you_mean,
        'search_terms': expanded_terms,
        'total_results': len(results),
    })
    
    return render(request, 'website/search_results.html', context)
