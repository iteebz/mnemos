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
from pathlib import Path
from typing import Dict, Any

from .logging import MnemosLogger  
from .analysis import MnemosAnalyzer
from .compression import MnemosCompressor
from .patterns import BehavioralPatterns
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
        self.patterns = BehavioralPatterns(self.log_file)
    
    def _find_mnemos_root(self):
        """Git-linked memory: .mnemos alongside .git for natural project boundaries"""
        current = Path.cwd()
        
        # Search upward for .git directory
        for parent in [current] + list(current.parents):
            if (parent / '.git').exists():
                # Create .mnemos alongside .git
                mnemos_dir = parent / '.mnemos'
                return str(mnemos_dir), 'memory'
        
        # Fallback to user home if no git repo found
        return str(Path.home() / '.mnemos'), 'global'
    
    # Delegate to modular components
    def observation(self, what: str, context: str = ""):
        """Log raw findings - what you see."""
        return self.logger.observation(what, context)
    
    def discovery(self, breakthrough: str, impact: str, solution: str = ""):
        """Log major discoveries that change everything."""
        return self.logger.discovery(breakthrough, impact, solution)
    
    def insight(self, understanding: str, evidence: str = ""):
        """Log analyzed understanding - what observations mean."""
        return self.logger.insight(understanding, evidence)
    
    def issue(self, problem: str, location: str, severity: str = "medium"):
        """Log discovered issues."""
        return self.logger.issue(problem, location, severity)
    
    def resolve(self, issue_id: str, solution: str):
        """Resolve an existing issue by ID."""
        return self.logger.resolve(issue_id, solution)
    
    def consideration(self, idea: str, context: str = ""):
        """Log future considerations - ideas to evaluate later, not actionable tasks."""
        return self.logger.consideration(idea, context)
    
    # Strategic memory methods
    def pattern(self, insight: str, value: str):
        """Log architectural patterns that persist across projects."""
        return self.logger.pattern(insight, value)
    
    def principle(self, rule: str, rationale: str):
        """Log design principles and rules."""
        return self.logger.principle(rule, rationale)
    
    def antipattern(self, problem: str, why_bad: str):
        """Log things to avoid and why."""
        return self.logger.antipattern(problem, why_bad)
    
    def thread(self, name: str, status: str = "active"):
        """Track investigation threads."""
        return self.logger.thread(name, status)
    
    def meta_reflect(self, trigger_count: int = 10):
        """Delegate to analyzer."""
        return self.analyzer.meta_reflect(trigger_count)
    
    def compress_findings(self, keep_recent: int = 15):
        """Delegate to compressor."""
        return self.compressor.compress_findings(keep_recent)

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