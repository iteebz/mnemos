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
    
    def archive_findings(self, archive_filter: str = None, older_than_hours: int = None) -> Dict[str, Any]:
        """Archive irrelevant findings permanently - beyond compression."""
        findings = self.load_findings(1000)
        
        if not findings:
            return {"status": "no_findings", "count": 0}
        
        archive_candidates = []
        remaining_findings = []
        
        # Archive criteria: semantic filters or time-based
        for finding in findings:
            should_archive = False
            
            # Time-based archival
            if older_than_hours:
                # Simple timestamp-based check (would need proper datetime parsing in production)
                should_archive = True  # Simplified for demo
            
            # Semantic filter archival
            if archive_filter:
                finding_text = json.dumps(finding).lower()
                if archive_filter.lower() in finding_text:
                    should_archive = True
            
            # Never archive critical types
            if finding.get("type") in ["discovery", "pattern", "principle"]:
                should_archive = False
            
            if should_archive:
                archive_candidates.append(finding)
            else:
                remaining_findings.append(finding)
        
        if not archive_candidates:
            return {"status": "no_candidates", "count": 0}
        
        # Create archive file
        archive_path = self.log_file.with_name(f"archive_{int(time.time())}.jsonl")
        with open(archive_path, 'w') as f:
            for finding in archive_candidates:
                f.write(json.dumps(finding) + '\n')
        
        # Rewrite main file without archived findings
        with open(self.log_file, 'w') as f:
            for finding in remaining_findings:
                f.write(json.dumps(finding) + '\n')
        
        return {
            "status": "archived",
            "archived_count": len(archive_candidates),
            "remaining_count": len(remaining_findings),
            "archive_file": str(archive_path)
        }
    
    def delete_findings(self, delete_filter: str = None, entry_ids: List[str] = None) -> Dict[str, Any]:
        """Permanently delete specific findings - use with caution."""
        findings = self.load_findings(1000)
        
        if not findings:
            return {"status": "no_findings", "count": 0}
        
        deleted_findings = []
        remaining_findings = []
        
        for finding in findings:
            should_delete = False
            
            # Delete by ID
            if entry_ids and finding.get("id") in entry_ids:
                should_delete = True
            
            # Delete by filter
            if delete_filter:
                finding_text = json.dumps(finding).lower()
                if delete_filter.lower() in finding_text:
                    should_delete = True
            
            # Safety: Never delete critical discoveries
            if finding.get("type") in ["discovery", "pattern", "principle"]:
                should_delete = False
            
            if should_delete:
                deleted_findings.append(finding)
            else:
                remaining_findings.append(finding)
        
        if not deleted_findings:
            return {"status": "no_matches", "count": 0}
        
        # Create backup before deletion
        backup_path = self.log_file.with_name(f"deleted_backup_{int(time.time())}.jsonl")
        with open(backup_path, 'w') as f:
            for finding in deleted_findings:
                f.write(json.dumps(finding) + '\n')
        
        # Rewrite main file without deleted findings
        with open(self.log_file, 'w') as f:
            for finding in remaining_findings:
                f.write(json.dumps(finding) + '\n')
        
        return {
            "status": "deleted",
            "deleted_count": len(deleted_findings),
            "remaining_count": len(remaining_findings),
            "backup_file": str(backup_path)
        }