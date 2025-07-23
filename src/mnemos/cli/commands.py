"""Command handlers for mnemos CLI - beautiful, DRY, extensible."""

import sys
from typing import Dict, Callable, Any, List
from pathlib import Path

from ..core import Mnemos
from .formatters import OutputFormatter


class CommandRegistry:
    """Self-documenting command registry with zero ceremony."""
    
    def __init__(self):
        self.commands: Dict[str, Dict[str, Any]] = {}
        self.mnemos = Mnemos()
    
    def command(self, primary: str, aliases: List[str] = None, help_text: str = ""):
        """Decorator for registering commands with auto-documentation."""
        def decorator(func: Callable):
            all_names = [primary] + (aliases or [])
            cmd_info = {
                'handler': func,
                'primary': primary,
                'aliases': aliases or [],
                'help': help_text,
                'all_names': all_names
            }
            
            for name in all_names:
                self.commands[name] = cmd_info
            
            return func
        return decorator
    
    def execute(self, command: str, args: List[str]) -> bool:
        """Execute command if registered, return True if handled."""
        if command in self.commands:
            cmd_info = self.commands[command]
            try:
                cmd_info['handler'](args)
                return True
            except Exception as e:
                print(f"❌ Command failed: {e}")
                return True
        return False
    
    def get_help(self) -> str:
        """Generate beautiful help from registered commands."""
        output = [
            "🧠 MNEMOS - Autonomous Investigation System", 
            "=" * 45,
            "",
            "QUICK COMMANDS (Claude-optimized):"
        ]
        
        # Group commands by category
        quick_commands = []
        flow_commands = []
        memory_commands = []
        strategic_commands = []
        
        seen_primaries = set()
        for cmd_info in self.commands.values():
            primary = cmd_info['primary']
            if primary in seen_primaries:
                continue
            seen_primaries.add(primary)
            
            aliases_str = f" | {' | '.join(cmd_info['aliases'])}" if cmd_info['aliases'] else ""
            cmd_line = f"  mnemos {primary}{aliases_str}"
            help_line = f"{cmd_line:<25} {cmd_info['help']}"
            
            # Categorize commands
            if primary in ['o', 'i', 'd', 'x', 'r', 'c', 'undo']:
                quick_commands.append(help_line)
            elif primary in ['start', 'done', 'status', 'search', 'momentum']:
                flow_commands.append(help_line)
            elif primary in ['reflect', 'compress', 'decompress', 'health', 'archive', 'delete']:
                memory_commands.append(help_line)
            elif primary in ['pattern', 'principle', 'antipattern']:
                strategic_commands.append(help_line)
        
        output.extend(quick_commands)
        output.extend(["", "INVESTIGATION FLOW:"] + flow_commands)
        output.extend(["", "MEMORY MANAGEMENT:"] + memory_commands)
        output.extend(["", "STRATEGIC MEMORY:"] + strategic_commands)
        
        output.extend([
            "",
            "FLAGS:",
            "  --verbose, -v              Show memory locations",
            "  --help, -h                 Show this help",
            "",
            "🎯 Run 'mnemos' without arguments for auto-initialize with context"
        ])
        
        return "\n".join(output)


# Global command registry
registry = CommandRegistry()


@registry.command('o', aliases=['obs', 'observation'], help_text="Log what you see")
def observation_cmd(args: List[str]):
    what = ' '.join(args) if args else input("What did you observe? ")
    result_id = registry.mnemos.observation(what)
    print(OutputFormatter.log_success("observation", result_id))


@registry.command('i', aliases=['insight'], help_text="Log what it means")
def insight_cmd(args: List[str]):
    understanding = ' '.join(args) if args else input("What insight? ")
    result_id = registry.mnemos.insight(understanding)
    print(OutputFormatter.log_success("insight", result_id))


@registry.command('d', aliases=['discovery'], help_text="Log breakthrough")
def discovery_cmd(args: List[str]):
    breakthrough = ' '.join(args) if args else input("What breakthrough? ")
    impact = input("Impact: ") if not args else ""
    result_id = registry.mnemos.discovery(breakthrough, impact)
    print(OutputFormatter.log_success("discovery", result_id))


@registry.command('x', aliases=['issue'], help_text="Log issue/bug")
def issue_cmd(args: List[str]):
    problem = ' '.join(args) if args else input("What problem? ")
    location = input("Location: ") if not args else "unknown"
    result_id = registry.mnemos.issue(problem, location)
    print(OutputFormatter.log_success("issue", result_id))


@registry.command('r', aliases=['resolve'], help_text="Resolve issue by ID")
def resolve_cmd(args: List[str]):
    if len(args) < 2:
        print("Usage: mnemos resolve <issue_id> <solution>")
        return
    
    issue_id = args[0]
    solution = ' '.join(args[1:]) if len(args) > 1 else input("Solution: ")
    result_id = registry.mnemos.resolve(issue_id, solution)
    print(OutputFormatter.log_success("resolved", result_id))


@registry.command('c', aliases=['consider', 'consideration'], help_text="Log consideration")
def consideration_cmd(args: List[str]):
    idea = ' '.join(args) if args else input("Consideration: ")
    result_id = registry.mnemos.consideration(idea)
    print(OutputFormatter.log_success("consideration", result_id))


@registry.command('pattern', help_text="Log architectural pattern") 
def pattern_cmd(args: List[str]):
    insight = ' '.join(args) if args else input("Pattern insight: ")
    value = input("Value: ") if not args else ""
    result_id = registry.mnemos.pattern(insight, value)
    print(OutputFormatter.log_success("pattern", result_id))


@registry.command('principle', help_text="Log design principle")
def principle_cmd(args: List[str]):
    rule = ' '.join(args) if args else input("Principle: ")
    rationale = input("Rationale: ") if not args else ""
    result_id = registry.mnemos.principle(rule, rationale)
    print(OutputFormatter.log_success("principle", result_id))


@registry.command('antipattern', help_text="Log what to avoid")
def antipattern_cmd(args: List[str]):
    problem = ' '.join(args) if args else input("Antipattern: ")
    why_bad = input("Why bad: ") if not args else ""
    result_id = registry.mnemos.antipattern(problem, why_bad)
    print(OutputFormatter.log_success("antipattern", result_id))


@registry.command('start', aliases=['thread'], help_text="Begin investigation thread")
def start_cmd(args: List[str]):
    name = ' '.join(args) if args else input("Thread name: ")
    registry.mnemos.thread(name, "active")
    print(f"Started thread: {name}")


@registry.command('done', aliases=['complete'], help_text="Complete investigation thread")
def done_cmd(args: List[str]):
    name = ' '.join(args) if args else input("Thread name: ")
    registry.mnemos.thread(name, "completed")
    print(f"Completed thread: {name}")


@registry.command('status', aliases=['summary'], help_text="Show investigation overview")
def status_cmd(args: List[str]):
    from .auto_init import show_rich_summary
    show_rich_summary(registry.mnemos)


@registry.command('search', aliases=['find', 'query'], help_text="Search memory")
def search_cmd(args: List[str]):
    if not args:
        print("Usage: mnemos search <term> [--type TYPE] [--limit N]")
        return
    
    search_term = args[0]
    search_type = None
    limit = 10
    
    # Parse optional flags
    for i, arg in enumerate(args[1:], start=1):
        if arg == '--type' and i + 1 < len(args):
            search_type = args[i + 1]
        elif arg == '--limit' and i + 1 < len(args):
            limit = int(args[i + 1])
    
    results = registry.mnemos.search(search_term, search_type, limit)
    print(OutputFormatter.search_results(results, search_term))


@registry.command('momentum', aliases=['flow'], help_text="Get suggestions based on patterns")
def momentum_cmd(args: List[str]):
    registry.mnemos.momentum()  # Output handled by momentum() method


@registry.command('reflect', aliases=['meta'], help_text="Run meta-analysis")
def reflect_cmd(args: List[str]):
    reflection = registry.mnemos.meta_reflect()
    print(f"🧠 Meta-reflection complete: {reflection.get('findings_analyzed', 0)} findings analyzed")


@registry.command('compress', help_text="Reversible semantic compression")
def compress_cmd(args: List[str]):
    result = registry.mnemos.compress_findings()
    print(OutputFormatter.compression_result(result))


@registry.command('health', aliases=['memory-health'], help_text="Show biological memory system status")
def health_cmd(args: List[str]):
    health = registry.mnemos.memory_health()
    print(OutputFormatter.memory_health(health))


@registry.command('undo', help_text="Remove last entry")
def undo_cmd(args: List[str]):
    if registry.mnemos.undo():
        print("⏪ UNDO: Last entry removed")
    else:
        print("❌ UNDO: No entries to remove")


@registry.command('surface', aliases=['smart', 'brain'], help_text="Smart memory surfacing - proactive context")
def surface_cmd(args: List[str]):
    context = ' '.join(args) if args else None
    registry.mnemos.surface_memory(context)


@registry.command('?', aliases=['suggest', 'next'], help_text="Investigation suggestions")
def suggest_cmd(args: List[str]):
    # First show smart memory surfacing
    registry.mnemos.surface_memory()
    print()
    
    # Then show momentum suggestions
    registry.mnemos.momentum()


def process_chained_commands(chain_args: List[str]) -> bool:
    """Process chained commands like 'o:observation' 'i:insight' 'd:discovery'."""
    results = []
    
    for arg in chain_args:
        if ':' not in arg:
            continue
            
        cmd_type, content = arg.split(':', 1)
        cmd_type = cmd_type.lower()
        
        if cmd_type in ['o', 'obs', 'observation']:
            result_id = registry.mnemos.observation(content)
            results.append(f"👁️  {result_id}")
        elif cmd_type in ['i', 'insight']:
            result_id = registry.mnemos.insight(content)
            results.append(f"💡 {result_id}")
        elif cmd_type in ['d', 'discovery']:
            result_id = registry.mnemos.discovery(content, "")
            results.append(f"🎯 {result_id}")
        elif cmd_type in ['x', 'issue']:
            result_id = registry.mnemos.issue(content, "unknown")
            results.append(f"🐛 {result_id}")
        elif cmd_type in ['c', 'consideration']:
            result_id = registry.mnemos.consideration(content)
            results.append(f"💭 {result_id}")
        elif cmd_type == 'pattern':
            result_id = registry.mnemos.pattern(content, "")
            results.append(f"🏗️  {result_id}")
        elif cmd_type == 'principle':
            result_id = registry.mnemos.principle(content, "")
            results.append(f"📏 {result_id}")
        elif cmd_type == 'antipattern':
            result_id = registry.mnemos.antipattern(content, "")
            results.append(f"🚫 {result_id}")
    
    if results:
        print(OutputFormatter.chained_results(results))
        return True
    
    return False