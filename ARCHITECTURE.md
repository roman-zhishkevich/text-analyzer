# Project Architecture

This project is organized into modular components for better maintainability and code organization.

## File Structure

```
text_analyzer/
├── src/                    # Source code directory
│   ├── __init__.py         # Package initialization
│   ├── app.py              # Main Streamlit application
│   ├── ru_support.py       # Russian language support module
│   └── be_support.py       # Belarusian language support module
├── venv/                   # Virtual environment (not in git)
├── requirements.txt        # Python dependencies
├── run.sh                  # Start script
├── stop.sh                 # Stop script
├── README.md               # Main documentation
├── QUICKSTART.md           # Quick start guide
├── ARCHITECTURE.md         # This file
└── sample_text.txt         # Sample text file
```

## Module Responsibilities

### `src/app.py` (Main Application)
**Purpose**: Streamlit UI and application logic

**Contains**:
- Streamlit page configuration and UI
- File upload handling
- File reading functions (`.txt`, `.pdf`, `.docx`)
- Text tokenization
- Stop words filtering
- Frequency analysis
- Results display

**Dependencies**: `ru_support`, `be_support`, `streamlit`, `PyPDF2`, `python-docx`

**Note**: Uses direct imports since all modules are in the same `src/` package

---

### `src/ru_support.py` (Russian Language Module)
**Purpose**: Russian language processing

**Contains**:
- `get_russian_analyzer()` - Initializes and caches pymorphy3 analyzer
- `lemmatize_russian(words)` - Lemmatizes Russian words
- `get_russian_stop_words()` - Returns set of Russian stop words (101 words)

**Dependencies**: `pymorphy3`, `streamlit`

**Stop words include**:
- Prepositions (предлоги): в, на, с, к, по, etc.
- Conjunctions (союзы): и, а, но, или, что, etc.
- Particles (частицы): не, ни, бы, ли, etc.
- Pronouns (местоимения): я, ты, он, она, etc.

---

### `src/be_support.py` (Belarusian Language Module)
**Purpose**: Belarusian language processing

**Contains**:
- `get_belarusian_analyzer()` - Initializes and caches Belarusian lemmatizer
- `lemmatize_belarusian(words)` - Lemmatizes Belarusian words
- `get_belarusian_stop_words()` - Returns set of Belarusian stop words (93 words)

**Dependencies**: `lemmatizer_be`, `streamlit`

**Stop words include**:
- Prepositions (прыназоўнікі): у, ў, на, з, да, etc.
- Conjunctions (злучнікі): і, й, а, але, ці, etc.
- Particles (часціцы): не, ні, б, бы, ж, etc.
- Pronouns (займеннікі): я, ты, ён, яна, etc.

---

## Data Flow

```
User uploads file
       ↓
src/app.py reads file (txt/pdf/docx)
       ↓
src/app.py tokenizes text
       ↓
User selects language (Russian/Belarusian)
       ↓
       ├─→ src/ru_support.lemmatize_russian()  (if Russian)
       └─→ src/be_support.lemmatize_belarusian()  (if Belarusian)
       ↓
src/app.py filters stop words (optional)
       ↓
src/app.py calculates frequency
       ↓
src/app.py displays results
```

## Adding New Languages

To add support for a new language:

1. Create a new file: `src/{language_code}_support.py`
2. Implement these functions:
   - `get_{language}_analyzer()` - Initialize lemmatizer
   - `lemmatize_{language}(words)` - Lemmatize function
   - `get_{language}_stop_words()` - Stop words set
3. Import in `src/app.py`
4. Add language option to the radio button
5. Update language selection logic

## Benefits of This Architecture

✅ **Modularity**: Each language is self-contained
✅ **Maintainability**: Easy to update individual language modules
✅ **Testability**: Can test each module independently
✅ **Scalability**: Easy to add new languages
✅ **Clear separation of concerns**: UI logic separate from language processing
✅ **Reusability**: Language modules can be used in other projects

## Testing

Test individual modules:

```bash
# Activate virtual environment first
source venv/bin/activate

# Test Russian module
python3 -c "from src.ru_support import lemmatize_russian; print(lemmatize_russian(['работал']))"

# Test Belarusian module
python3 -c "from src.be_support import lemmatize_belarusian; print(lemmatize_belarusian(['працаваў']))"
```

Test the full application:

```bash
./run.sh
# Then upload a test file in the browser
```

