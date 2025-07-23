"""Main CLI entry point - beautiful, modular, world-class."""

import sys
from pathlib import Path

from .commands import registry, process_chained_commands
from .auto_init import auto_initialize


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
        print(registry.get_help())
        return
    
    # Handle chained commands: mnemos 'o:observation' 'i:insight' 'd:discovery'
    if len(sys.argv) > 1 and ':' in sys.argv[1]:
        process_chained_commands(sys.argv[1:])
        return
    
    command = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    if verbose:
        import os
        from ..core import Mnemos
        mnemos = Mnemos()
        mnemos_home = os.environ.get('MNEMOS_HOME', '.mnemos')
        print(f"💾 Memory location: {Path(mnemos_home).resolve()}")
        print(f"📁 Files: {mnemos.log_file}, {mnemos.reflection_file}")
        print()
    
    # Try registered commands first
    if registry.execute(command, args):
        return
    
    # Special commands that need custom handling
    if command in ['init']:
        auto_initialize()
        return
    
    # Unknown command - show auto-initialize instead of help
    print(f"❓ Unknown command '{command}' - showing mnemos overview:")
    print()
    auto_initialize()


if __name__ == "__main__":
    main()