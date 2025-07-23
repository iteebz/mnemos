"""Smart Memory Surfacing - Proactive cognitive archaeology."""

import json
from collections import defaultdict, Counter
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta


class MemorySurface:
    """Proactive memory surfacing based on investigation context and behavioral patterns."""
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.relevance_threshold = 0.4  # Minimum relevance for surfacing
        self.max_suggestions = 5  # Maximum findings to surface
    
    def surface_relevant_memory(self, current_context: Optional[str] = None, 
                               recent_limit: int = 3) -> Dict[str, Any]:
        """Surface relevant memory based on current investigation context."""
        if not self.log_file.exists():
            return self._empty_surface()
        
        entries = self._load_entries()
        if len(entries) < 5:  # Need minimum history for relevance
            return self._empty_surface()
        
        # Extract current investigation context
        context = self._extract_current_context(entries, recent_limit, current_context)
        
        # Find relevant historical findings
        relevant_findings = self._find_relevant_findings(entries, context)
        
        # Surface proactive insights
        insights = self._generate_proactive_insights(relevant_findings, context)
        
        return {
            'status': 'surfaced' if relevant_findings else 'no_relevant_memory',
            'context_analysis': context,
            'relevant_findings': relevant_findings[:self.max_suggestions],
            'proactive_insights': insights,
            'surfacing_confidence': self._calculate_confidence(relevant_findings)
        }
    
    def surface_for_entry_type(self, entry_type: str, content: str) -> List[Dict[str, Any]]:
        """Surface memory relevant to a specific entry type and content."""
        if not self.log_file.exists():
            return []
        
        entries = self._load_entries()
        
        # Find similar entries of the same type
        similar_entries = []
        content_keywords = self._extract_keywords(content)
        
        for entry in entries:
            if entry.get('type') == entry_type:
                entry_content = self._get_entry_content(entry)
                if entry_content:
                    similarity = self._calculate_content_similarity(content_keywords, entry_content)
                    if similarity > self.relevance_threshold:
                        similar_entries.append({
                            'entry': entry,
                            'similarity': similarity,
                            'relevance_reason': f"Similar {entry_type} pattern"
                        })
        
        # Also find related discoveries/insights that followed similar patterns
        related_outcomes = self._find_related_outcomes(entries, content_keywords)
        
        # Combine and rank by relevance
        all_relevant = similar_entries + related_outcomes
        return sorted(all_relevant, key=lambda x: x['similarity'], reverse=True)[:3]
    
    def _extract_current_context(self, entries: List[Dict], recent_limit: int, 
                                explicit_context: Optional[str]) -> Dict[str, Any]:
        """Extract current investigation context from recent entries."""
        recent_entries = entries[-recent_limit:] if len(entries) >= recent_limit else entries
        
        context = {
            'recent_types': [e.get('type', 'unknown') for e in recent_entries],
            'keywords': [],
            'themes': [],
            'active_issues': [],
            'investigation_momentum': None,
            'explicit_focus': explicit_context
        }
        
        # Extract keywords from recent activity
        all_keywords = []
        for entry in recent_entries:
            content = self._get_entry_content(entry)
            if content:
                keywords = self._extract_keywords(content)
                all_keywords.extend(keywords)
        
        # Identify dominant themes
        keyword_counts = Counter(all_keywords)
        context['themes'] = [word for word, count in keyword_counts.most_common(5) if count > 1]
        context['keywords'] = list(keyword_counts.keys())[:10]
        
        # Find active issues (unresolved)
        all_entries = entries
        issue_ids = {e.get('id') for e in all_entries if e.get('type') == 'issue'}
        resolved_ids = {e.get('issue_id') for e in all_entries if e.get('type') == 'resolved'}
        active_issue_ids = issue_ids - resolved_ids
        
        context['active_issues'] = [
            e for e in all_entries 
            if e.get('type') == 'issue' and e.get('id') in active_issue_ids
        ]
        
        # Detect investigation momentum (pattern in recent types)
        if len(context['recent_types']) >= 2:
            context['investigation_momentum'] = " → ".join(context['recent_types'])
        
        return context
    
    def _find_relevant_findings(self, entries: List[Dict], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find historical findings relevant to current context."""
        relevant = []
        
        # Skip recent entries (already in current context)
        historical_entries = entries[:-3] if len(entries) > 3 else []
        
        for entry in historical_entries:
            relevance_score = self._calculate_relevance(entry, context)
            if relevance_score > self.relevance_threshold:
                relevant.append({
                    'entry': entry,
                    'relevance_score': relevance_score,
                    'relevance_reasons': self._explain_relevance(entry, context, relevance_score)
                })
        
        return sorted(relevant, key=lambda x: x['relevance_score'], reverse=True)
    
    def _calculate_relevance(self, entry: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Calculate relevance score between entry and current context."""
        score = 0.0
        
        # Type relevance - same or complementary types
        entry_type = entry.get('type', 'unknown')
        if entry_type in context['recent_types']:
            score += 0.3  # Same type recently used
        
        # Complement patterns (observation → insight → discovery)
        complement_map = {
            'observation': ['insight', 'discovery'],
            'insight': ['discovery', 'pattern'],
            'issue': ['resolved', 'discovery']
        }
        if entry_type in complement_map:
            recent_types = set(context['recent_types'])
            if any(comp_type in recent_types for comp_type in complement_map[entry_type]):
                score += 0.2
        
        # Keyword relevance
        entry_content = self._get_entry_content(entry)
        if entry_content and context['keywords']:
            entry_keywords = self._extract_keywords(entry_content)
            keyword_overlap = len(set(entry_keywords) & set(context['keywords']))
            keyword_score = keyword_overlap / max(len(context['keywords']), 1)
            score += 0.4 * keyword_score
        
        # Theme relevance (stronger signal)
        if entry_content and context['themes']:
            entry_keywords = self._extract_keywords(entry_content)
            theme_overlap = len(set(entry_keywords) & set(context['themes']))
            theme_score = theme_overlap / max(len(context['themes']), 1)
            score += 0.5 * theme_score
        
        # Active issue relevance
        if entry_type == 'resolved' and context['active_issues']:
            # Check if this resolution relates to active issues
            for active_issue in context['active_issues']:
                issue_keywords = self._extract_keywords(self._get_entry_content(active_issue))
                resolved_keywords = self._extract_keywords(entry_content)
                if len(set(issue_keywords) & set(resolved_keywords)) > 0:
                    score += 0.6  # Highly relevant for active problems
        
        # Discovery/pattern relevance (always valuable)
        if entry_type in ['discovery', 'pattern', 'principle']:
            score += 0.2  # Boost important finding types
        
        # Explicit context match
        if context.get('explicit_focus'):
            explicit_keywords = self._extract_keywords(context['explicit_focus'])
            if entry_content:
                entry_keywords = self._extract_keywords(entry_content)
                explicit_overlap = len(set(explicit_keywords) & set(entry_keywords))
                if explicit_overlap > 0:
                    score += 0.7  # High boost for explicit matches
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _explain_relevance(self, entry: Dict[str, Any], context: Dict[str, Any], score: float) -> List[str]:
        """Generate human-readable explanations for why this entry is relevant."""
        reasons = []
        
        entry_type = entry.get('type', 'unknown')
        entry_content = self._get_entry_content(entry)
        
        # Type relevance
        if entry_type in context['recent_types']:
            reasons.append(f"Same type ({entry_type}) in recent investigation")
        
        # Keyword/theme matches
        if entry_content and context['themes']:
            entry_keywords = self._extract_keywords(entry_content)
            matched_themes = set(entry_keywords) & set(context['themes'])
            if matched_themes:
                reasons.append(f"Shares themes: {', '.join(list(matched_themes)[:2])}")
        
        # Issue resolution relevance
        if entry_type == 'resolved' and context['active_issues']:
            reasons.append("Previous resolution pattern for active issues")
        
        # High-value content
        if entry_type in ['discovery', 'pattern', 'principle']:
            reasons.append(f"Strategic {entry_type} from investigation history")
        
        # Explicit focus match
        if context.get('explicit_focus') and entry_content:
            explicit_keywords = self._extract_keywords(context['explicit_focus'])
            entry_keywords = self._extract_keywords(entry_content)
            if set(explicit_keywords) & set(entry_keywords):
                reasons.append("Matches current investigation focus")
        
        return reasons[:3]  # Top 3 reasons
    
    def _generate_proactive_insights(self, relevant_findings: List[Dict], context: Dict[str, Any]) -> List[str]:
        """Generate proactive insights based on relevant findings."""
        insights = []
        
        if not relevant_findings:
            return insights
        
        # Pattern recognition
        finding_types = [f['entry'].get('type') for f in relevant_findings]
        type_counts = Counter(finding_types)
        
        if type_counts.get('resolved', 0) > 1 and context['active_issues']:
            insights.append("💡 Historical resolutions available for similar active issues")
        
        if type_counts.get('discovery', 0) > 2:
            insights.append("🎯 Multiple relevant discoveries - potential pattern synthesis opportunity")
        
        if type_counts.get('pattern', 0) > 0:
            insights.append("🏗️ Architectural patterns relevant to current investigation")
        
        # Investigation momentum insights
        if context.get('investigation_momentum'):
            momentum = context['investigation_momentum']
            if 'observation' in momentum and 'insight' not in momentum:
                insights.append("⚡ Consider capturing insights from recent observations")
            elif 'insight' in momentum and 'discovery' not in momentum:
                insights.append("⚡ Insights gathered - potential breakthrough synthesis point")
        
        return insights
    
    def _find_related_outcomes(self, entries: List[Dict], keywords: List[str]) -> List[Dict[str, Any]]:
        """Find successful outcomes that followed similar investigation patterns."""
        related = []
        
        for i, entry in enumerate(entries):
            if entry.get('type') in ['discovery', 'resolved', 'insight']:
                # Look back for similar context
                lookback_start = max(0, i - 3)
                context_entries = entries[lookback_start:i]
                
                context_content = []
                for ctx_entry in context_entries:
                    content = self._get_entry_content(ctx_entry)
                    if content:
                        context_content.extend(self._extract_keywords(content))
                
                # Check similarity to current keywords
                similarity = len(set(keywords) & set(context_content)) / max(len(keywords), 1)
                
                if similarity > 0.3:
                    related.append({
                        'entry': entry,
                        'similarity': similarity,
                        'relevance_reason': f"Similar context led to {entry.get('type')}"
                    })
        
        return related
    
    def _get_entry_content(self, entry: Dict[str, Any]) -> Optional[str]:
        """Extract the main content from an entry."""
        content_fields = ['what', 'understanding', 'breakthrough', 'problem', 'idea', 'insight', 'rule']
        for field in content_fields:
            if field in entry and entry[field]:
                return entry[field]
        return None
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text."""
        if not text:
            return []
        
        # Simple keyword extraction - words longer than 3 chars, alphanumeric
        words = text.lower().split()
        keywords = [
            word.strip('.,!?()[]{}";:') 
            for word in words 
            if len(word) > 3 and word.isalpha()
        ]
        
        # Filter common words
        stop_words = {'this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 'were', 'said', 'each', 'which', 'their', 'time', 'would', 'there', 'could', 'other', 'more', 'very', 'what', 'know', 'just', 'first', 'into', 'over', 'think', 'also', 'your', 'work', 'life', 'only', 'when', 'come', 'like', 'make', 'well', 'even', 'back', 'good', 'much', 'take', 'find'}
        keywords = [k for k in keywords if k not in stop_words]
        
        return keywords[:10]  # Top 10 keywords
    
    def _calculate_content_similarity(self, keywords1: List[str], content2: str) -> float:
        """Calculate content similarity between keyword list and content."""
        keywords2 = self._extract_keywords(content2)
        if not keywords1 or not keywords2:
            return 0.0
        
        overlap = len(set(keywords1) & set(keywords2))
        return overlap / max(len(keywords1), len(keywords2))
    
    def _calculate_confidence(self, relevant_findings: List[Dict]) -> float:
        """Calculate confidence in surfacing results."""
        if not relevant_findings:
            return 0.0
        
        # Average relevance score
        avg_relevance = sum(f['relevance_score'] for f in relevant_findings) / len(relevant_findings)
        
        # Boost confidence if we have multiple relevant findings
        count_boost = min(len(relevant_findings) / 5.0, 0.2)  # Up to 20% boost
        
        return min(avg_relevance + count_boost, 1.0)
    
    def _empty_surface(self) -> Dict[str, Any]:
        """Return empty surfacing result."""
        return {
            'status': 'no_memory',
            'context_analysis': {},
            'relevant_findings': [],
            'proactive_insights': [],
            'surfacing_confidence': 0.0
        }
    
    def _load_entries(self) -> List[Dict[str, Any]]:
        """Load all log entries."""
        entries = []
        if not self.log_file.exists():
            return entries
        
        with open(self.log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    # Skip compression summaries for surfacing
                    if entry.get('type') != 'semantic_summary':
                        entries.append(entry)
                except json.JSONDecodeError:
                    continue
        
        return entries