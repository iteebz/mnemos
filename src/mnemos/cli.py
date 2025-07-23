#!/usr/bin/env python3
"""Beautiful CLI interface for mnemos - Claude-optimized investigation commands."""

import sys
import argparse
from pathlib import Path

from .core import Mnemos


def main():
    """Claude-friendly mnemos CLI interface."""
    if len(sys.argv) < 2:
        show_help()
        return
    
    # Check for --verbose flag
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    if verbose:
        sys.argv = [arg for arg in sys.argv if arg not in ['--verbose', '-v']]
    
    command = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    mnemos = Mnemos()
    
    if verbose:
        import os
        mnemos_home = os.environ.get('MNEMOS_HOME', '.mnemos')
        print(f"💾 Memory location: {Path(mnemos_home).resolve()}")
        print(f"📁 Files: {mnemos.log_file}, {mnemos.reflection_file}")
        print()
    
    # Quick commands (Claude-optimized)
    if command in ['o', 'obs', 'observation']:
        what = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else input("What did you observe? ")
        result_id = mnemos.observation(what)
        print(f"Logged observation: {result_id}")
        
    elif command in ['i', 'insight']:
        understanding = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else input("What insight? ")
        result_id = mnemos.insight(understanding)
        print(f"Logged insight: {result_id}")
        
    elif command in ['d', 'discovery']:
        breakthrough = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else input("What breakthrough? ")
        impact = input("Impact: ") if len(sys.argv) <= 2 else ""
        result_id = mnemos.discovery(breakthrough, impact)
        print(f"Logged discovery: {result_id}")
    
    elif command in ['x', 'issue']:
        problem = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else input("What problem? ")
        location = input("Location: ") if len(sys.argv) <= 2 else "unknown"
        result_id = mnemos.issue(problem, location)
        print(f"Logged issue: {result_id}")
        
    elif command in ['r', 'resolve']:
        if len(sys.argv) < 3:
            print("Usage: mnemos resolve <issue_id> <solution>")
            return
        issue_id = sys.argv[2]
        solution = ' '.join(sys.argv[3:]) if len(sys.argv) > 3 else input("Solution: ")
        result_id = mnemos.resolve(issue_id, solution)
        print(f"Resolved issue: {result_id}")
        
    # Strategic commands
    elif command == 'pattern':
        insight = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else input("Pattern insight: ")
        value = input("Value: ") if len(sys.argv) <= 2 else ""
        result_id = mnemos.pattern(insight, value)
        print(f"Logged pattern: {result_id}")
        
    elif command == 'principle':
        rule = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else input("Principle: ")
        rationale = input("Rationale: ") if len(sys.argv) <= 2 else ""
        result_id = mnemos.principle(rule, rationale)
        print(f"Logged principle: {result_id}")
        
    elif command == 'antipattern':
        problem = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else input("Antipattern: ")
        why_bad = input("Why bad: ") if len(sys.argv) <= 2 else ""
        result_id = mnemos.antipattern(problem, why_bad)
        print(f"Logged antipattern: {result_id}")
    
    # Investigation management
    elif command in ['thread', 'start']:
        name = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else input("Thread name: ")
        status = "active"
        mnemos.thread(name, status)
        print(f"Started thread: {name}")
        
    elif command in ['done', 'complete']:
        name = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else input("Thread name: ")
        mnemos.thread(name, "completed")
        print(f"Completed thread: {name}")
        
    elif command in ['status', 'summary']:
        summary = mnemos.summarize()
        print("\n🤖 MNEMOS STATUS")
        print("=" * 30)
        print(f"Recent discoveries: {summary.get('recent_discoveries', 0)}")
        print(f"Recent issues: {summary.get('recent_issues', 0)}")
        if summary.get('active_threads'):
            print(f"Active threads: {', '.join(summary['active_threads'])}")
        
    elif command in ['reflect', 'meta']:
        reflection = mnemos.meta_reflect()
        print(f"🧠 Meta-reflection complete: {reflection.get('findings_analyzed', 0)} findings analyzed")
        
    elif command in ['compress']:
        result = mnemos.compress_findings()
        if result['status'] == 'semantic_compression':
            print(f"🗜️  Semantic compression complete:")
            print(f"   Preserved: {result['preserved_discoveries']} discoveries, {result['preserved_patterns']} patterns")
            print(f"   Compressed: {result['compressed_routine']} routine findings")
            print(f"   Total: {result['original_count']} → {result['compressed_count']} entries")
        else:
            print(f"🗜️  {result['status']}: {result.get('count', 0)} findings")
        
    elif command in ['?', 'next', 'suggest']:
        show_suggestions(mnemos)
        
    elif command in ['init']:
        init_message = mnemos.init()
        print(init_message)
        
    else:
        show_help()


def show_suggestions(mnemos):
    """Show investigation suggestions for Claude."""
    summary = mnemos.summarize()
    print("\n🎯 INVESTIGATION SUGGESTIONS")
    print("=" * 35)
    
    count = 1
    if summary.get('reflection_due'):
        print(f"{count}. Run meta-analysis: mnemos reflect")
        count += 1
    
    if summary.get('active_threads'):
        print(f"{count}. Continue threads: {', '.join(summary['active_threads'])}")
        count += 1
        
    if summary.get('recent_discoveries'):
        print(f"{count}. Validate recent discoveries")
        count += 1
        
    print(f"{count}. Start new investigation: mnemos start <topic>")


def show_help():
    """Show beautiful help for Claude."""
    print("""
🤖 MNEMOS - Beautiful Investigation CLI

TACTICAL INVESTIGATION:
  mnemos o "observation"     Log what you see
  mnemos i "insight"         Log what it means  
  mnemos d "discovery"       Log breakthrough
  mnemos x "problem"         Log issue/bug
  mnemos r <id> "solution"   Resolve issue

STRATEGIC MEMORY:
  mnemos pattern "insight"   Architectural pattern
  mnemos principle "rule"    Design principle
  mnemos antipattern "bad"   Thing to avoid

INVESTIGATION FLOW:
  mnemos start "topic"       Begin investigation
  mnemos done "topic"        Complete investigation  
  mnemos status              Show current state
  mnemos reflect             Meta-analysis
  mnemos compress            Semantic compression
  mnemos ?                   What to investigate next

ALIASES:
  o/obs = observation, i = insight, d = discovery
  x = issue, r = resolve, ? = suggest

FLAGS:
  --verbose, -v              Show memory locations

Claude-optimized for zero-ceremony autonomous investigation! 🔍

ENVIRONMENT:
  MNEMOS_HOME=~/workspace/.mnemos  # Unified polyrepo memory
  (defaults to local .mnemos)      # Per-project memory
""")


if __name__ == "__main__":
    main()