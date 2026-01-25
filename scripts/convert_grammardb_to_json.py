#!/usr/bin/env python3
"""
Convert GrammarDB XML files to JSON format
Extracts word forms and their lemmas for fast dictionary lookup
"""

import xml.etree.ElementTree as ET
import json
import os
import sys
from pathlib import Path


def parse_grammardb_xml(xml_file):
    """
    Parse a single GrammarDB XML file
    
    Real GrammarDB structure:
    <Wordlist>
        <Paradigm pdgId="..." lemma="а+" tag="...">
            <Variant id="..." lemma="а+" ...>
                <Form tag="...">а+</Form>
            </Variant>
        </Paradigm>
    </Wordlist>
    
    Args:
        xml_file: Path to XML file
        
    Returns:
        dict: word_form -> lemma mapping
    """
    word_to_lemma = {}
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # GrammarDB structure: <Paradigm> elements with lemma attribute
        for paradigm in root.findall('.//Paradigm'):
            # Get lemma from Paradigm attribute
            lemma_raw = paradigm.get('lemma')
            if not lemma_raw:
                continue
            
            # Clean lemma (remove stress marks, special characters)
            lemma = lemma_raw.replace('+', '').replace('́', '').strip().lower()
            
            if not lemma:
                continue
            
            # Add lemma itself
            word_to_lemma[lemma] = lemma
            
            # Get all Form elements within this Paradigm
            for form_elem in paradigm.findall('.//Form'):
                if form_elem.text:
                    # Clean form (remove stress marks, special characters)
                    word_form = form_elem.text.replace('+', '').replace('́', '').strip().lower()
                    if word_form and word_form not in word_to_lemma:
                        word_to_lemma[word_form] = lemma
        
        print(f"✅ Parsed {xml_file.name}: {len(word_to_lemma):,} forms")
        
    except Exception as e:
        print(f"⚠️ Error parsing {xml_file}: {e}")
    
    return word_to_lemma


def convert_grammardb_directory(input_dir, output_json):
    """
    Convert all GrammarDB XML files in directory to single JSON
    
    Args:
        input_dir: Directory containing XML files
        output_json: Output JSON file path
    """
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"❌ Error: Directory not found: {input_dir}")
        sys.exit(1)
    
    # Find all XML files
    xml_files = list(input_path.glob("**/*.xml"))
    
    if not xml_files:
        print(f"❌ Error: No XML files found in {input_dir}")
        print("Looking for files...")
        all_files = list(input_path.glob("**/*"))
        for f in all_files[:20]:  # Show first 20 files
            print(f"  - {f}")
        sys.exit(1)
    
    print(f"📁 Found {len(xml_files)} XML files")
    print()
    
    # Combine all word forms from all files
    all_words = {}
    
    for xml_file in xml_files:
        word_map = parse_grammardb_xml(xml_file)
        all_words.update(word_map)
    
    print()
    print(f"📊 Total Statistics:")
    print(f"   Total word forms: {len(all_words):,}")
    print(f"   Unique lemmas: {len(set(all_words.values())):,}")
    print()
    
    # Write to JSON
    output_path = Path(output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"💾 Writing to {output_json}...")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_words, f, ensure_ascii=False, indent=2)
    
    # Show file size
    file_size = os.path.getsize(output_json)
    size_mb = file_size / (1024 * 1024)
    print(f"✅ Created: {output_json} ({size_mb:.1f} MB)")
    print()
    print("🎉 Conversion complete!")
    print()
    print("Next steps:")
    print(f"  1. Verify file: cat {output_json} | head -20")
    print(f"  2. Test: python test_belarusian_lemmatizer.py")
    print(f"  3. Start app: ./run.sh")


def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_grammardb_to_json.py <input_dir> <output_json>")
        print()
        print("Example:")
        print("  python scripts/convert_grammardb_to_json.py /tmp/grammardb data/grammardb.json")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_json = sys.argv[2]
    
    print("=" * 70)
    print("GrammarDB XML → JSON Converter")
    print("=" * 70)
    print()
    
    convert_grammardb_directory(input_dir, output_json)


if __name__ == "__main__":
    main()

