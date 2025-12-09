# Quick Start Guide

## Setup Instructions

### 1. Create Virtual Environment (First Time Only)

Create a Python virtual environment to isolate dependencies:

```bash
python3 -m venv venv
```

**Note**: You only need to do this once, unless you delete the `venv` folder.

### 2. Install Dependencies (First Time Only)

Activate the virtual environment and install packages:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Note**: The `pymorphy3-dicts-ru` package is ~50MB and contains Russian morphological dictionaries. It will be downloaded during installation.

### 3. Run the Application

**Easy way** (recommended) - Use the provided script:

```bash
./run.sh
```

**Manual way** - Activate the environment and run:

```bash
source venv/bin/activate
streamlit run src/app.py
```

The application will automatically open in your web browser at `http://localhost:8501`

### 4. Stop the Application

Press `Ctrl+C` in the terminal, or use:

```bash
./stop.sh
```

### 5. Test the Application

A sample Russian text file is included: `sample_text.txt`

Upload it to test the functionality:
- Total words: ~171
- Unique lemmas: ~113
- Top words will include: война, мир, роман, толстой

## Features Overview

### File Upload
- Drag and drop or click to upload
- Supported formats: `.txt`, `.pdf`, `.docx`
- Multiple encoding support (UTF-8, CP1251)

### Analysis Performed
1. **Tokenization**: Extracts words using regex (Cyrillic and Latin letters)
2. **Lemmatization**: Converts each word to its dictionary form using pymorphy2
3. **Frequency Analysis**: Counts occurrences of each lemma
4. **Statistics**: Calculates total words, unique lemmas, and lexical diversity

### Output
- **Metrics**: Total words, unique lemmas, lexical diversity %
- **Top 50 Lemmas**: Ranked frequency table
- **Sample**: First 50 lemmas from the text
- **Preview**: First 500 characters of original text
