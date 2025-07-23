"""Extended examples and advanced techniques for mnemos investigations."""

ADVANCED_EXAMPLES = """# Advanced Investigation Examples

## Example 1: Performance Bottleneck Investigation

```python
# 1. OBSERVE
mnemos.observation("API response times increased 3x after deployment")
mnemos.thread("performance_degradation", "active")

# 2. HYPOTHESIZE  
mnemos.insight("Could be database connection pooling, caching, or new code inefficiency")

# 3. TEST
mnemos.observation("Database query logs show 10x more connection attempts")
mnemos.observation("Connection pool size unchanged at 5, but concurrent users now 50+")

# 4. LEARN
mnemos.discovery("Connection pool exhaustion causing cascade delays", 
                impact="Root cause identified - simple configuration fix",
                solution="Increased pool size from 5 to 20")

# 5. ITERATE
mnemos.thread("performance_degradation", "completed") 
mnemos.pattern("Connection pool sizing needs to scale with user growth")
```

## Example 2: Architecture Investigation

```python
# Initial observation
mnemos.observation("Three different HTTP clients used across similar services")
mnemos.thread("http_client_inconsistency", "active")

# Pattern recognition
mnemos.insight("Each team chose different client: requests, httpx, aiohttp")
mnemos.insight("No shared library or standard for HTTP client selection")

# Investigation deepens
mnemos.observation("Performance characteristics vary significantly between clients")
mnemos.observation("Error handling patterns are inconsistent across services")

# Strategic insight
mnemos.principle("Standardize on single HTTP client across organization")
mnemos.pattern("Team autonomy without standards leads to fragmentation")
mnemos.antipattern("Multiple HTTP clients in same codebase without justification")
```

## Example 3: Meta-Investigation Discovery

```python
# After meta-reflection reveals patterns
mnemos.meta_reflect()

# Strategic breakthrough  
mnemos.discovery("Most critical issues cluster in authentication modules",
                impact="Authentication is systemic weak point requiring focused effort")

mnemos.pattern("Authentication complexity correlates with bug density")
mnemos.principle("Simplify authentication flows to reduce bug surface area")

# New investigation thread spawned from meta-analysis
mnemos.thread("authentication_simplification", "active")
```

## Investigation Thread Management

### Active Thread Tracking
```python
# Start investigation
mnemos.thread("database_migration_issues", "active")

# Track progress through findings
mnemos.observation("Migration script fails on large datasets")
mnemos.insight("Memory usage spikes during batch processing")
mnemos.discovery("Batch size optimization reduces memory 90%")

# Complete thread
mnemos.thread("database_migration_issues", "completed")
```

### Thread Abandonment
```python
# When investigation proves unfruitful
mnemos.thread("cache_invalidation_theory", "abandoned")
mnemos.insight("Cache invalidation not the root cause - DNS issues confirmed instead")
```

## Pattern Recognition Techniques

### Location-Based Pattern Detection
```python
# Multiple issues in same module
mnemos.issue("Authentication failure", location="auth/login.py:45", severity="critical")
mnemos.issue("Session timeout", location="auth/session.py:23", severity="medium")  
mnemos.issue("Permission check bug", location="auth/permissions.py:67", severity="high")

# Meta-reflection will detect "auth" module as hotspot
```

### Temporal Pattern Recognition
```python
# Time-based correlation discovery
mnemos.observation("Error rate spikes every morning at 9am")
mnemos.observation("Database connection count peaks at same time")
mnemos.insight("Morning user surge exceeds infrastructure capacity")
mnemos.discovery("Predictable load patterns enable proactive scaling")
```

## Advanced Meta-Reflection Usage

### Custom Reflection Triggers
```python
# Force reflection after major discoveries
mnemos.discovery("New caching strategy reduces latency 50%")
mnemos.meta_reflect(trigger_count=5)  # Lower threshold for immediate analysis
```

### Pattern-Driven Investigation
```python
# Use meta-reflection results to guide next steps
reflection = mnemos.meta_reflect()
if "authentication" in str(reflection.get("issue_hotspots", {})):
    mnemos.thread("auth_deep_dive", "active")
    mnemos.observation("Meta-analysis suggests focusing on authentication module")
```

## Memory Management Strategies

### Semantic Compression
```python
# When memory grows large, preserve high-value insights
result = mnemos.compress_findings(keep_recent=20)
print(f"Compressed {result['compressed_routine']} routine findings")
print(f"Preserved {result['preserved_discoveries']} discoveries")
```

### Strategic vs Tactical Balance
```python
# Balance session-specific vs cross-project insights
mnemos.observation("Current deployment failing")  # Tactical
mnemos.pattern("Deployment failures often trace to config mismatches")  # Strategic
```

## Investigation Quality Principles

1. **Specific over general** - "Database deadlock in user registration" vs "database issues"
2. **Evidence-based** - Link insights to concrete observations
3. **Actionable** - Discoveries should enable next steps
4. **Connected** - Reference related findings and patterns
5. **Persistent** - Important insights become principles/patterns

## Common Investigation Antipatterns

❌ **Hypothesis tunneling** - Sticking to first theory despite contradicting evidence
❌ **Pattern forcing** - Finding patterns where none exist  
❌ **Shallow observation** - Not digging into anomalies
❌ **Poor logging discipline** - Investigating without recording findings
❌ **Meta-neglect** - Never stepping back to see bigger patterns
"""

INVESTIGATION_CHECKLISTS = """# Investigation Checklists

## Starting New Investigation

- [ ] Review existing findings for related patterns
- [ ] Start investigation thread: `mnemos.thread("topic", "active")`
- [ ] Define clear observation target
- [ ] Check for obvious explanations first

## During Investigation

- [ ] Log observations immediately - don't batch
- [ ] Follow evidence, not assumptions
- [ ] Look for patterns in unexpected places
- [ ] Connect to previous discoveries when relevant
- [ ] Ask "why" at least 3 times for each finding

## Completing Investigation

- [ ] Mark thread status: completed/abandoned
- [ ] Extract patterns/principles from discoveries
- [ ] Check if meta-reflection is due
- [ ] Document key learnings for future reference

## Meta-Reflection Checklist

- [ ] Analyze findings from last 50 entries
- [ ] Identify hotspot modules/locations
- [ ] Look for temporal patterns
- [ ] Extract cross-cutting insights
- [ ] Generate strategic principles from tactical findings

## Memory Management Checklist

- [ ] Monitor memory size (>50 findings consider compression)
- [ ] Preserve discoveries, patterns, principles
- [ ] Compress routine observations and resolved issues
- [ ] Maintain investigation velocity vs memory size balance
"""