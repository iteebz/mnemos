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
from .protocols import PROTOCOL, METHODOLOGY, BOUNDARIES, INIT_MESSAGE


class Mnemos:
    """Modular autonomous investigation core - clean separation of concerns."""
    
    def __init__(self):
        # Unified investigation memory for polyrepo monoworkspaces
        mnemos_home = os.environ.get('MNEMOS_HOME', '.mnemos')
        self.mnemos_dir = Path(mnemos_home)
        self.log_file = self.mnemos_dir / "mnemos.jsonl"
        self.reflection_file = self.mnemos_dir / "reflections.jsonl"
        self.mnemos_dir.mkdir(parents=True, exist_ok=True)
        
        # Modular components
        self.logger = MnemosLogger(self.log_file)
        self.analyzer = MnemosAnalyzer(self.log_file, self.reflection_file)
        self.compressor = MnemosCompressor(self.log_file)
    
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
        """Mark issue as resolved with explicit ID linking."""
        return self.logger.resolve(issue_id, solution)
    
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