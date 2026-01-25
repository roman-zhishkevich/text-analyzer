"""
Text Analyzer - Streamlit App
Supports .txt, .pdf, and .docx files
Performs tokenization and lemmatization for Russian and Belarusian languages
Uses pymorphy3 (Russian) and lemmatizer_be (Belarusian)
"""

# Core Streamlit and data processing imports
import streamlit as st
from collections import Counter
import re
import io
import csv

# Language support modules
from ru_support import lemmatize_russian, get_russian_stop_words
from belarusian.be_support import lemmatize_belarusian, get_belarusian_stop_words
from stop_words_manager import render_stop_words_ui
from text_input_handler import render_text_input_ui


def tokenize_text(text):
    """
    Tokenize text into words
    Removes punctuation and keeps only Cyrillic and Latin letters
    
    Args:
        text: Raw text string to tokenize
        
    Returns:
        list: List of lowercase words (Cyrillic and Latin only)
    """
    # Extract words using regex: Cyrillic (а-я, ё) and Latin (a-z) letters only
    words = re.findall(r'[а-яёА-ЯЁa-zA-Z]+', text)
    # Convert all words to lowercase for consistency
    words = [word.lower() for word in words]
    return words


def filter_stop_words(lemmas, stop_words):
    """
    Filter out stop words from the list of lemmas
    
    Args:
        lemmas: List of lemmatized words
        stop_words: Set of stop words to filter out
        
    Returns:
        list: Filtered list with stop words removed
    """
    return [lemma for lemma in lemmas if lemma not in stop_words]


def create_csv_download(freq_data, filename):
    """
    Create CSV data for download
    
    Args:
        freq_data: Dictionary with Ранг, Лемма, Частота
        filename: Name for the downloaded file
        
    Returns:
        CSV data as bytes
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Ранг', 'Лемма', 'Частота'])
    
    # Write data rows
    for i in range(len(freq_data['Ранг'])):
        writer.writerow([
            freq_data['Ранг'][i],
            freq_data['Лемма'][i],
            freq_data['Частота'][i]
        ])
    
    return output.getvalue().encode('utf-8-sig')  # BOM for Excel compatibility


def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="Text Analyzer",
        page_icon="📝",
        layout="wide"
    )
    
    # Header section
    st.title("📝 Text Analyzer")
    st.markdown("""
    Загрузите текстовый файл (.txt, .pdf или .docx) для анализа русского текста.
    Приложение выполнит токенизацию, лемматизацию и частотный анализ.
    """)
    
    # Language selector
    st.markdown("### 🌍 Выберите язык текста")
    language = st.radio(
        "Выберите язык вашего документа:",
        options=["🇷🇺 Русский", "🇧🇾 Беларуская"],
        horizontal=True,
        help="⚠️ ВАЖНО: Выберите правильный язык ПЕРЕД анализом текста!"
    )
    
    # Determine language code and display information
    if "Русский" in language:
        lang_code = "ru"
        lang_emoji = "🇷🇺"
        lang_name = "Русский"
    else:
        lang_code = "be"
        lang_emoji = "🇧🇾"
        lang_name = "Беларуская"
    
    st.info(f"{lang_emoji} **Язык анализа:** {lang_name}")
    
    # Render stop words management UI
    # This returns the combined set of default + custom stop words
    current_stop_words = render_stop_words_ui(lang_code)
    
    # Text input UI (file upload or direct paste)
    text_content, source_name = render_text_input_ui()
    
    # Process text if available
    if text_content is not None and text_content.strip():
        # Display spinner during processing
        with st.spinner("Обработка текста..."):
            try:
                # Step 1: Text is already extracted from render_text_input_ui()
                
                # Step 2: Tokenize text into individual words
                words = tokenize_text(text_content)
                
                # Step 3: Lemmatize words based on selected language
                if lang_code == "ru":
                    # Russian: use pymorphy3 for morphological analysis
                    lemmas = lemmatize_russian(words)
                else:
                    # Belarusian: use lemmatizer_be based on Bnkorpus
                    lemmas = lemmatize_belarusian(words)
                
                # Step 4: Remove stop words (prepositions, conjunctions, etc.)
                # Use stop words from the UI (includes custom additions)
                filtered_lemmas = filter_stop_words(lemmas, current_stop_words)
                
                # Step 5: Calculate statistics for analysis
                total_words = len(words)  # Total word count
                unique_lemmas = len(set(filtered_lemmas))  # Count of unique lemmas
                lemma_freq = Counter(filtered_lemmas)  # Frequency distribution
                top_50_lemmas = lemma_freq.most_common(50)  # Top 50 most frequent
                
                # Display results section
                st.markdown("---")
                st.header("📊 Результаты анализа")
                
                # Show how many stop words were filtered out
                filtered_count = len(lemmas) - len(filtered_lemmas)
                st.info(f"🔍 Отфильтровано {filtered_count} стоп-слов ({(filtered_count/len(lemmas)*100):.1f}% от общего числа)")
                
                # Display three key metrics in columns
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        label="Всего слов",
                        value=f"{total_words:,}",
                        help="Общее количество слов в тексте"
                    )
                with col2:
                    st.metric(
                        label="Уникальных лемм",
                        value=f"{unique_lemmas:,}",
                        help="Количество уникальных лемматизированных форм"
                    )
                with col3:
                    # Lexical diversity = ratio of unique lemmas to total words
                    st.metric(
                        label="Лексическое разнообразие",
                        value=f"{(unique_lemmas / total_words * 100):.1f}%",
                        help="Отношение уникальных лемм к общему количеству слов"
                    )
                
                st.markdown("---")
                
                # Display top 50 most frequent lemmas
                st.subheader("🔝 Топ-50 наиболее частых лемм")
                
                # Prepare data for table display (rank, lemma, frequency)
                freq_data = {
                    "Ранг": list(range(1, len(top_50_lemmas) + 1)),
                    "Лемма": [lemma for lemma, _ in top_50_lemmas],
                    "Частота": [freq for _, freq in top_50_lemmas]
                }
                st.table(freq_data)
                
                # Create CSV download button for exporting results
                csv_data = create_csv_download(freq_data, "results.csv")
                # Generate filename from source (remove extension if present)
                safe_filename = source_name.rsplit('.', 1)[0] if '.' in source_name else source_name
                safe_filename = safe_filename.replace(' ', '_')
                st.download_button(
                    label="📥 Скачать результаты (CSV)",
                    data=csv_data,
                    file_name=f"text_analysis_{safe_filename}.csv",
                    mime="text/csv",
                    help="Загрузить таблицу частот в формате CSV для Excel"
                )
                
                # Optional: Show preview of original text in expandable section
                with st.expander("📄 Просмотр оригинального текста (первые 500 символов)"):
                    preview_text = text_content[:500]
                    if len(text_content) > 500:
                        preview_text += "..."
                    st.text(preview_text)
                
            except Exception as e:
                # Display error message if something goes wrong during processing
                st.error(f"❌ Ошибка обработки текста: {str(e)}")
                st.exception(e)


if __name__ == "__main__":
    main()

