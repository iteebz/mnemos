"""Search pattern analysis for cognitive breadcrumbs."""

import json
from collections import Counter
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class SearchPatterns:
    """Analyzes search sequences and provides cognitive breadcrumbs."""
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.session_searches = []
    
    def track_search(self, term: str) -> None:
        """Track search term for sequence analysis."""
        self.session_searches.append({
            'term': term,
            'timestamp': datetime.now()
        })
    
    def get_search_breadcrumbs(self, current_term: str, limit: int = 5) -> List[str]:
        """Get related search terms based on historical sequences."""
        if not self.log_file.exists():
            return []
        
        sequences = self._extract_search_sequences()
        related_terms = Counter()
        
        # Find terms that appeared after current_term in sequences
        for sequence in sequences:
            if current_term.lower() in [s.lower() for s in sequence]:
                term_index = next(i for i, s in enumerate(sequence) if s.lower() == current_term.lower())
                # Add terms that came after this one
                for next_term in sequence[term_index + 1:]:
                    if next_term.lower() != current_term.lower():
                        related_terms[next_term] += 1
        
        return [term for term, count in related_terms.most_common(limit)]
    
    def _extract_search_sequences(self) -> List[List[str]]:
        """Extract search term sequences from logs (implied by content analysis)."""
        sequences = []
        entries = self._load_entries()
        
        # Group entries by time windows (5-minute sessions)
        time_windows = self._group_by_time_windows(entries, minutes=5)
        
        for window in time_windows:
            # Extract key terms from each window
            terms = self._extract_key_terms(window)
            if len(terms) > 1:
                sequences.append(terms)
        
        return sequences
    
    def _load_entries(self) -> List[Dict[str, Any]]:
        """Load all log entries."""
        entries = []
        if not self.log_file.exists():
            return entries
        
        with open(self.log_file, 'r') as f:
            for line in f:
                try:
                    entries.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
        
        return entries
    
    def _group_by_time_windows(self, entries: List[Dict], minutes: int = 5) -> List[List[Dict]]:
        """Group entries into temporal windows."""
        if not entries:
            return []
        
        windows = []
        current_window = [entries[0]]
        
        for entry in entries[1:]:
            # Simple grouping by timestamp (this is basic - could be improved)
            current_window.append(entry)
            
            # Start new window if we have enough entries
            if len(current_window) >= 5:
                windows.append(current_window)
                current_window = []
        
        if current_window:
            windows.append(current_window)
        
        return windows
    
    def _extract_key_terms(self, entries: List[Dict]) -> List[str]:
        """Extract key terms from a group of entries."""
        terms = []
        
        for entry in entries:
            # Extract meaningful terms from text fields
            for field in ['what', 'understanding', 'breakthrough', 'problem']:
                if field in entry:
                    text = entry[field].lower()
                    # Simple term extraction (could be more sophisticated)
                    key_terms = [word for word in text.split() 
                               if len(word) > 4 and word.isalpha()]
                    terms.extend(key_terms[:2])  # Top 2 terms per entry
        
        # Return unique terms
        return list(dict.fromkeys(terms))