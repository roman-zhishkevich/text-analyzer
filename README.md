# Text Analyzer - Streamlit App

A Python Streamlit application for analyzing Russian and Belarusian text files with tokenization, lemmatization, and frequency analysis.

## Features

- 🌍 **Multi-language support**: Russian (pymorphy3) and Belarusian (lemmatizer_be)
- 📁 **Multi-format support**: Upload .txt, .pdf, or .docx files
- 🇷🇺 🇧🇾 **Accurate lemmatization**: Language-specific morphological analysis
- 🔍 **Stop words filtering**: Remove prepositions, conjunctions, and common words
- 📊 **Frequency analysis**: View top 20 most common lemmas
- 📥 **CSV Export**: Download analysis results as CSV file
- 🔒 **Completely offline**: All processing happens locally (after initial data download)
- 🎨 **Clean UI**: Beautiful Streamlit interface with metrics and tables

## Installation

1. Create a virtual environment (recommended):

```bash
python3 -m venv venv
```

2. Activate the virtual environment:

```bash
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Starting the App

**Option 1: Using the provided script**
```bash
./run.sh
```

**Option 2: Manual command**
```bash
source venv/bin/activate && streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

### Stopping the App

**Option 1: Using the provided script**
```bash
./stop.sh
```

**Option 2: Manual command**
```bash
pkill -f streamlit
```

**Option 3: In the terminal**
Press `Ctrl + C` if running in the foreground

## How It Works

1. **Select Language**: Choose Russian (Русский) or Belarusian (Беларуская)
2. **Upload**: Choose a .txt, .pdf, or .docx file containing text in your selected language
3. **Processing**: The app automatically:
   - Extracts text from the file
   - Tokenizes the text into words
   - Lemmatizes each word using the appropriate library (pymorphy3 for Russian, lemmatizer_be for Belarusian)
   - Filters stop words (optional, enabled by default)
   - Calculates frequency statistics
4. **Results**: View:
   - Total word count
   - Number of unique lemmas
   - Lexical diversity percentage
   - Top 20 most frequent lemmas
   - Download results as CSV for further analysis

## Requirements

- Python 3.13 or higher (also compatible with 3.11+)
- Internet connection (for initial installation and first-time Belarusian data download ~37MB)
- Once installed and data downloaded, the app works completely offline

## Dependencies

- `streamlit`: Web app framework
- `pymorphy3`: Russian morphological analyzer (Python 3.11+ compatible)
- `pymorphy3-dicts-ru`: Russian dictionaries for pymorphy3
- `lemmatizer_be`: Belarusian lemmatizer based on Bnkorpus
- `PyPDF2`: PDF file reading
- `python-docx`: DOCX file reading
- `setuptools`: Required for pkg_resources

## Example Use Cases

- Analyzing Russian and Belarusian literature texts
- Processing academic papers in Russian or Belarusian
- Studying word frequency in documents
- Lexical diversity analysis for linguistic research
- Comparative analysis between Russian and Belarusian texts
- Text preprocessing for NLP tasks

