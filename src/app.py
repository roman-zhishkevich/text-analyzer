"""
Text Analyzer - Streamlit App
Supports .txt, .pdf, and .docx files
Performs tokenization and lemmatization for Russian and Belarusian languages
Uses pymorphy3 (Russian) and lemmatizer_be (Belarusian)
"""

import streamlit as st
from collections import Counter
import re
import io
import csv

# File reading imports
import PyPDF2
from docx import Document
from io import BytesIO

# Language support modules
from ru_support import lemmatize_russian, get_russian_stop_words
from be_support import lemmatize_belarusian, get_belarusian_stop_words


def read_txt_file(file):
    """Read content from a .txt file"""
    try:
        # Try UTF-8 first, then fall back to other encodings
        content = file.read().decode('utf-8')
    except UnicodeDecodeError:
        file.seek(0)
        content = file.read().decode('cp1251', errors='ignore')
    return content


def read_pdf_file(file):
    """Read content from a .pdf file"""
    pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
    content = ""
    for page in pdf_reader.pages:
        content += page.extract_text() + "\n"
    return content


def read_docx_file(file):
    """Read content from a .docx file"""
    doc = Document(BytesIO(file.read()))
    content = ""
    for paragraph in doc.paragraphs:
        content += paragraph.text + "\n"
    return content


def read_file_content(uploaded_file):
    """Read file content based on file type"""
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'txt':
        return read_txt_file(uploaded_file)
    elif file_extension == 'pdf':
        return read_pdf_file(uploaded_file)
    elif file_extension == 'docx':
        return read_docx_file(uploaded_file)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


def tokenize_text(text):
    """
    Tokenize text into words
    Removes punctuation and keeps only Cyrillic and Latin letters
    """
    # Extract words (Cyrillic and Latin letters)
    words = re.findall(r'[а-яёА-ЯЁa-zA-Z]+', text)
    # Convert to lowercase
    words = [word.lower() for word in words]
    return words


def filter_stop_words(lemmas, stop_words):
    """
    Filter out stop words from the list of lemmas
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
    
    # Title and description
    st.title("📝 Text Analyzer")
    st.markdown("""
    Загрузите текстовый файл (.txt, .pdf или .docx) для анализа русского текста.
    Приложение выполнит токенизацию, лемматизацию и частотный анализ.
    """)
    
    # Language selector - Belarusian support disabled
    # st.markdown("### 🌍 Выберите язык текста")
    # language = st.radio(
    #     "Выберите язык вашего документа:",
    #     options=["Русский (Russian)", "Беларуская (Belarusian)"],
    #     horizontal=True,
    #     help="⚠️ ВАЖНО: Выберите правильный язык ПЕРЕД анализом текста!"
    # )
    # lang_code = "ru" if "Русский" in language else "be"
    
    # Hardcoded to Russian only
    lang_code = "ru"
    
    # Show selected language
    lang_emoji = "🇷🇺"
    lang_name = "Русский"
    st.info(f"{lang_emoji} **Язык анализа:** {lang_name}")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Выберите файл",
        type=['txt', 'pdf', 'docx'],
        help="Загрузите файл .txt, .pdf или .docx с русским текстом"
    )
    
    if uploaded_file is not None:
        # Display file information
        st.success(f"✅ Файл загружен: **{uploaded_file.name}**")
        
        with st.spinner("Обработка файла..."):
            try:
                # Read file content
                text_content = read_file_content(uploaded_file)
                
                # Tokenize text
                words = tokenize_text(text_content)
                
                # Lemmatize words based on selected language
                if lang_code == "ru":
                    # Russian: use pymorphy3
                    lemmas = lemmatize_russian(words)
                    stop_words = get_russian_stop_words()
                else:
                    # Belarusian: use lemmatizer_be
                    lemmas = lemmatize_belarusian(words)
                    stop_words = get_belarusian_stop_words()
                
                # Filter stop words (always enabled)
                filtered_lemmas = filter_stop_words(lemmas, stop_words)
                
                # Calculate statistics
                total_words = len(words)
                unique_lemmas = len(set(filtered_lemmas))
                lemma_freq = Counter(filtered_lemmas)
                top_20_lemmas = lemma_freq.most_common(20)
                
                # Display results
                st.markdown("---")
                st.header("📊 Результаты анализа")
                
                # Show filter info
                filtered_count = len(lemmas) - len(filtered_lemmas)
                st.info(f"🔍 Отфильтровано {filtered_count} стоп-слов ({(filtered_count/len(lemmas)*100):.1f}% от общего числа)")
                
                # Metrics section
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
                    st.metric(
                        label="Лексическое разнообразие",
                        value=f"{(unique_lemmas / total_words * 100):.1f}%",
                        help="Отношение уникальных лемм к общему количеству слов"
                    )
                
                st.markdown("---")
                
                # Top 20 most frequent lemmas
                st.subheader("🔝 Топ-20 наиболее частых лемм")
                
                # Create a formatted table
                freq_data = {
                    "Ранг": list(range(1, len(top_20_lemmas) + 1)),
                    "Лемма": [lemma for lemma, _ in top_20_lemmas],
                    "Частота": [freq for _, freq in top_20_lemmas]
                }
                st.table(freq_data)
                
                # Download button for CSV
                csv_data = create_csv_download(freq_data, "results.csv")
                st.download_button(
                    label="📥 Скачать результаты (CSV)",
                    data=csv_data,
                    file_name=f"text_analysis_{uploaded_file.name.rsplit('.', 1)[0]}.csv",
                    mime="text/csv",
                    help="Загрузить таблицу частот в формате CSV для Excel"
                )
                
                # Optional: Display raw text preview
                with st.expander("📄 Просмотр оригинального текста (первые 500 символов)"):
                    preview_text = text_content[:500]
                    if len(text_content) > 500:
                        preview_text += "..."
                    st.text(preview_text)
                
            except Exception as e:
                st.error(f"❌ Ошибка обработки файла: {str(e)}")
                st.exception(e)
    else:
        # Show example/demo information
        with st.expander("ℹ️ О программе"):
            st.markdown("""
            ### Возможности:
            - **Поддержка русского языка**: Используется pymorphy3 для точной лемматизации
            - **Поддержка нескольких форматов**: Обработка файлов .txt, .pdf и .docx
            - **Точная лемматизация**: Морфологический анализ с учетом особенностей языка
            - **Автоматическая фильтрация стоп-слов**: Удаление предлогов, союзов и служебных слов
            - **Оффлайн обработка**: Вся обработка происходит локально на вашем компьютере
            - **Частотный анализ**: Показывает наиболее частые слова в их лемматизированной форме
            
            ### Как это работает:
            1. Загрузите файл с помощью формы выше
            2. Приложение автоматически определяет тип файла и извлекает текст
            3. Текст токенизируется (разбивается на слова)
            4. Каждое слово лемматизируется с использованием pymorphy3
            5. Рассчитываются статистики и выполняется частотный анализ
            
            ### Технологии:
            - **Русский язык**: pymorphy3 с русскими словарями
            - **Поддержка PDF**: PyPDF2
            - **Поддержка DOCX**: python-docx
            """)


if __name__ == "__main__":
    main()

