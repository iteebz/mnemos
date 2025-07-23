#!/usr/bin/env python3
"""Beautiful CLI interface for mnemos - Claude-optimized investigation commands."""

import sys
import argparse
from pathlib import Path

from .core import Mnemos


def process_chained_commands(mnemos, chain_args):
    """Process chained commands like 'o:observation' 'i:insight' 'd:discovery'."""
    results = []
    
    for arg in chain_args:
        if ':' not in arg:
            continue
            
        cmd_type, content = arg.split(':', 1)
        cmd_type = cmd_type.lower()
        
        if cmd_type in ['o', 'obs', 'observation']:
            result_id = mnemos.observation(content)
            results.append(f"👁️  {result_id}")
        elif cmd_type in ['i', 'insight']:
            result_id = mnemos.insight(content)
            results.append(f"💡 {result_id}")
        elif cmd_type in ['d', 'discovery']:
            result_id = mnemos.discovery(content, "")
            results.append(f"🎯 {result_id}")
        elif cmd_type in ['x', 'issue']:
            result_id = mnemos.issue(content, "unknown")
            results.append(f"🐛 {result_id}")
        elif cmd_type in ['c', 'consideration']:
            result_id = mnemos.consideration(content)
            results.append(f"💭 {result_id}")
        elif cmd_type == 'pattern':
            result_id = mnemos.pattern(content, "")
            results.append(f"🏗️  {result_id}")
        elif cmd_type == 'principle':
            result_id = mnemos.principle(content, "")
            results.append(f"📏 {result_id}")
        elif cmd_type == 'antipattern':
            result_id = mnemos.antipattern(content, "")
            results.append(f"🚫 {result_id}")
    
    if results:
        print(f"⚡ CHAINED: {' → '.join(results)}")


def main():
    """Claude-friendly mnemos CLI interface."""
    if len(sys.argv) < 2:
        show_help()
        return
    
    # Check for --verbose flag
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    if verbose:
        sys.argv = [arg for arg in sys.argv if arg not in ['--verbose', '-v']]
    
    mnemos = Mnemos()
    
    # Handle chained commands: mnemos 'o:observation' 'i:insight' 'd:discovery'
    if len(sys.argv) > 1 and ':' in sys.argv[1]:
        process_chained_commands(mnemos, sys.argv[1:])
        return
    
    command = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    
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
    
    elif command in ['c', 'consider', 'consideration']:
        idea = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else input("Consideration: ")
        result_id = mnemos.consideration(idea)
        print(f"Logged consideration: {result_id}")
    
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
        show_rich_summary(mnemos)
        
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


def show_rich_summary(mnemos):
    """Show semantically rich investigation overview for fresh Claude instances."""
    import json
    from pathlib import Path
    
    # Read raw memory for rich context
    log_file = Path(mnemos.log_file)
    if not log_file.exists():
        print("🤖 MNEMOS - No investigation memory found")
        return
    
    entries = []
    with open(log_file) as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    
    # Get recent entries (last 10)
    recent = entries[-10:] if len(entries) > 10 else entries
    
    print("\\n🧠 MNEMOS INVESTIGATION OVERVIEW")
    print("=" * 45)
    print(f"📊 Total memory: {len(entries)} entries")
    
    # Recent discoveries with content
    discoveries = [e for e in recent if e.get('type') == 'discovery']
    if discoveries:
        print("\\n🎯 RECENT DISCOVERIES:")
        for d in discoveries[-3:]:
            breakthrough = d.get('breakthrough', '')[:80]
            print(f"   • {breakthrough}{'...' if len(d.get('breakthrough', '')) > 80 else ''}")
    
    # Active issues
    issues = [e for e in entries if e.get('type') == 'issue']
    resolved_ids = {e.get('issue_id') for e in entries if e.get('type') == 'resolved'}
    active_issues = [i for i in issues if i.get('id') not in resolved_ids]
    
    if active_issues:
        print("\\n🐛 ACTIVE ISSUES:")
        for issue in active_issues[-3:]:
            problem = issue.get('problem', '')[:60]
            print(f"   • [{issue.get('id', 'unknown')}] {problem}")
    
    # Recent considerations (future ideas)
    considerations = [e for e in recent if e.get('type') == 'consideration']
    if considerations:
        print("\\n💭 RECENT CONSIDERATIONS:")
        for c in considerations[-3:]:
            idea = c.get('idea', '')[:70]
            print(f"   • {idea}{'...' if len(c.get('idea', '')) > 70 else ''}")
    
    # Investigation patterns
    patterns = [e for e in entries if e.get('type') == 'pattern']
    if patterns:
        print(f"\\n🏗️  PATTERNS DISCOVERED: {len(patterns)}")
        if patterns:
            latest = patterns[-1]
            insight = latest.get('insight', '')[:60]
            print(f"   Latest: {insight}{'...' if len(latest.get('insight', '')) > 60 else ''}")
    
    print(f"\\n⚡ Investigation velocity: {len(recent)} entries recently")
    print("\\n🎯 Ready for autonomous investigation!")


def show_suggestions(mnemos):
    """Show investigation suggestions for Claude."""
    summary = mnemos.summarize()
    print("\\n🎯 INVESTIGATION SUGGESTIONS")
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
  mnemos c "idea"            Future consideration

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
  x = issue, r = resolve, c = consideration, ? = suggest

FLAGS:
  --verbose, -v              Show memory locations

Claude-optimized for zero-ceremony autonomous investigation! 🔍

ENVIRONMENT:
  MNEMOS_HOME=~/workspace/.mnemos  # Unified polyrepo memory
  (defaults to local .mnemos)      # Per-project memory
""")


if __name__ == "__main__":
    main()