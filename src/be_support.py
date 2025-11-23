"""
Belarusian Language Support Module
Provides lemmatization and stop words for Belarusian text
"""

import streamlit as st
from lemmatizer_be import BnkorpusLemmatizer  # noqa: E402


@st.cache_resource
def get_belarusian_analyzer():
    """Initialize and cache the Belarusian lemmatizer"""
    return BnkorpusLemmatizer()


def lemmatize_belarusian(words):
    """
    Lemmatize Belarusian words using lemmatizer_be
    
    Args:
        words: List of words to lemmatize
        
    Returns:
        List of lemmas
    """
    lemmatizer = get_belarusian_analyzer()
    lemmas = []
    for word in words:
        # Get the lemma for Belarusian
        lemma = lemmatizer.lemmatize(word)
        lemmas.append(lemma)
    return lemmas


def get_belarusian_stop_words():
    """
    Returns a set of common Belarusian stop words
    (prepositions, conjunctions, particles, pronouns)
    """
    return {
        # Prepositions (прыназоўнікі)
        'у', 'ў', 'на', 'з', 'да', 'па', 'пра', 'для', 'з-за', 'з-пад', 'праз',
        'над', 'пад', 'перад', 'каля', 'ля', 'пасля', 'без', 'ад', 'за', 'аб',
        'пры', 'між', 'сярод', 'ля', 'праз',
        
        # Conjunctions (злучнікі)
        'і', 'й', 'а', 'але', 'ці', 'альбо', 'што', 'каб', 'калі', 'як', 'хаця',
        'таму', 'бо', 'таксама', 'жа',
        
        # Particles (часціцы)
        'не', 'ні', 'б', 'бы', 'ж', 'жа', 'ці', 'вось', 'ажно', 'нават', 'толькі',
        'хоць', 'ледзь', 'амаль',
        
        # Pronouns (займеннікі)
        'я', 'ты', 'ён', 'яна', 'яно', 'мы', 'вы', 'яны', 'мой', 'твой', 'свой',
        'наш', 'ваш', 'яго', 'яе', 'іх', 'гэты', 'той', 'такі', 'увесь',
        'сам', 'самы', 'які', 'чый', 'хто', 'што', 'гэта',
        
        # Common verbs and words
        'быць', 'усё', 'ўсё', 'яшчэ', 'ужо', 'там', 'тут', 'дзе', 'куды',
        'тады', 'потым', 'цяпер', 'вельмі', 'больш', 'так', 'ды', 'не'
    }

