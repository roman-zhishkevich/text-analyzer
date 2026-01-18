"""
Stop Words Manager UI
Provides interface for viewing and managing stop words
"""

import streamlit as st
from ru_support import get_russian_stop_words
from be_support import get_belarusian_stop_words


def render_stop_words_ui(lang_code="ru"):
    """
    Render the stop words management UI
    
    Args:
        lang_code: Language code ('ru' or 'be')
        
    Returns:
        set: Combined set of default and custom stop words
    """
    # Initialize session state for custom stop words
    if 'custom_stop_words' not in st.session_state:
        st.session_state.custom_stop_words = set()
    
    # Get default stop words based on language
    if lang_code == "ru":
        default_stop_words = get_russian_stop_words()
    else:
        default_stop_words = get_belarusian_stop_words()
    
    # Combine default and custom
    current_stop_words = default_stop_words | st.session_state.custom_stop_words
    
    # Stop words editor section
    with st.expander("⚙️ Управление стоп-словами", expanded=False):
        # Display statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Стандартных", len(default_stop_words))
        with col2:
            st.metric("Добавлено", len(st.session_state.custom_stop_words))
        with col3:
            st.metric("Всего", len(current_stop_words))
        
        st.markdown("---")
        
        # Add new stop words
        st.subheader("➕ Добавить стоп-слова")
        col_add1, col_add2 = st.columns([3, 1])
        with col_add1:
            new_words_input = st.text_input(
                "Введите слова через запятую:",
                placeholder="например, шесть, семь, восемь",
                key="new_stop_words_input"
            )
        with col_add2:
            if st.button("Добавить", type="primary"):
                if new_words_input:
                    new_words = [w.strip().lower() for w in new_words_input.split(',') if w.strip()]
                    st.session_state.custom_stop_words.update(new_words)
                    st.success(f"✅ Добавлено {len(new_words)} слов(а)")
                    st.rerun()
        
        # Remove custom stop words
        if st.session_state.custom_stop_words:
            st.subheader("➖ Удалить добавленные слова")
            words_to_remove = st.multiselect(
                "Выберите слова для удаления:",
                sorted(st.session_state.custom_stop_words),
                key="words_to_remove"
            )
            col_rem1, col_rem2 = st.columns([3, 1])
            with col_rem2:
                if st.button("Удалить выбранные"):
                    for word in words_to_remove:
                        st.session_state.custom_stop_words.discard(word)
                    st.success(f"✅ Удалено {len(words_to_remove)} слов(а)")
                    st.rerun()
        
        # Reset button
        st.markdown("---")
        if st.button("🔄 Сбросить к стандартным"):
            st.session_state.custom_stop_words = set()
            st.success("✅ Сброшено к стандартным стоп-словам")
            st.rerun()
        
        # Display current stop words (sorted)
        st.subheader("📋 Текущие стоп-слова")
        st.caption(f"Всего: {len(current_stop_words)} слов")
        
        # Display in columns for better readability
        sorted_words = sorted(current_stop_words)
        words_per_column = 15
        num_columns = (len(sorted_words) + words_per_column - 1) // words_per_column
        
        cols = st.columns(num_columns)
        for i, word in enumerate(sorted_words):
            col_idx = i // words_per_column
            with cols[col_idx]:
                # Mark custom words with a badge
                if word in st.session_state.custom_stop_words:
                    st.markdown(f"🟢 {word}")
                else:
                    st.text(word)
    
    # Return combined stop words for use in analysis
    return current_stop_words

