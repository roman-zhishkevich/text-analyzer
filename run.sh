#!/bin/bash
# Run the Text Analyzer Streamlit App

cd "$(dirname "$0")"
source venv/bin/activate
streamlit run src/app.py

