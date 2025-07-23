"""Beautiful output formatting for mnemos CLI."""

from typing import Dict, Any, List


class OutputFormatter:
    """Zero-ceremony, beautiful CLI output formatting."""
    
    ICONS = {
        "observation": "👁️",
        "insight": "💡", 
        "discovery": "🎯",
        "issue": "🐛",
        "consideration": "💭",
        "pattern": "🏗️",
        "principle": "📏",
        "antipattern": "🚫",
        "resolved": "✅"
    }
    
    @classmethod
    def log_success(cls, entry_type: str, result_id: str) -> str:
        """Beautiful success message with emoji."""
        icon = cls.ICONS.get(entry_type, "📝")
        return f"{icon} {result_id}"
    
    @classmethod
    def chained_results(cls, results: List[str]) -> str:
        """Format chained command results."""
        return f"⚡ CHAINED: {' → '.join(results)}"
    
    @classmethod
    def memory_health(cls, health: Dict[str, Any]) -> str:
        """Format biological memory health status."""
        state = health['memory_state']
        rec = health['compression_recommendation']
        
        output = [
            "🧠 BIOLOGICAL MEMORY HEALTH",
            "=" * 30,
            f"📊 Status: {health['health'].upper()}",
            f"📈 Entries: {state['total_entries']} ({state['pressure_level']} pressure)",
            f"🎯 Discoveries: {state['discoveries']}",
            f"🏗️  Patterns: {state['patterns']}",
            f"🐛 Open Issues: {state['unresolved_issues']}",
            ""
        ]
        
        if rec['should_compress']:
            output.extend([
                f"💡 RECOMMENDATION: {rec['trigger_description']}",
                f"   Command: mnemos compress  # Will keep {rec['keep_recent']} recent entries"
            ])
        else:
            output.append("✅ No compression needed - memory pressure within healthy limits")
        
        return "\n".join(output)
    
    @classmethod
    def compression_result(cls, result: Dict[str, Any]) -> str:
        """Format compression operation results."""
        if result['status'] == 'reversible_compression':
            return "\n".join([
                "🗜️  Reversible compression complete:",
                f"   Preserved: {result['preserved_discoveries']} discoveries, {result['preserved_patterns']} patterns",
                f"   Compressed: {result['compressed_routine']} routine findings",
                f"   Total: {result['original_count']} → {result['compressed_count']} entries",
                f"   Recovery: mnemos decompress {result['compression_id']}"
            ])
        elif result['status'] == 'semantic_compression':
            return "\n".join([
                "🗜️  Semantic compression complete:",
                f"   Preserved: {result['preserved_discoveries']} discoveries, {result['preserved_patterns']} patterns",
                f"   Compressed: {result['compressed_routine']} routine findings",
                f"   Total: {result['original_count']} → {result['compressed_count']} entries"
            ])
        else:
            return f"🗜️  {result['status']}: {result.get('count', 0)} findings"
    
    @classmethod
    def search_results(cls, results: List[Dict], search_term: str) -> str:
        """Format search results with beautiful formatting."""
        if not results:
            return f"🔍 No results found for '{search_term}'"
        
        output = [
            f"🔍 SEARCH RESULTS: '{search_term}' ({len(results)} matches)",
            "=" * 50,
            ""
        ]
        
        for result in results:
            entry_type = result.get('type', 'unknown')
            timestamp = result.get('timestamp', 'unknown')
            entry_id = result.get('id', 'unknown')
            icon = cls.ICONS.get(entry_type, "📄")
            
            # Type-specific content extraction
            content = cls._extract_content(result, entry_type)
            truncated = content[:70] + ('...' if len(content) > 70 else '')
            
            status_info = ""
            if entry_type == 'issue':
                status = result.get('status', 'unknown')
                status_info = f" | {status.upper()}"
            
            output.append(f"{icon} [{entry_id}] {timestamp}{status_info} | {truncated}")
        
        return "\n".join(output)
    
    @classmethod
    def _extract_content(cls, result: Dict, entry_type: str) -> str:
        """Extract display content based on entry type."""
        content_map = {
            'observation': 'what',
            'insight': 'understanding', 
            'discovery': 'breakthrough',
            'issue': 'problem',
            'consideration': 'idea'
        }
        
        field = content_map.get(entry_type, 'content')
        return result.get(field, str(result))
    
    @classmethod
    def rich_summary(cls, entries: List[Dict], total_count: int) -> str:
        """Format rich investigation overview."""
        if not entries:
            return "🤖 MNEMOS - No investigation memory found"
        
        recent = entries[-10:] if len(entries) > 10 else entries
        
        output = [
            "🧠 MNEMOS INVESTIGATION OVERVIEW",
            "=" * 45,
            f"📊 Total memory: {total_count} entries",
            ""
        ]
        
        # Recent discoveries
        discoveries = [e for e in recent if e.get('type') == 'discovery']
        if discoveries:
            output.append("🎯 RECENT DISCOVERIES:")
            for d in discoveries[-3:]:
                breakthrough = d.get('breakthrough', '')[:80]
                truncated = breakthrough + ('...' if len(d.get('breakthrough', '')) > 80 else '')
                output.append(f"   • {truncated}")
            output.append("")
        
        # Active issues
        all_issues = [e for e in entries if e.get('type') == 'issue']
        resolved_ids = {e.get('issue_id') for e in entries if e.get('type') == 'resolved'}
        active_issues = [i for i in all_issues if i.get('id') not in resolved_ids]
        
        if active_issues:
            output.append("🐛 ACTIVE ISSUES:")
            for issue in active_issues[-3:]:
                problem = issue.get('problem', '')[:60]
                output.append(f"   • [{issue.get('id', 'unknown')}] {problem}")
            output.append("")
        
        # Recent considerations
        considerations = [e for e in recent if e.get('type') == 'consideration']
        if considerations:
            output.append("💭 RECENT CONSIDERATIONS:")
            for c in considerations[-3:]:
                idea = c.get('idea', '')[:70]
                truncated = idea + ('...' if len(c.get('idea', '')) > 70 else '')
                output.append(f"   • {truncated}")
            output.append("")
        
        # Patterns discovered
        patterns = [e for e in entries if e.get('type') == 'pattern']
        if patterns:
            output.append(f"🏗️  PATTERNS DISCOVERED: {len(patterns)}")
            if patterns:
                latest = patterns[-1]
                insight = latest.get('insight', '')[:60]
                truncated = insight + ('...' if len(latest.get('insight', '')) > 60 else '')
                output.append(f"   Latest: {truncated}")
            output.append("")
        
        output.extend([
            f"⚡ Investigation velocity: {len(recent)} entries recently",
            "",
            "🎯 Ready for autonomous investigation!"
        ])
        
        return "\n".join(output)