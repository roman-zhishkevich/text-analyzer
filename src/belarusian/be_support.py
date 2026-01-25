"""
Belarusian Language Support Module
Provides lemmatization and stop words for Belarusian text

Supports two modes:
1. Basic mode: lemmatizer_be only (default, always works)
2. Enhanced mode: GrammarDB + lemmatizer_be (faster, more accurate)
"""

import streamlit as st
import os
from lemmatizer_be import BnkorpusLemmatizer  # noqa: E402

# Auto-download GrammarDB if not present (for Streamlit Cloud)
try:
    from .auto_download import ensure_grammardb_ready
    # This runs once on module import (first app startup)
    ensure_grammardb_ready()
except Exception as e:
    print(f"⚠️ Auto-download skipped: {e}")

# Try to import enhanced lemmatizer (optional)
try:
    from .be_lemmatizer_enhanced import get_enhanced_lemmatizer
    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False


# Configuration: Enable enhanced mode if GrammarDB is available
GRAMMARDB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "grammardb.json")
USE_ENHANCED = ENHANCED_AVAILABLE and os.path.exists(GRAMMARDB_PATH)


@st.cache_resource
def get_belarusian_analyzer():
    """
    Initialize and cache the Belarusian lemmatizer
    
    Returns:
        BnkorpusLemmatizer or EnhancedBelarusianLemmatizer based on availability
    """
    if USE_ENHANCED:
        print("✅ Using Enhanced Belarusian Lemmatizer (GrammarDB + lemmatizer_be)")
        return get_enhanced_lemmatizer(GRAMMARDB_PATH)
    else:
        print("📝 Using Basic Belarusian Lemmatizer (lemmatizer_be only)")
        return BnkorpusLemmatizer()


def lemmatize_belarusian(words):
    """
    Lemmatize Belarusian words
    
    Automatically uses enhanced lemmatizer if GrammarDB is available,
    otherwise falls back to basic lemmatizer_be
    
    Args:
        words: List of words to lemmatize
        
    Returns:
        List of lemmas
    """
    analyzer = get_belarusian_analyzer()
    lemmas = []
    
    for word in words:
        # Get the lemma (both basic and enhanced have .lemmatize() method)
        lemma = analyzer.lemmatize(word)
        lemmas.append(lemma)
    
    return lemmas


def get_lemmatizer_info():
    """
    Get information about current lemmatizer configuration
    
    Returns:
        dict: Configuration info
    """
    return {
        'mode': 'enhanced' if USE_ENHANCED else 'basic',
        'enhanced_available': ENHANCED_AVAILABLE,
        'grammardb_path': GRAMMARDB_PATH if USE_ENHANCED else None,
        'grammardb_exists': os.path.exists(GRAMMARDB_PATH)
    }


def get_belarusian_stop_words():
    """
    Returns a set of common Belarusian stop words
    (prepositions, conjunctions, particles, pronouns)
    
    Note: Includes both Cyrillic and Latin variants of lookalike letters
    to handle mixed-alphabet texts and keyboard layout typos
    """
    return {
        # Prepositions (прыназоўнікі)
        'у', 'y', 'ў', 'на', 'з', 'да', 'па', 'пра', 'для', 'з-за', 'з-пад', 'праз',
        'над', 'пад', 'перад', 'каля', 'ля', 'пасля', 'без', 'ад', 'за', 'аб',
        'пры', 'між', 'сярод', 'ля', 'праз',
        
        # Conjunctions (злучнікі)
        'і', 'i', 'й', 'а', 'a', 'але', 'ці', 'ci', 'альбо', 'што', 'каб', 'калі', 'як', 'хаця',
        'таму', 'бо', 'таксама', 'жа',
        
        # Particles (часціцы)
        'не', 'ne', 'ні', 'б', 'бы', 'ж', 'жа', 'ці', 'ci', 'вось', 'ажно', 'нават', 'толькі',
        'хоць', 'ледзь', 'амаль',
        
        # Pronouns (займеннікі)
        'я', 'ты', 'ён', 'яна', 'яно', 'мы', 'вы', 'яны', 'мой', 'твой', 'свой',
        'наш', 'ваш', 'яго', 'яе', 'іх', 'ix', 'гэты', 'той', 'такі', 'увесь',
        'сам', 'самы', 'які', 'чый', 'хто', 'што', 'гэта',
        
        # Common verbs and words
        'быць', 'усё', 'ўсё', 'яшчэ', 'ужо', 'там', 'тут', 'дзе', 'куды',
        'тады', 'потым', 'цяпер', 'вельмі', 'больш', 'так', 'ды', 'не', 'ne'
    }

