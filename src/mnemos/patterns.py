"""Behavioral pattern recognition for Claude's investigation flows."""

import json
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta


class BehavioralPatterns:
    """Captures and surfaces Claude's investigation patterns without embeddings."""
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.session_searches = []  # Track search sequences in current session
    
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
    
    def get_investigation_flows(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Get common investigation flow patterns."""
        if not self.log_file.exists():
            return []
        
        flows = self._extract_investigation_flows()
        flow_patterns = Counter()
        
        for flow in flows:
            pattern = " → ".join(flow['types'])
            flow_patterns[pattern] += 1
        
        common_patterns = []
        for pattern, count in flow_patterns.most_common(limit):
            # Find a recent example of this pattern
            example = next((f for f in flows if " → ".join(f['types']) == pattern), None)
            common_patterns.append({
                'pattern': pattern,
                'count': count,
                'example': example['entries'] if example else []
            })
        
        return common_patterns
    
    def get_location_clusters(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get issue clusters by location."""
        if not self.log_file.exists():
            return []
        
        location_issues = defaultdict(list)
        
        with open(self.log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if entry.get('type') == 'issue' and 'location' in entry:
                        location_issues[entry['location']].append({
                            'problem': entry['problem'],
                            'severity': entry.get('severity', 'medium'),
                            'timestamp': entry['timestamp']
                        })
                except json.JSONDecodeError:
                    continue
        
        # Sort by issue count and return top locations
        sorted_locations = sorted(
            location_issues.items(), 
            key=lambda x: len(x[1]), 
            reverse=True
        )[:limit]
        
        return [
            {
                'location': location,
                'issue_count': len(issues),
                'recent_issues': issues[-3:],  # Last 3 issues
                'severity_distribution': Counter(i['severity'] for i in issues)
            }
            for location, issues in sorted_locations
        ]
    
    def get_successful_patterns(self, pattern_type: str = None) -> List[Dict[str, Any]]:
        """Get successful investigation patterns that led to discoveries."""
        if not self.log_file.exists():
            return []
        
        successful_sequences = []
        entries = self._load_entries()
        
        # Find sequences ending in discoveries or resolutions
        for i, entry in enumerate(entries):
            if entry.get('type') in ['discovery', 'resolved']:
                # Look back for the sequence that led to this success
                lookback_start = max(0, i - 5)  # Look back up to 5 entries
                sequence = entries[lookback_start:i+1]
                
                if len(sequence) > 1:  # Only meaningful sequences
                    successful_sequences.append({
                        'outcome': entry,
                        'sequence': sequence,
                        'pattern': " → ".join(s.get('type', 'unknown') for s in sequence)
                    })
        
        return successful_sequences[-5:]  # Return 5 most recent successful patterns
    
    def _extract_search_sequences(self) -> List[List[str]]:
        """Extract search term sequences from logs (implied by content analysis)."""
        # This is a simplified approach - in real implementation, we'd track actual searches
        # For now, we extract terms that appear frequently together in content
        sequences = []
        
        # Look for terms that appear in similar contexts (basic co-occurrence)
        entries = self._load_entries()
        
        # Group entries by time windows (5-minute sessions)
        time_windows = self._group_by_time_windows(entries, minutes=5)
        
        for window in time_windows:
            # Extract key terms from each window
            terms = self._extract_key_terms(window)
            if len(terms) > 1:
                sequences.append(terms)
        
        return sequences
    
    def _extract_investigation_flows(self) -> List[Dict[str, Any]]:
        """Extract sequences of investigation types."""
        entries = self._load_entries()
        flows = []
        
        # Group entries by time windows
        time_windows = self._group_by_time_windows(entries, minutes=10)
        
        for window in time_windows:
            if len(window) > 1:  # Only meaningful flows
                flows.append({
                    'types': [entry.get('type', 'unknown') for entry in window],
                    'entries': [self._summarize_entry(entry) for entry in window],
                    'timestamp': window[0].get('timestamp', '')
                })
        
        return flows
    
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
    
    def _summarize_entry(self, entry: Dict[str, Any]) -> Dict[str, str]:
        """Create a summary of an entry for pattern display."""
        summary = {'type': entry.get('type', 'unknown')}
        
        # Extract the main content based on type
        if entry.get('type') == 'observation':
            summary['content'] = entry.get('what', '')[:50] + '...'
        elif entry.get('type') == 'insight':
            summary['content'] = entry.get('understanding', '')[:50] + '...'
        elif entry.get('type') == 'discovery':
            summary['content'] = entry.get('breakthrough', '')[:50] + '...'
        elif entry.get('type') == 'issue':
            summary['content'] = entry.get('problem', '')[:50] + '...'
        else:
            # Generic fallback
            for field in ['what', 'understanding', 'breakthrough', 'problem', 'idea']:
                if field in entry:
                    summary['content'] = entry[field][:50] + '...'
                    break
        
        return summary