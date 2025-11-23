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

**Note**: The `pymorphy3-dicts-ru` package is ~50MB and contains Russian morphological dictionaries. It will be downloaded during installation

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
- **Top 20 Lemmas**: Ranked frequency table
- **Sample**: First 50 lemmas from the text
- **Preview**: First 500 characters of original text

## Troubleshooting

### Command Not Found Error
If you get `streamlit: command not found`, make sure you've activated the virtual environment:
```bash
source venv/bin/activate
```
Or simply use the provided script: `./run.sh`

### Import Errors
If you get import errors, make sure all packages are installed:
```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Virtual Environment Issues
If the virtual environment seems broken (Python not found, packages missing), recreate it:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use
If port 8501 is busy, specify a different port:
```bash
source venv/bin/activate
streamlit run src/app.py --server.port 8502
```

### PDF Extraction Issues
Some PDFs may have extraction problems:
- Make sure the PDF contains text (not scanned images)
- Try converting to .txt first if issues persist

### DOCX Issues
If DOCX files don't load properly:
- Make sure the file is a valid .docx (not .doc)
- Try opening and re-saving in Word/LibreOffice

## Performance Tips

- **First run**: May be slower due to pymorphy2 initialization
- **Subsequent runs**: Analyzer is cached for better performance
- **Large files**: Processing time scales with file size
- **Memory**: Large documents (>10MB) may require more RAM

## Offline Usage

Once dependencies are installed, the app works completely offline:
- No internet connection required
- All processing happens locally
- No data is sent to external servers
- Russian dictionaries are stored locally

## Example Workflow

1. Open the app: `./run.sh`
2. Upload a Russian text file
3. Review the metrics (word count, unique lemmas)
4. Check the top 20 most frequent words
5. Examine the lemma sample for quality check
6. Use the expander to view original text

## Next Steps

- Test with your own Russian text files
- Try different file formats (.txt, .pdf, .docx)
- Compare frequency analysis across different texts
- Use for linguistic research or text analysis projects

Enjoy analyzing Russian texts!

