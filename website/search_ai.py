"""
Local AI-powered search with Vietnamese language support using MiniLM.
"""

from sentence_transformers import SentenceTransformer, util
from typing import Optional, List, Dict

# Manual abbreviation mappings for common short forms
MANUAL_ABBREVIATIONS = {
    'cf': ['cà phê', 'cafe', 'coffee'],
    'ts': ['trà sữa', 'milk tea'],
    'bmì': ['bánh mì'],
    'bm': ['bánh mì'],
    'ct': ['cơm tấm'],
    'com': ['cơm'],
}


class LocalSearchAI:
    """Singleton class for local AI search."""
    
    _instance: Optional['LocalSearchAI'] = None
    _model: Optional[SentenceTransformer] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._model is None:
            print("Loading AI model ...")
            self._model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            print("Model loaded successfully!")
    
    @property
    def model(self) -> SentenceTransformer:
        """Ensure model is always available."""
        if self._model is None:
            self.__init__()
        return self._model  # type: ignore
    
    def find_similar(
        self, 
        query: str, 
        candidates: List[str], 
        top_k: int = 5, 
        threshold: float = 0.35
    ) -> List[Dict[str, any]]:
        """
        Find semantically similar terms using AI.
        """
        if not query or not candidates:
            return []
        
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        candidate_embeddings = self.model.encode(candidates, convert_to_tensor=True)
        
        similarities = util.cos_sim(query_embedding, candidate_embeddings)[0]
        
        results = []
        for idx, score in enumerate(similarities):
            score_value = float(score)
            if score_value > threshold:
                results.append({
                    'term': candidates[idx],
                    'score': score_value
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def expand_search_query(
        self, 
        query: str, 
        candidates: List[str], 
        max_terms: int = 3
    ) -> List[str]:
        """
        Expand search query with AI suggestions + manual abbreviations.
        """
        query_lower = query.lower().strip()
        
        # Check manual abbreviations first
        if query_lower in MANUAL_ABBREVIATIONS:
            expanded = [query] + MANUAL_ABBREVIATIONS[query_lower]
            return expanded[:max_terms + 1]
        
        # Otherwise use AI
        similar = self.find_similar(query, candidates, top_k=max_terms)
        expanded = [query] + [s['term'] for s in similar]
        
        # Remove duplicates
        seen = set()
        result = []
        for term in expanded:
            term_lower = term.lower()
            if term_lower not in seen:
                seen.add(term_lower)
                result.append(term)
        
        return result


# Global instance
search_ai = LocalSearchAI()
