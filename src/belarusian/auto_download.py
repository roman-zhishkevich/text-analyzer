"""
Auto-download GrammarDB on first run
Designed for Streamlit Cloud deployment
"""

import os
import sys
import json
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.request import urlopen, Request
from zipfile import ZipFile


# GrammarDB release URL
GRAMMARDB_URL = "https://github.com/Belarus/GrammarDB/releases/download/RELEASE-202601/RELEASE-202601.zip"


def parse_grammardb_xml(xml_content):
    """Parse GrammarDB XML and extract word→lemma mappings"""
    word_to_lemma = {}
    
    try:
        root = ET.fromstring(xml_content)
        
        for paradigm in root.findall('.//Paradigm'):
            lemma_raw = paradigm.get('lemma')
            if not lemma_raw:
                continue
            
            # Clean lemma (remove stress marks)
            lemma = lemma_raw.replace('+', '').replace('́', '').strip().lower()
            
            if not lemma:
                continue
            
            # Add lemma itself
            word_to_lemma[lemma] = lemma
            
            # Get all forms
            for form_elem in paradigm.findall('.//Form'):
                if form_elem.text:
                    word_form = form_elem.text.replace('+', '').replace('́', '').strip().lower()
                    if word_form and word_form not in word_to_lemma:
                        word_to_lemma[word_form] = lemma
        
    except Exception as e:
        print(f"⚠️ Error parsing XML: {e}")
    
    return word_to_lemma


def download_and_setup_grammardb(target_path):
    """
    Download GrammarDB from GitHub and convert to JSON
    
    Args:
        target_path: Path where to save grammardb.json
        
    Returns:
        bool: True if successful, False otherwise
    """
    print("📥 Downloading GrammarDB from GitHub...")
    
    try:
        # Download with user agent (some servers require it)
        req = Request(GRAMMARDB_URL, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urlopen(req, timeout=120) as response:
            zip_data = response.read()
        
        print(f"✅ Downloaded {len(zip_data) / (1024*1024):.1f} MB")
        
        # Extract and parse
        print("📂 Extracting and parsing XML files...")
        
        all_words = {}
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract ZIP to temp directory
            zip_path = Path(temp_dir) / "grammardb.zip"
            zip_path.write_bytes(zip_data)
            
            with ZipFile(zip_path, 'r') as zip_file:
                zip_file.extractall(temp_dir)
            
            # Parse all XML files
            xml_files = list(Path(temp_dir).glob("*.xml"))
            print(f"📄 Found {len(xml_files)} XML files")
            
            for xml_file in xml_files:
                try:
                    xml_content = xml_file.read_text(encoding='utf-8')
                    words = parse_grammardb_xml(xml_content)
                    all_words.update(words)
                    print(f"   ✅ {xml_file.name}: {len(words):,} forms")
                except Exception as e:
                    print(f"   ⚠️ {xml_file.name}: {e}")
        
        # Save to JSON
        print(f"💾 Saving {len(all_words):,} word forms to JSON...")
        
        # Create parent directory if needed
        Path(target_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(all_words, f, ensure_ascii=False, indent=2)
        
        file_size = Path(target_path).stat().st_size / (1024 * 1024)
        print(f"✅ GrammarDB saved: {target_path} ({file_size:.1f} MB)")
        print(f"📊 Total: {len(all_words):,} word forms, {len(set(all_words.values())):,} unique lemmas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during download/setup: {e}")
        import traceback
        traceback.print_exc()
        return False


def ensure_grammardb_ready():
    """
    Ensure GrammarDB is available
    Downloads and sets up if not present
    
    Returns:
        bool: True if GrammarDB is ready, False if setup failed
    """
    # Determine path to grammardb.json
    # Go up from src/belarusian/ to project root
    project_root = Path(__file__).parent.parent.parent
    grammardb_path = project_root / "data" / "grammardb.json"
    
    # Check if already exists
    if grammardb_path.exists():
        file_size = grammardb_path.stat().st_size / (1024 * 1024)
        print(f"✅ GrammarDB already exists: {grammardb_path} ({file_size:.1f} MB)")
        return True
    
    print(f"⚠️ GrammarDB not found at: {grammardb_path}")
    print("🔄 Starting automatic download and setup...")
    
    # Download and setup
    success = download_and_setup_grammardb(str(grammardb_path))
    
    if success:
        print("🎉 GrammarDB setup completed successfully!")
        return True
    else:
        print("⚠️ GrammarDB setup failed. Falling back to basic mode.")
        return False


if __name__ == "__main__":
    # Can be run standalone for testing
    ensure_grammardb_ready()

