"""Investigation flow pattern analysis."""

import json
from collections import Counter
from pathlib import Path
from typing import List, Dict, Any


class InvestigationFlows:
    """Analyzes investigation sequences and successful patterns."""
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
    
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
            current_window.append(entry)
            
            # Start new window if we have enough entries
            if len(current_window) >= 5:
                windows.append(current_window)
                current_window = []
        
        if current_window:
            windows.append(current_window)
        
        return windows
    
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