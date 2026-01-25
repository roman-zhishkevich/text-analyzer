"""
GrammarDB Handler
Handles loading and lookup from GrammarDB Belarusian grammar database
"""

import json
import os
from pathlib import Path


class GrammarDBHandler:
    """
    Handler for GrammarDB - Belarusian grammar database
    Provides fast dictionary lookup for word lemmatization
    """
    
    def __init__(self, grammardb_path=None):
        """
        Initialize GrammarDB handler
        
        Args:
            grammardb_path: Path to GrammarDB data file (JSON format)
                          If None, looks for default location
        """
        self.word_to_lemma = {}
        self.loaded = False
        
        if grammardb_path and os.path.exists(grammardb_path):
            self.load_database(grammardb_path)
    
    def load_database(self, grammardb_path):
        """
        Load GrammarDB dictionary into memory
        
        Args:
            grammardb_path: Path to GrammarDB JSON file
            
        Expected JSON format:
        {
            "хлопчык": "хлопчык",
            "хлопчыка": "хлопчык",
            "хлопчыкі": "хлопчык",
            ...
        }
        """
        try:
            with open(grammardb_path, 'r', encoding='utf-8') as f:
                self.word_to_lemma = json.load(f)
            self.loaded = True
            print(f"✅ GrammarDB loaded: {len(self.word_to_lemma):,} word forms")
        except FileNotFoundError:
            print(f"⚠️ GrammarDB file not found: {grammardb_path}")
            self.loaded = False
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing GrammarDB file: {e}")
            self.loaded = False
        except Exception as e:
            print(f"❌ Error loading GrammarDB: {e}")
            self.loaded = False
    
    def lookup(self, word):
        """
        Look up word in GrammarDB dictionary
        
        Args:
            word: Word form to look up
            
        Returns:
            str: Lemma if found, None if not found
        """
        if not self.loaded:
            return None
        
        # Normalize word (lowercase)
        word_normalized = word.lower().strip()
        
        # Fast dictionary lookup - O(1)
        return self.word_to_lemma.get(word_normalized)
    
    def is_in_dictionary(self, word):
        """
        Check if word exists in GrammarDB
        
        Args:
            word: Word to check
            
        Returns:
            bool: True if word is in dictionary, False otherwise
        """
        if not self.loaded:
            return False
        
        return word.lower().strip() in self.word_to_lemma
    
    def get_stats(self):
        """
        Get statistics about loaded dictionary
        
        Returns:
            dict: Statistics (total words, loaded status)
        """
        return {
            'loaded': self.loaded,
            'total_forms': len(self.word_to_lemma),
            'unique_lemmas': len(set(self.word_to_lemma.values())) if self.loaded else 0
        }


# Singleton instance for caching
_grammardb_instance = None


def get_grammardb_handler(grammardb_path=None):
    """
    Get or create GrammarDB handler instance (singleton pattern)
    
    Args:
        grammardb_path: Path to GrammarDB data file
        
    Returns:
        GrammarDBHandler: Handler instance
    """
    global _grammardb_instance
    
    if _grammardb_instance is None:
        _grammardb_instance = GrammarDBHandler(grammardb_path)
    
    return _grammardb_instance

