#!/usr/bin/env python3
"""Beautiful CLI interface for mnemos - Claude-optimized investigation commands."""

# DEPRECATED: This file is being migrated to modular CLI components
# New implementation: src/mnemos/cli/

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
        # Auto-initialize with full context - perfect Claude entry point
        auto_initialize()
        return
    
    # Check for flags
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    if verbose:
        sys.argv = [arg for arg in sys.argv if arg not in ['--verbose', '-v']]
    
    # Handle help flag
    if '--help' in sys.argv or '-h' in sys.argv:
        show_help()
        return
    
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
        if result['status'] == 'reversible_compression':
            print(f"🗜️  Reversible compression complete:")
            print(f"   Preserved: {result['preserved_discoveries']} discoveries, {result['preserved_patterns']} patterns")
            print(f"   Compressed: {result['compressed_routine']} routine findings")
            print(f"   Total: {result['original_count']} → {result['compressed_count']} entries")
            print(f"   Recovery: mnemos decompress {result['compression_id']}")
        elif result['status'] == 'semantic_compression':
            print(f"🗜️  Semantic compression complete:")
            print(f"   Preserved: {result['preserved_discoveries']} discoveries, {result['preserved_patterns']} patterns")
            print(f"   Compressed: {result['compressed_routine']} routine findings")
            print(f"   Total: {result['original_count']} → {result['compressed_count']} entries")
        else:
            print(f"🗜️  {result['status']}: {result.get('count', 0)} findings")
    
    elif command in ['archive']:
        if len(sys.argv) < 3:
            print("Usage: mnemos archive <filter> [--older-than-hours N]")
            print("Example: mnemos archive \"test\" --older-than-hours 24")
            return
        
        archive_filter = sys.argv[2]
        older_than_hours = None
        
        # Parse optional --older-than-hours flag
        if '--older-than-hours' in sys.argv:
            idx = sys.argv.index('--older-than-hours')
            if idx + 1 < len(sys.argv):
                older_than_hours = int(sys.argv[idx + 1])
        
        result = mnemos.archive_findings(archive_filter, older_than_hours)
        if result['status'] == 'archived':
            print(f"📦 Archive complete:")
            print(f"   Archived: {result['archived_count']} findings")
            print(f"   Remaining: {result['remaining_count']} findings")
            print(f"   Archive file: {result['archive_file']}")
        else:
            print(f"📦 {result['status']}: {result.get('count', 0)} findings")
    
    elif command in ['delete']:
        if len(sys.argv) < 3:
            print("Usage: mnemos delete <filter|id1,id2,...>")
            print("⚠️  WARNING: Permanent deletion! Use archive for safer removal.")
            return
        
        delete_arg = sys.argv[2]
        
        # Check if it's comma-separated IDs or a filter
        if ',' in delete_arg:
            entry_ids = [id.strip() for id in delete_arg.split(',')]
            result = mnemos.delete_findings(entry_ids=entry_ids)
        else:
            result = mnemos.delete_findings(delete_filter=delete_arg)
        
        if result['status'] == 'deleted':
            print(f"🗑️  Deletion complete:")
            print(f"   Deleted: {result['deleted_count']} findings")
            print(f"   Remaining: {result['remaining_count']} findings")
            print(f"   Backup: {result['backup_file']}")
        else:
            print(f"🗑️  {result['status']}: {result.get('count', 0)} findings")
    
    elif command in ['decompress', 'recover']:
        if len(sys.argv) < 3:
            print("Usage: mnemos decompress <compression_id>")
            print("       mnemos list-compressions  # Show available archives")
            return
        
        try:
            compression_id = int(sys.argv[2])
            result = mnemos.decompress_findings(compression_id)
            
            if result['status'] == 'decompressed':
                print(f"📈 Decompression complete:")
                print(f"   Recovered: {result['recovered_count']} findings")
                print(f"   Total memory: {result['total_count']} entries")
                print(f"   Backup: {result['backup_created']}")
            else:
                print(f"📈 {result['status']}: compression_id {result.get('compression_id', 'unknown')}")
        except ValueError:
            print("❌ Invalid compression ID - must be a number")
    
    elif command in ['list-compressions', 'compressions']:
        compressions = mnemos.list_compressions()
        if not compressions:
            print("📦 No compression archives found")
        else:
            print(f"📦 COMPRESSION ARCHIVES ({len(compressions)} available)")
            print("=" * 50)
            for comp in compressions:
                print(f"  ID: {comp['compression_id']} | {comp['timestamp']} | {comp['compressed_count']} findings")
                print(f"      Recovery: mnemos decompress {comp['compression_id']}")
                print()
    
    elif command in ['health', 'memory-health']:
        health = mnemos.memory_health()
        state = health['memory_state']
        rec = health['compression_recommendation']
        
        print(f"🧠 BIOLOGICAL MEMORY HEALTH")
        print("=" * 30)
        print(f"📊 Status: {health['health'].upper()}")
        print(f"📈 Entries: {state['total_entries']} ({state['pressure_level']} pressure)")
        print(f"🎯 Discoveries: {state['discoveries']}")
        print(f"🏗️  Patterns: {state['patterns']}")
        print(f"🐛 Open Issues: {state['unresolved_issues']}")
        print()
        
        if rec['should_compress']:
            print(f"💡 RECOMMENDATION: {rec['trigger_description']}")
            print(f"   Command: mnemos compress  # Will keep {rec['keep_recent']} recent entries")
        else:
            print(f"✅ No compression needed - memory pressure within healthy limits")
        
    elif command in ['?', 'next', 'suggest']:
        show_suggestions(mnemos)
        
    elif command in ['momentum', 'flow']:
        suggestions = mnemos.momentum()
        # Output already handled by momentum() method
        
    elif command in ['search', 'find', 'query']:
        if len(sys.argv) < 3:
            print("Usage: mnemos search <term> [--type TYPE] [--limit N]")
            return
        
        search_term = sys.argv[2]
        search_type = None
        limit = 10
        
        # Parse optional flags
        for i, arg in enumerate(sys.argv[3:], start=3):
            if arg == '--type' and i + 1 < len(sys.argv):
                search_type = sys.argv[i + 1]
            elif arg == '--limit' and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
        
        results = mnemos.search(search_term, search_type, limit)
        show_search_results(results, search_term)
        
    elif command in ['init']:
        # Redirect to auto-initialize for consistency
        auto_initialize()
        
    elif command in ['undo']:
        if mnemos.undo():
            print("⏪ UNDO: Last entry removed")
        else:
            print("❌ UNDO: No entries to remove")
        
    else:
        # Unknown command - show auto-initialize instead of help
        print(f"❓ Unknown command '{command}' - showing mnemos overview:")
        print()
        auto_initialize()


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


def auto_initialize():
    """Perfect Claude entry point - auto-initialize with full context and suggestions."""
    mnemos = Mnemos()
    
    print("🧠 MNEMOS - Autonomous Investigation System")
    print("=" * 45)
    
    # Show current investigation context
    show_rich_summary(mnemos)
    
    # Show momentum suggestions
    print("\n🚀 MOMENTUM SUGGESTIONS")
    print("-" * 25)
    suggestions = mnemos.momentum()
    
    if not suggestions:
        print("🔄 Building behavioral patterns... Continue investigating to unlock momentum suggestions!")
    
    print("\n💡 ESSENTIAL COMMANDS")
    print("-" * 20)
    print("  mnemos o \"observation\"     Log what you see")
    print("  mnemos i \"insight\"         Log what it means")
    print("  mnemos d \"discovery\"       Log breakthrough")
    print("  mnemos x \"problem\"         Log issue/bug")
    print("  mnemos r <id> \"solution\"   Resolve issue")
    print("  mnemos search \"term\"       Search memory")
    print("  mnemos momentum            Get next suggestions")
    
    print("\n🎯 Ready for autonomous investigation!")


def show_help():
    """Show comprehensive help for mnemos CLI."""
    print("🧠 MNEMOS - Autonomous Investigation System")
    print("=" * 45)
    print()
    print("QUICK COMMANDS (Claude-optimized):")
    print("  mnemos o \"observation\"     Log what you see")
    print("  mnemos i \"insight\"         Log what it means") 
    print("  mnemos d \"discovery\"       Log breakthrough")
    print("  mnemos x \"problem\"         Log issue/bug")
    print("  mnemos r <id> \"solution\"   Resolve issue")
    print("  mnemos c \"idea\"            Log consideration")
    print("  mnemos undo                Remove last entry")
    print()
    print("INVESTIGATION FLOW:")
    print("  mnemos start \"topic\"       Begin investigation thread")
    print("  mnemos done \"topic\"        Complete investigation thread")
    print("  mnemos status              Show investigation overview")
    print("  mnemos search \"term\"       Search memory")
    print("  mnemos momentum            Get suggestions based on patterns")
    print()
    print("MEMORY MANAGEMENT:")
    print("  mnemos reflect             Run meta-analysis")
    print("  mnemos compress            Reversible semantic compression")
    print("  mnemos decompress <id>     Recover compressed findings")
    print("  mnemos list-compressions   Show available compression archives")
    print("  mnemos health              Show biological memory system status")
    print("  mnemos archive <filter>    Archive irrelevant findings")
    print("  mnemos delete <filter>     Permanently delete findings (⚠️ caution)")
    print()
    print("STRATEGIC MEMORY:")
    print("  mnemos pattern \"insight\"   Log architectural pattern")
    print("  mnemos principle \"rule\"    Log design principle")
    print("  mnemos antipattern \"bad\"   Log what to avoid")
    print()
    print("FLAGS:")
    print("  --verbose, -v              Show memory locations")
    print("  --help, -h                 Show this help")
    print()
    print("CHAINED COMMANDS:")
    print("  mnemos 'o:saw bug' 'i:memory leak' 'd:root cause found'")
    print()
    print("🎯 Run 'mnemos' without arguments for auto-initialize with context")


def show_search_results(results, search_term):
    """Display search results with beautiful formatting."""
    if not results:
        print(f"🔍 No results found for '{search_term}'")
        return
    
    print(f"\n🔍 SEARCH RESULTS: '{search_term}' ({len(results)} matches)")
    print("=" * 50)
    
    for result in results:
        entry_type = result.get('type', 'unknown')
        timestamp = result.get('timestamp', 'unknown')
        entry_id = result.get('id', 'unknown')
        
        # Type-specific formatting
        if entry_type == 'observation':
            what = result.get('what', '')[:70]
            print(f"👁️  [{entry_id}] {timestamp} | {what}{'...' if len(result.get('what', '')) > 70 else ''}")
        elif entry_type == 'insight':
            understanding = result.get('understanding', '')[:70]
            print(f"💡 [{entry_id}] {timestamp} | {understanding}{'...' if len(result.get('understanding', '')) > 70 else ''}")
        elif entry_type == 'discovery':
            breakthrough = result.get('breakthrough', '')[:70]
            print(f"🎯 [{entry_id}] {timestamp} | {breakthrough}{'...' if len(result.get('breakthrough', '')) > 70 else ''}")
        elif entry_type == 'issue':
            problem = result.get('problem', '')[:70]
            status = result.get('status', 'unknown')
            print(f"🐛 [{entry_id}] {timestamp} | {status.upper()} | {problem}{'...' if len(result.get('problem', '')) > 70 else ''}")
        elif entry_type == 'consideration':
            idea = result.get('idea', '')[:70]
            print(f"💭 [{entry_id}] {timestamp} | {idea}{'...' if len(result.get('idea', '')) > 70 else ''}")
        else:
            # Generic fallback
            content = str(result)[:70]
            print(f"📄 [{entry_id}] {timestamp} | {content}{'...' if len(str(result)) > 70 else ''}")




if __name__ == "__main__":
    main()