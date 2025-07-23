# Mnemos - Autonomous Investigation System

**Zero-ceremony autonomous investigation for AI development**

## Philosophy

Mnemos is designed for Claude developing tools for Claude. A **minimal core for real-time hypothesis-driven discovery** that gets smarter over time through semantic compression and persistent memory.

## Core Principle

```
🔄 OBSERVE → HYPOTHESIZE → TEST → LEARN → ITERATE
     ↓ (periodic)
🧠 META-REFLECT → PATTERN-DETECT → SYSTEMIC-INSIGHTS
```

## Installation

```bash
pip install mnemos
```

## Quick Start

```python
from mnemos import Mnemos
mnemos = Mnemos()  # Auto-creates .mnemos/ memory

# Tactical investigation
mnemos.observation("What you see")
mnemos.insight("What it means")
mnemos.discovery("Breakthrough that changes everything")
mnemos.issue("Problem found", location="file:line")

# Strategic memory  
mnemos.pattern("Architectural insight")
mnemos.principle("Design rule")
mnemos.antipattern("What to avoid")
```

## CLI Interface

```bash
# Quick logging (Claude-optimized)
mnemos o "observation"     # Log what you see
mnemos i "insight"         # Log what it means
mnemos d "discovery"       # Log breakthrough
mnemos x "problem"         # Log issue

# Investigation flow
mnemos start "topic"       # Begin investigation
mnemos status              # Show current state
mnemos reflect             # Meta-analysis
mnemos compress            # Semantic compression

# Memory validation
mnemos --verbose status    # Shows memory locations
```

## Polyrepo Memory

```bash
# Unified memory across projects
export MNEMOS_HOME=~/workspace/.mnemos
mnemos status  # Shared investigation context

# Per-project memory (default)
mnemos status  # Local .mnemos directory
```

## Semantic Compression

Mnemos gets **smarter over time**:
- **Preserves**: Discoveries, patterns, principles, critical issues
- **Compresses**: Routine observations, resolved issues  
- **Intelligence**: Rich knowledge without noise accumulation

```bash
mnemos compress  # Manual compression
# Automatic compression when memory grows large
```

## Global Access

Install once, use everywhere:
```bash
# Add to ~/bin/mnemos for global access
chmod +x ~/bin/mnemos

# Auto-detects context:
# 1. Development directory: poetry run mnemos
# 2. Project with mnemos dependency: poetry run mnemos  
# 3. Fallback: development version from ~/dev/workspace/mnemos
```

## Core Files

- `.mnemos/mnemos.jsonl` - Investigation findings
- `.mnemos/reflections.jsonl` - Meta-analysis insights
- Environment: `MNEMOS_HOME` for unified memory

## Advanced Usage

For comprehensive investigation protocols and examples:
```python
mnemos.protocol()     # Full autonomous investigation guide
mnemos.methodology()  # Human-like discovery techniques
```

## The Revolution

**Before**: Static documentation, forgotten context, manual correlation
**After**: Living memory, persistent intelligence, autonomous pattern detection

Mnemos is Claude developing custom tooling so Claude can operate better. Meta-cognitive development at its finest.