"""Auto-initialization and rich summary for mnemos CLI."""

import json
from pathlib import Path
from typing import List, Dict

from ..core import Mnemos
from .formatters import OutputFormatter


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


def show_rich_summary(mnemos: Mnemos):
    """Show semantically rich investigation overview for fresh Claude instances."""
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
    
    print(OutputFormatter.rich_summary(entries, len(entries)))


def show_suggestions(mnemos: Mnemos):
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