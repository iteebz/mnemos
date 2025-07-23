#!/usr/bin/env python3
"""Mnemos Core - Autonomous investigation engine.

AUTONOMOUS OPERATION:
When user says "run the mnemos loop", you (Claude) become the investigator.
1. Run this script to see system state and active investigations
2. Read nexus/PROTOCOL.md for investigation methodology (optional - trust instincts)
3. Choose most promising investigation thread or start new discovery  
4. Follow evidence trails using: discovery(), issue(), thread()
5. Think like human investigator: "hmm, let me check...", "that's suspicious..."
6. Trust the process - let evidence guide direction

CORE LOOP: OBSERVE → HYPOTHESIZE → TEST → LEARN → ITERATE
FILES: PROTOCOL.md (methodology), README.md (overview), .mnemos/findings.jsonl (persistent memory)
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List

from .logging import MnemosLogger  
from .analysis import MnemosAnalyzer
from .compression import MnemosCompressor
from .memory_manager import AutoCompressionIntegration
from .patterns import BehavioralPatterns
from .patterns.surfacing import MemorySurface
from .protocols import PROTOCOL, METHODOLOGY, BOUNDARIES, INIT_MESSAGE


class Mnemos:
    """Modular autonomous investigation core - clean separation of concerns."""
    
    def __init__(self):
        # Unified investigation memory for polyrepo monoworkspaces
        if 'MNEMOS_HOME' in os.environ:
            self.mnemos_dir = Path(os.environ['MNEMOS_HOME'])
            self.project_name = 'custom'
        else:
            mnemos_root, project_name = self._find_mnemos_root()
            self.mnemos_dir = Path(mnemos_root)
            self.project_name = project_name
            
        self.log_file = self.mnemos_dir / f"{self.project_name}.jsonl"
        self.reflection_file = self.mnemos_dir / f"{self.project_name}_reflections.jsonl"
        self.mnemos_dir.mkdir(parents=True, exist_ok=True)
        
        # Modular components
        self.logger = MnemosLogger(self.log_file)
        self.analyzer = MnemosAnalyzer(self.log_file, self.reflection_file)
        self.compressor = MnemosCompressor(self.log_file)
        self.memory_manager = AutoCompressionIntegration(self.log_file, self.compressor)
        self.patterns = BehavioralPatterns(self.log_file)
        self.surface = MemorySurface(self.log_file)
    
    def _find_mnemos_root(self):
        """Git-linked memory: .mnemos alongside .git for natural project boundaries"""
        current = Path.cwd()
        
        # Search upward for .git directory
        for parent in [current] + list(current.parents):
            if (parent / '.git').exists():
                # Create .mnemos alongside .git
                mnemos_dir = parent / '.mnemos'
                return str(mnemos_dir), 'memory'
        
        # Security: Prevent context leakage - require git repo
        print("❌ MNEMOS ERROR: Not in a git repository")
        print("   Mnemos requires a git repo to prevent context leakage between projects")
        print("   Navigate to a git repository or run 'git init' to create one")
        sys.exit(1)
    
    def _post_write_hook(self):
        """Invisible auto-compression after memory writes - biological memory management."""
        try:
            result = self.memory_manager.post_write_hook()
            if result and result.get("auto_compression") and result.get("status") == "reversible_compression":
                # Subtle notification - don't interrupt flow
                print(f"🧠 Memory consolidated: {result['original_count']} → {result['compressed_count']} entries")
        except Exception:
            # Silent failure - don't break user flow
            pass
    
    # Delegate to modular components with auto-compression
    def observation(self, what: str, context: str = ""):
        """Log raw findings - what you see."""
        result = self.logger.observation(what, context)
        self._post_write_hook()
        return result
    
    def discovery(self, breakthrough: str, impact: str, solution: str = ""):
        """Log major discoveries that change everything."""
        result = self.logger.discovery(breakthrough, impact, solution)
        self._post_write_hook()
        return result
    
    def insight(self, understanding: str, evidence: str = ""):
        """Log analyzed understanding - what observations mean."""
        result = self.logger.insight(understanding, evidence)
        self._post_write_hook()
        return result
    
    def issue(self, problem: str, location: str, severity: str = "medium"):
        """Log discovered issues."""
        result = self.logger.issue(problem, location, severity)
        self._post_write_hook()
        return result
    
    def resolve(self, issue_id: str, solution: str):
        """Resolve an existing issue by ID."""
        result = self.logger.resolve(issue_id, solution)
        self._post_write_hook()
        return result
    
    def consideration(self, idea: str, context: str = ""):
        """Log future considerations - ideas to evaluate later, not actionable tasks."""
        result = self.logger.consideration(idea, context)
        self._post_write_hook()
        return result
    
    # Strategic memory methods
    def pattern(self, insight: str, value: str):
        """Log architectural patterns that persist across projects."""
        result = self.logger.pattern(insight, value)
        self._post_write_hook()
        return result
    
    def principle(self, rule: str, rationale: str):
        """Log design principles and rules."""
        result = self.logger.principle(rule, rationale)
        self._post_write_hook()
        return result
    
    def antipattern(self, problem: str, why_bad: str):
        """Log things to avoid and why."""
        result = self.logger.antipattern(problem, why_bad)
        self._post_write_hook()
        return result
    
    def thread(self, name: str, status: str = "active"):
        """Track investigation threads."""
        result = self.logger.thread(name, status)
        self._post_write_hook()
        return result
    
    def meta_reflect(self, trigger_count: int = 10):
        """Delegate to analyzer."""
        return self.analyzer.meta_reflect(trigger_count)
    
    def compress_findings(self, keep_recent: int = 15):
        """Manual compression using biological memory system."""
        return self.memory_manager.manual_compress(keep_recent)
    
    def archive_findings(self, archive_filter: str = None, older_than_hours: int = None):
        """Archive irrelevant findings permanently - beyond compression."""
        return self.compressor.archive_findings(archive_filter, older_than_hours)
    
    def delete_findings(self, delete_filter: str = None, entry_ids: list = None):
        """Permanently delete specific findings - use with caution.""" 
        return self.compressor.delete_findings(delete_filter, entry_ids)

    def decompress_findings(self, compression_id: int):
        """Recover compressed findings by ID - reversible compression."""
        return self.compressor.decompress_findings(compression_id)
    
    def list_compressions(self):
        """List available compression archives for recovery."""
        return self.compressor.list_compressions()
    
    def memory_health(self):
        """Get biological memory system health status."""
        return self.memory_manager.memory_status()

    def undo(self):
        """Delegate to logger."""
        return self.logger.undo()

    def summarize(self):
        """Delegate to analyzer."""
        return self.analyzer.summarize()
    
    def protocol(self):
        """Return full investigation protocol for Claude."""
        return PROTOCOL
    
    def methodology(self):
        """Return investigation methodology reference."""
        return METHODOLOGY
    
    def boundaries(self):
        """Return operational boundaries for autonomous work."""
        return BOUNDARIES
    
    def search(self, term: str, search_type: str = None, limit: int = 10, show_breadcrumbs: bool = True):
        """Search investigation history with behavioral breadcrumbs."""
        # Track this search for pattern analysis
        self.patterns.track_search(term)
        
        # Get search results
        results = self.logger.search(term, search_type, limit)
        
        if show_breadcrumbs and results:
            # Show cognitive breadcrumbs
            breadcrumbs = self.patterns.get_search_breadcrumbs(term)
            if breadcrumbs:
                print(f"🧭 Related searches: {', '.join(breadcrumbs)}")
        
        return results
    
    def investigation_patterns(self):
        """Show Claude's investigation patterns and cognitive breadcrumbs."""
        patterns = {
            'flows': self.patterns.get_investigation_flows(),
            'locations': self.patterns.get_location_clusters(),
            'successful': self.patterns.get_successful_patterns()
        }
        
        print("🧠 CLAUDE'S INVESTIGATION PATTERNS")
        print("=" * 40)
        
        if patterns['flows']:
            print("📈 Common Investigation Flows:")
            for i, flow in enumerate(patterns['flows'], 1):
                print(f"  {i}. {flow['pattern']} (used {flow['count']} times)")
        
        if patterns['locations']:
            print("\n🗺️ Issue Hotspots:")
            for loc in patterns['locations']:
                print(f"  • {loc['location']}: {loc['issue_count']} issues")
        
        if patterns['successful']:
            print("\n✅ Recent Successful Patterns:")
            for pattern in patterns['successful'][-3:]:
                print(f"  • {pattern['pattern']} → {pattern['outcome'].get('type', 'success')}")
        
        return patterns
    
    def momentum(self):
        """Show investigation momentum suggestions based on behavioral patterns."""
        suggestions = self.patterns.get_momentum_suggestions()
        
        if not suggestions:
            print("🚀 No momentum patterns detected yet. Continue investigating to build behavioral data!")
            return []
        
        print("🚀 INVESTIGATION MOMENTUM SUGGESTIONS")
        print("=" * 40)
        print("Based on your historical patterns, consider investigating:")
        print()
        
        for i, suggestion in enumerate(suggestions, 1):
            confidence_emoji = "🔥" if suggestion['confidence'] > 0.7 else "⚡" if suggestion['confidence'] > 0.4 else "💡"
            print(f"{confidence_emoji} {i}. {suggestion['suggestion']}")
            print(f"   {suggestion['rationale']}")
            print(f"   Confidence: {suggestion['confidence']:.0%} | Frequency: {suggestion['frequency']}x")
            print()
        
        return suggestions
    
    def surface_memory(self, context: str = None) -> Dict[str, Any]:
        """Proactively surface relevant memory based on current investigation context."""
        result = self.surface.surface_relevant_memory(context)
        
        if result['status'] == 'surfaced':
            print("🧠 SMART MEMORY SURFACING")
            print("=" * 30)
            
            # Show proactive insights first
            if result['proactive_insights']:
                print("💡 PROACTIVE INSIGHTS:")
                for insight in result['proactive_insights']:
                    print(f"   {insight}")
                print()
            
            # Show relevant findings
            if result['relevant_findings']:
                print(f"📚 RELEVANT MEMORY ({len(result['relevant_findings'])} findings):")
                for i, finding in enumerate(result['relevant_findings'], 1):
                    entry = finding['entry']
                    entry_type = entry.get('type', 'unknown')
                    timestamp = entry.get('timestamp', 'unknown')
                    relevance = finding['relevance_score']
                    
                    # Type-specific content extraction
                    content = ""
                    if entry_type == 'discovery':
                        content = entry.get('breakthrough', '')[:60]
                    elif entry_type == 'insight':
                        content = entry.get('understanding', '')[:60] 
                    elif entry_type == 'observation':
                        content = entry.get('what', '')[:60]
                    elif entry_type == 'issue':
                        content = entry.get('problem', '')[:60]
                    elif entry_type == 'resolved':
                        content = entry.get('solution', '')[:60]
                    elif entry_type == 'pattern':
                        content = entry.get('insight', '')[:60]
                    else:
                        # Generic fallback
                        for field in ['what', 'understanding', 'breakthrough', 'problem', 'idea']:
                            if field in entry:
                                content = entry[field][:60]
                                break
                    
                    # Format with emoji
                    type_emoji = {
                        'discovery': '🎯', 'insight': '💡', 'observation': '👁️',
                        'issue': '🐛', 'resolved': '✅', 'pattern': '🏗️',
                        'principle': '📏', 'consideration': '💭'
                    }.get(entry_type, '📄')
                    
                    print(f"   {type_emoji} [{entry.get('id', 'unknown')[:8]}] {content}{'...' if len(content) >= 60 else ''}")
                    print(f"     Relevance: {relevance:.0%} | {timestamp}")
                    
                    # Show top relevance reason
                    if finding['relevance_reasons']:
                        print(f"     Why: {finding['relevance_reasons'][0]}")
                    print()
            
            confidence = result['surfacing_confidence']
            confidence_emoji = "🔥" if confidence > 0.7 else "⚡" if confidence > 0.4 else "💡"
            print(f"{confidence_emoji} Surfacing confidence: {confidence:.0%}")
            
        elif result['status'] == 'no_relevant_memory':
            print("🧠 No relevant memory surfaced - investigating uncharted territory!")
        else:
            print("🧠 Insufficient memory for smart surfacing - continue investigating to build context")
        
        return result
    
    def surface_for_entry(self, entry_type: str, content: str) -> List[Dict[str, Any]]:
        """Surface memory relevant to a specific entry being created."""
        relevant = self.surface.surface_for_entry_type(entry_type, content)
        
        if relevant:
            print(f"🔗 CONTEXTUAL MEMORY ({len(relevant)} related findings):")
            for finding in relevant:
                entry = finding['entry']
                similarity = finding['similarity']
                reason = finding['relevance_reason']
                
                # Brief display
                entry_id = entry.get('id', 'unknown')[:8]
                entry_content = ""
                if entry.get('type') == 'discovery':
                    entry_content = entry.get('breakthrough', '')[:40]
                elif entry.get('type') == 'insight':
                    entry_content = entry.get('understanding', '')[:40]
                elif entry.get('type') == 'observation':
                    entry_content = entry.get('what', '')[:40]
                
                print(f"   📎 [{entry_id}] {entry_content}{'...' if len(entry_content) >= 40 else ''}")
                print(f"      {reason} (similarity: {similarity:.0%})")
        
        return relevant
    
    def init(self):
        """Initialize Claude with full mnemos context and current status."""
        status = self.summarize()
        status_text = f"Findings: {status['total_findings']}, Recent: {status['recent_issues']} issues, {status['recent_discoveries']} discoveries"
        if status['active_threads']:
            status_text += f", Active threads: {', '.join(status['active_threads'])}"
        return INIT_MESSAGE.format(status=status_text)


def main():
    """Interactive Mnemos core session with autonomous guidance."""
    mnemos = Mnemos()
    
    print("🤖 Mnemos - Human-Like Investigation")
    print("=" * 40)
    
    summary = mnemos.summarize()
    print(f"Recent issues: {summary['recent_issues']}")
    print(f"Recent discoveries: {summary['recent_discoveries']}")
    
    if summary['active_threads']:
        print(f"Active threads: {', '.join(summary['active_threads'])}")
    
    if summary['last_discovery']:
        last = summary['last_discovery']
        print(f"Last discovery: {last['breakthrough']}")
    
    # DYNAMIC INVESTIGATION SUGGESTIONS
    print(f"\n🎯 INVESTIGATION OPTIONS:")
    
    suggestion_count = 1
    
    if summary['reflection_due']:
        print(f"{suggestion_count}. Meta-analysis: mnemos.meta_reflect() - {summary['total_findings']} findings ready")
        suggestion_count += 1
    
    if summary['active_threads']:
        print(f"{suggestion_count}. Continue active threads: {', '.join(summary['active_threads'])}")
        suggestion_count += 1
    
    if summary['recent_discoveries']:
        print(f"{suggestion_count}. Validate recent fixes - test in real scenarios")
        suggestion_count += 1
    
    if summary['recent_issues']:
        print(f"{suggestion_count}. Investigate issue patterns - check for related problems")
        suggestion_count += 1
    
    print(f"{suggestion_count}. Start new investigation - follow curiosity")
    
    print(f"\n💡 Methods: mnemos.observation(), mnemos.insight(), mnemos.discovery(), mnemos.issue(), mnemos.thread()")
    print("🔍 Begin autonomous discovery!")
    
    return mnemos


if __name__ == "__main__":
    main()