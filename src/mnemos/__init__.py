"""Mnemos - Autonomous investigation and memory system."""

from .core import Mnemos

__all__ = ["Mnemos"]
__version__ = "0.2.0"

# CLI entry point
def main():
    """CLI entry point for modular CLI system."""
    from .cli.main import main as cli_main
    cli_main()