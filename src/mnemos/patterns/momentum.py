"""Momentum-driven investigation suggestions."""

import json
from collections import defaultdict, Counter
from pathlib import Path
from typing import List, Dict, Any


class MomentumEngine:
    """Generates investigation suggestions based on behavioral momentum patterns."""
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
    
    def get_momentum_suggestions(self, recent_entries: int = 3, limit: int = 3) -> List[Dict[str, Any]]:
        """Suggest next investigation steps based on behavioral momentum patterns."""
        if not self.log_file.exists():
            return []
        
        entries = self._load_entries()
        if len(entries) < recent_entries:
            return []
        
        # Get recent investigation context
        recent_context = entries[-recent_entries:]
        current_focus = self._extract_investigation_focus(recent_context)
        
        # Find historical patterns: what typically comes after similar contexts?
        momentum_patterns = self._find_momentum_patterns(entries, current_focus)
        
        # Rank suggestions by success rate and frequency
        suggestions = []
        for pattern in momentum_patterns[:limit]:
            suggestions.append({
                'suggestion': pattern['next_step'],
                'confidence': pattern['success_rate'],
                'frequency': pattern['frequency'],
                'context': pattern['similar_context'],
                'rationale': f"You typically investigate '{pattern['next_step']}' after {pattern['trigger_pattern']}"
            })
        
        return suggestions
    
    def _extract_investigation_focus(self, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract the current investigation focus from recent entries."""
        focus = {
            'types': [e.get('type', 'unknown') for e in entries],
            'keywords': [],
            'themes': []
        }
        
        # Extract key terms from recent content
        for entry in entries:
            for field in ['what', 'understanding', 'breakthrough', 'problem']:
                if field in entry:
                    text = entry[field].lower()
                    # Extract meaningful terms
                    words = [w for w in text.split() if len(w) > 4 and w.isalpha()]
                    focus['keywords'].extend(words[:3])  # Top 3 per entry
        
        # Identify themes (recurring concepts)
        keyword_counts = Counter(focus['keywords'])
        focus['themes'] = [term for term, count in keyword_counts.most_common(3) if count > 1]
        
        return focus
    
    def _find_momentum_patterns(self, entries: List[Dict[str, Any]], current_focus: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find patterns of what typically follows similar investigation contexts."""
        patterns = []
        
        # Look for similar historical contexts
        for i in range(len(entries) - 4):  # Need at least 4 entries to see pattern
            window = entries[i:i+3]  # 3-entry context window
            next_entry = entries[i+3]
            
            # Check if this window is similar to current focus
            similarity_score = self._calculate_context_similarity(window, current_focus)
            
            if similarity_score > 0.3:  # Threshold for "similar enough"
                # What happened next?
                next_action = self._extract_next_action(next_entry)
                if next_action:
                    patterns.append({
                        'next_step': next_action,
                        'similar_context': window,
                        'trigger_pattern': " → ".join(e.get('type', 'unknown') for e in window),
                        'outcome_type': next_entry.get('type', 'unknown'),
                        'similarity': similarity_score
                    })
        
        # Calculate success rates and frequencies
        pattern_stats = defaultdict(lambda: {'count': 0, 'successes': 0})
        
        for pattern in patterns:
            key = pattern['next_step']
            pattern_stats[key]['count'] += 1
            if pattern['outcome_type'] in ['discovery', 'resolved', 'insight']:
                pattern_stats[key]['successes'] += 1
        
        # Build final pattern list with stats
        final_patterns = []
        for pattern in patterns:
            key = pattern['next_step']
            stats = pattern_stats[key]
            pattern.update({
                'frequency': stats['count'],
                'success_rate': stats['successes'] / stats['count'] if stats['count'] > 0 else 0
            })
            final_patterns.append(pattern)
        
        # Sort by success rate then frequency
        return sorted(final_patterns, key=lambda x: (x['success_rate'], x['frequency']), reverse=True)
    
    def _calculate_context_similarity(self, window: List[Dict[str, Any]], current_focus: Dict[str, Any]) -> float:
        """Calculate similarity between historical window and current focus."""
        window_types = [e.get('type', 'unknown') for e in window]
        window_keywords = []
        
        for entry in window:
            for field in ['what', 'understanding', 'breakthrough', 'problem']:
                if field in entry:
                    text = entry[field].lower()
                    words = [w for w in text.split() if len(w) > 4 and w.isalpha()]
                    window_keywords.extend(words[:2])
        
        # Type similarity (exact matches)
        type_overlap = len(set(window_types) & set(current_focus['types']))
        type_similarity = type_overlap / max(len(set(window_types)), len(set(current_focus['types'])), 1)
        
        # Keyword similarity
        keyword_overlap = len(set(window_keywords) & set(current_focus['keywords']))
        keyword_similarity = keyword_overlap / max(len(set(window_keywords)), len(set(current_focus['keywords'])), 1)
        
        # Combined similarity (weighted toward types as they're more reliable)
        return 0.7 * type_similarity + 0.3 * keyword_similarity
    
    def _extract_next_action(self, entry: Dict[str, Any]) -> str:
        """Extract the key action/focus from an entry."""
        entry_type = entry.get('type', 'unknown')
        
        if entry_type == 'observation':
            content = entry.get('what', '')
        elif entry_type == 'insight':
            content = entry.get('understanding', '')
        elif entry_type == 'discovery':
            content = entry.get('breakthrough', '')
        elif entry_type == 'issue':
            content = entry.get('problem', '')
        else:
            return None
        
        if not content:
            return None
        
        # Extract the key action or focus (first few words)
        words = content.split()[:6]  # First 6 words usually capture the essence
        return ' '.join(words)
    
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