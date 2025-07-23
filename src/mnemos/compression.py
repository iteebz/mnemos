"""Mnemos compression methods - findings compression and archival."""

import json
import time
from pathlib import Path
from typing import Dict, Any, List


class MnemosCompressor:
    """Findings compression and archival for Mnemos investigation system."""
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
        
    def load_findings(self, limit: int = 1000) -> List[Dict]:
        """Load findings for compression analysis."""
        if not self.log_file.exists():
            return []
            
        findings = []
        with open(self.log_file) as f:
            for line in f:
                if line.strip():
                    findings.append(json.loads(line))
        return findings[-limit:]  # Last N entries
    
    def compress_findings(self, keep_recent: int = 15) -> Dict[str, Any]:
        """Semantic compression - preserve signal, compress noise."""
        findings = self.load_findings(1000)
        
        if len(findings) <= keep_recent:
            return {"status": "no_compression_needed", "count": len(findings)}
        
        # Semantic preservation strategy
        recent = findings[-keep_recent:]
        old = findings[:-keep_recent]
        
        # PRESERVE: High-value findings regardless of age
        discoveries = [f for f in old if f.get("type") == "discovery"]
        patterns = [f for f in old if f.get("type") == "pattern"]
        principles = [f for f in old if f.get("type") == "principle"]
        critical_issues = [f for f in old if f.get("type") in ["bug", "issue"] and f.get("severity") == "critical"]
        
        # COMPRESS: Regular observations and resolved issues
        regular_findings = [f for f in old if f not in discoveries + patterns + principles + critical_issues]
        
        # Semantic summary of compressed findings
        compressed_summary = self._create_semantic_summary(regular_findings, len(old))
        
        # Final memory: semantic summary + preserved findings + recent
        preserved = discoveries + patterns + principles + critical_issues
        compressed = [compressed_summary] + preserved + recent
        
        # Backup and write
        backup_path = self.log_file.with_suffix('.backup.jsonl')
        backup_path.write_text(self.log_file.read_text())
        
        with open(self.log_file, 'w') as f:
            for finding in compressed:
                f.write(json.dumps(finding) + '\n')
        
        return {
            "status": "semantic_compression",
            "original_count": len(findings),
            "compressed_count": len(compressed),
            "preserved_discoveries": len(discoveries),
            "preserved_patterns": len(patterns + principles),
            "compressed_routine": len(regular_findings),
            "backup_created": str(backup_path)
        }
    
    def _create_semantic_summary(self, compressed_findings: List[Dict], total_old: int) -> Dict[str, Any]:
        """Create intelligent summary preserving essential patterns."""
        observations = [f for f in compressed_findings if f.get("type") == "observation"]
        insights = [f for f in compressed_findings if f.get("type") == "insight"]
        regular_issues = [f for f in compressed_findings if f.get("type") in ["bug", "issue"]]
        
        # Extract semantic patterns
        issue_locations = {}
        for issue in regular_issues:
            loc = issue.get("location", "unknown")
            module = loc.split("/")[0] if "/" in loc else loc
            issue_locations[module] = issue_locations.get(module, 0) + 1
        
        # Key insights extraction
        key_insights = [i.get("understanding", "") for i in insights[-3:]]
        
        return {
            "timestamp": time.strftime("%H:%M:%S"),
            "type": "semantic_summary",
            "period_summary": f"Compressed {len(compressed_findings)} routine findings from {total_old} total",
            "observation_patterns": len(observations),
            "insight_patterns": len(insights),
            "routine_issues": len(regular_issues),
            "issue_hotspots": dict(sorted(issue_locations.items(), key=lambda x: x[1], reverse=True)[:3]),
            "key_insights": key_insights,
            "compression_intelligence": "Preserved discoveries, patterns, principles. Compressed routine observations."
        }