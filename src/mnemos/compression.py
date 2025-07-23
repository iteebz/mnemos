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
        """Reversible semantic compression - preserve signal, compress noise with recovery."""
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
        
        # Create reversible compression archive
        compression_id = int(time.time())
        compressed_archive_path = self.log_file.with_name(f"compressed_{compression_id}.jsonl")
        
        # Store compressed findings with metadata for recovery
        with open(compressed_archive_path, 'w') as f:
            compression_metadata = {
                "type": "compression_metadata",
                "compression_id": compression_id,
                "timestamp": time.strftime("%H:%M:%S"),
                "compressed_count": len(regular_findings),
                "compression_trigger": f"Compressed when memory exceeded {keep_recent + len(old)} entries",
                "recovery_command": f"mnemos decompress {compression_id}"
            }
            f.write(json.dumps(compression_metadata) + '\n')
            
            for finding in regular_findings:
                f.write(json.dumps(finding) + '\n')
        
        # Semantic summary with recovery pointer
        compressed_summary = self._create_semantic_summary(regular_findings, len(old))
        compressed_summary["compression_id"] = compression_id
        compressed_summary["compressed_archive"] = str(compressed_archive_path)
        compressed_summary["recovery_note"] = f"Full details recoverable with: mnemos decompress {compression_id}"
        
        # Final memory: semantic summary + preserved findings + recent
        preserved = discoveries + patterns + principles + critical_issues
        compressed = [compressed_summary] + preserved + recent
        
        # Backup original (keep for safety)
        backup_path = self.log_file.with_suffix(f'.backup_{compression_id}.jsonl')
        backup_path.write_text(self.log_file.read_text())
        
        with open(self.log_file, 'w') as f:
            for finding in compressed:
                f.write(json.dumps(finding) + '\n')
        
        return {
            "status": "reversible_compression",
            "original_count": len(findings),
            "compressed_count": len(compressed),
            "preserved_discoveries": len(discoveries),
            "preserved_patterns": len(patterns + principles),
            "compressed_routine": len(regular_findings),
            "compression_id": compression_id,
            "compressed_archive": str(compressed_archive_path),
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
    
    def decompress_findings(self, compression_id: int) -> Dict[str, Any]:
        """Recover compressed findings by compression ID - reversible compression."""
        # Find the compressed archive
        compressed_archive_path = self.log_file.with_name(f"compressed_{compression_id}.jsonl")
        
        if not compressed_archive_path.exists():
            return {"status": "archive_not_found", "compression_id": compression_id}
        
        # Load compressed findings
        compressed_findings = []
        metadata = None
        
        with open(compressed_archive_path) as f:
            for line in f:
                if line.strip():
                    finding = json.loads(line)
                    if finding.get("type") == "compression_metadata":
                        metadata = finding
                    else:
                        compressed_findings.append(finding)
        
        if not metadata:
            return {"status": "invalid_archive", "compression_id": compression_id}
        
        # Load current memory
        current_findings = self.load_findings(1000)
        
        # Find and remove the semantic summary for this compression
        updated_findings = []
        summary_removed = False
        
        for finding in current_findings:
            if (finding.get("type") == "semantic_summary" and 
                finding.get("compression_id") == compression_id):
                summary_removed = True
                continue
            updated_findings.append(finding)
        
        if not summary_removed:
            return {"status": "summary_not_found", "compression_id": compression_id}
        
        # Insert compressed findings back in chronological order
        # This is simplified - in production would need proper timestamp sorting
        final_findings = compressed_findings + updated_findings
        
        # Create backup before decompression
        backup_path = self.log_file.with_suffix(f'.pre_decompress_{compression_id}.jsonl')
        backup_path.write_text(self.log_file.read_text())
        
        # Write expanded memory
        with open(self.log_file, 'w') as f:
            for finding in final_findings:
                f.write(json.dumps(finding) + '\n')
        
        # Archive the compression file (keep for audit trail)
        archived_compression = compressed_archive_path.with_suffix('.archived.jsonl')
        compressed_archive_path.rename(archived_compression)
        
        return {
            "status": "decompressed",
            "compression_id": compression_id,
            "recovered_count": len(compressed_findings),
            "total_count": len(final_findings),
            "backup_created": str(backup_path),
            "compressed_archive_moved": str(archived_compression)
        }
    
    def list_compressions(self) -> List[Dict[str, Any]]:
        """List all available compression archives for recovery."""
        compressions = []
        
        # Find all compressed_*.jsonl files
        parent_dir = self.log_file.parent
        for file_path in parent_dir.glob("compressed_*.jsonl"):
            try:
                compression_id = int(file_path.stem.split('_')[1])
                
                # Read metadata
                with open(file_path) as f:
                    first_line = f.readline()
                    if first_line:
                        metadata = json.loads(first_line)
                        if metadata.get("type") == "compression_metadata":
                            compressions.append({
                                "compression_id": compression_id,
                                "timestamp": metadata.get("timestamp"),
                                "compressed_count": metadata.get("compressed_count"),
                                "archive_path": str(file_path)
                            })
            except (ValueError, json.JSONDecodeError):
                continue
        
        return sorted(compressions, key=lambda x: x["compression_id"], reverse=True)