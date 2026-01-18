"""
Russian Language Support Module
Provides lemmatization and stop words for Russian text
"""

import streamlit as st
import pymorphy3


@st.cache_resource
def get_russian_analyzer():
    """Initialize and cache the pymorphy3 analyzer for Russian"""
    return pymorphy3.MorphAnalyzer()


def lemmatize_russian(words):
    """
    Lemmatize Russian words using pymorphy3
    
    Args:
        words: List of words to lemmatize
        
    Returns:
        List of lemmas
    """
    morph = get_russian_analyzer()
    lemmas = []
    for word in words:
        # Parse the word and get the normal form (lemma)
        parsed = morph.parse(word)[0]
        lemma = parsed.normal_form
        lemmas.append(lemma)
    return lemmas


def get_russian_stop_words():
    """
    Returns a set of common Russian stop words
    (prepositions, conjunctions, particles, pronouns, numerals)
    """
    return {
        # Prepositions (предлоги)
        'в', 'на', 'с', 'к', 'по', 'о', 'у', 'из', 'за', 'от', 'до', 'для',
        'при', 'через', 'над', 'под', 'об', 'про', 'без', 'около', 'перед',
        'между', 'среди', 'вокруг', 'после', 'кроме',
        
        # Conjunctions (союзы)
        'и', 'а', 'но', 'или', 'что', 'как', 'если', 'когда', 'чтобы', 'хотя',
        'потому', 'так', 'тоже', 'также', 'либо', 'зато', 'однако', 'же',
        
        # Particles (частицы)
        'не', 'ни', 'бы', 'ли', 'же', 'ведь', 'уж', 'вот', 'даже', 'лишь',
        'только', 'почти', 'ну', 'то', 'нибудь',
        
        # Pronouns (местоимения)
        'я', 'ты', 'он', 'она', 'оно', 'мы', 'вы', 'они', 'мой', 'твой', 'свой',
        'наш', 'ваш', 'его', 'её', 'их', 'этот', 'тот', 'такой', 'весь',
        'сам', 'самый', 'который', 'какой', 'чей', 'кто', 'что',
        
        # Common verbs (вспомогательные глаголы)
        'быть', 'это', 'весь', 'себя', 'свой', 'мочь',
        
        # Numerals (числительные)
        'один', 'два', 'три', 'четыре', 'пять', 'раз',
        
        # Other common words
        'да', 'нет', 'вс', 'всё', 'ещё', 'уже', 'там', 'тут', 'где', 'куда',
        'здесь', 'тогда', 'потом', 'теперь', 'очень', 'более', 'самый'
    }

