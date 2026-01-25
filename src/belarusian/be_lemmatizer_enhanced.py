"""
Enhanced Belarusian Lemmatizer
Combines GrammarDB (fast dictionary lookup) with lemmatizer_be (smart analysis)
Optimized for speed and accuracy
"""

from lemmatizer_be import BnkorpusLemmatizer
from .grammardb_handler import get_grammardb_handler


class EnhancedBelarusianLemmatizer:
    """
    Enhanced Belarusian lemmatizer using two-stage approach:
    1. GrammarDB lookup (fast, accurate for known words)
    2. lemmatizer_be fallback (handles unknown/new words)
    """
    
    def __init__(self, grammardb_path=None):
        """
        Initialize enhanced lemmatizer
        
        Args:
            grammardb_path: Optional path to GrammarDB data file
        """
        # Stage 1: GrammarDB handler (fast dictionary lookup)
        self.grammardb = get_grammardb_handler(grammardb_path)
        
        # Stage 2: lemmatizer_be (smart morphological analysis)
        self.lemmatizer_be = BnkorpusLemmatizer()
        
        # Statistics tracking
        self.stats = {
            'total_words': 0,
            'grammardb_hits': 0,
            'lemmatizer_be_fallbacks': 0
        }
    
    def lemmatize(self, word):
        """
        Lemmatize a single word using optimized two-stage approach
        
        Args:
            word: Word to lemmatize
            
        Returns:
            str: Lemmatized form (base form)
        """
        self.stats['total_words'] += 1
        
        # Stage 1: Try GrammarDB first (fast path - microseconds)
        lemma = self.grammardb.lookup(word)
        
        if lemma is not None:
            self.stats['grammardb_hits'] += 1
            return lemma
        
        # Stage 2: Fallback to lemmatizer_be (slow path - milliseconds)
        self.stats['lemmatizer_be_fallbacks'] += 1
        lemma = self.lemmatizer_be.lemmatize(word)
        
        return lemma
    
    def lemmatize_batch(self, words):
        """
        Lemmatize multiple words efficiently
        
        Args:
            words: List of words to lemmatize
            
        Returns:
            list: List of lemmatized forms
        """
        return [self.lemmatize(word) for word in words]
    
    def validate_lemma(self, word, lemma):
        """
        Validate if a lemma is correct by checking GrammarDB
        
        Args:
            word: Original word
            lemma: Proposed lemma
            
        Returns:
            bool: True if lemma is validated, False otherwise
        """
        return self.grammardb.is_in_dictionary(lemma)
    
    def get_performance_stats(self):
        """
        Get performance statistics
        
        Returns:
            dict: Statistics including hit rate and performance metrics
        """
        total = self.stats['total_words']
        
        if total == 0:
            return {
                'total_words': 0,
                'grammardb_hit_rate': 0,
                'performance': 'No words processed'
            }
        
        hit_rate = (self.stats['grammardb_hits'] / total) * 100
        fallback_rate = (self.stats['lemmatizer_be_fallbacks'] / total) * 100
        
        return {
            'total_words': total,
            'grammardb_hits': self.stats['grammardb_hits'],
            'lemmatizer_be_fallbacks': self.stats['lemmatizer_be_fallbacks'],
            'grammardb_hit_rate': f"{hit_rate:.1f}%",
            'fallback_rate': f"{fallback_rate:.1f}%",
            'grammardb_loaded': self.grammardb.loaded,
            'grammardb_size': len(self.grammardb.word_to_lemma) if self.grammardb.loaded else 0
        }
    
    def reset_stats(self):
        """Reset statistics counters"""
        self.stats = {
            'total_words': 0,
            'grammardb_hits': 0,
            'lemmatizer_be_fallbacks': 0
        }


# Singleton instance for caching
_enhanced_lemmatizer_instance = None


def get_enhanced_lemmatizer(grammardb_path=None):
    """
    Get or create enhanced lemmatizer instance (singleton pattern)
    
    Args:
        grammardb_path: Optional path to GrammarDB data file
        
    Returns:
        EnhancedBelarusianLemmatizer: Enhanced lemmatizer instance
    """
    global _enhanced_lemmatizer_instance
    
    if _enhanced_lemmatizer_instance is None:
        _enhanced_lemmatizer_instance = EnhancedBelarusianLemmatizer(grammardb_path)
    
    return _enhanced_lemmatizer_instance

