"""
Text Input Handler
Provides interface for text input via file upload or direct paste
"""

import streamlit as st
from io import BytesIO


def read_txt_file(file):
    """
    Read content from a .txt file with automatic encoding detection
    
    Args:
        file: File object from Streamlit file uploader
        
    Returns:
        str: Decoded text content
    """
    try:
        # Try UTF-8 encoding first (most common)
        content = file.read().decode('utf-8')
    except UnicodeDecodeError:
        # Fallback to Windows-1251 (common for Cyrillic text)
        file.seek(0)  # Reset file pointer to beginning
        content = file.read().decode('cp1251', errors='ignore')
    return content


def read_pdf_file(file):
    """
    Read content from a .pdf file
    
    Args:
        file: File object from Streamlit file uploader
        
    Returns:
        str: Extracted text from all PDF pages
    """
    import PyPDF2
    # Create PDF reader from bytes
    pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
    content = ""
    # Extract text from each page
    for page in pdf_reader.pages:
        content += page.extract_text() + "\n"
    return content


def read_docx_file(file):
    """
    Read content from a .docx file
    
    Args:
        file: File object from Streamlit file uploader
        
    Returns:
        str: Extracted text from all DOCX paragraphs
    """
    from docx import Document
    # Create Document object from bytes
    doc = Document(BytesIO(file.read()))
    content = ""
    # Extract text from each paragraph
    for paragraph in doc.paragraphs:
        content += paragraph.text + "\n"
    return content


def read_file_content(uploaded_file):
    """
    Read file content based on file type
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        str: Extracted text content from the file
        
    Raises:
        ValueError: If file type is not supported
    """
    # Extract file extension from filename
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    # Route to appropriate reader based on file type
    if file_extension == 'txt':
        return read_txt_file(uploaded_file)
    elif file_extension == 'pdf':
        return read_pdf_file(uploaded_file)
    elif file_extension == 'docx':
        return read_docx_file(uploaded_file)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


def render_text_input_ui():
    """
    Render text input interface with file upload and direct text input options
    
    Returns:
        tuple: (text_content, source_name) where text_content is the text to analyze
               and source_name is the name/description of the source
    """
    st.subheader("📄 Выберите способ ввода текста")
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📁 Загрузить файл", "✏️ Вставить текст"])
    
    text_content = None
    source_name = None
    
    # Tab 1: File Upload
    with tab1:
        uploaded_file = st.file_uploader(
            "Выберите файл",
            type=['txt', 'pdf', 'docx'],
            help="Поддерживаются форматы: .txt, .pdf, .docx"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ Файл загружен: **{uploaded_file.name}**")
            try:
                text_content = read_file_content(uploaded_file)
                source_name = uploaded_file.name
            except Exception as e:
                st.error(f"❌ Ошибка чтения файла: {str(e)}")
                return None, None
    
    # Tab 2: Direct Text Input
    with tab2:
        direct_text = st.text_area(
            "Вставьте текст для анализа:",
            height=400,
            max_chars=100000,
            placeholder="Вставьте ваш текст здесь (до 100,000 символов)...",
            help="Можно вставить текст напрямую из буфера обмена"
        )
        
        # Show statistics if text is present
        if direct_text and direct_text.strip():
            char_count = len(direct_text)
            word_count = len(direct_text.split())
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Символов", f"{char_count:,}")
            with col2:
                st.metric("Слов (приблиз.)", f"{word_count:,}")
        
        # Always show the button
        if st.button("📊 Анализировать текст", type="primary", disabled=not (direct_text and direct_text.strip())):
            if direct_text and direct_text.strip():
                text_content = direct_text
                source_name = "Прямой ввод текста"
    
    return text_content, source_name

