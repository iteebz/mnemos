"""Mnemos analysis methods - meta-reflection, pattern detection."""

import json
import time
from pathlib import Path
from typing import Dict, Any, List


class MnemosAnalyzer:
    """Meta-analysis and pattern detection for Mnemos investigation system."""
    
    def __init__(self, log_file: Path, reflection_file: Path):
        self.log_file = log_file
        self.reflection_file = reflection_file
        
    def load_recent(self, limit: int = 10) -> List[Dict]:
        """Load recent findings for pattern recognition."""
        if not self.log_file.exists():
            return []
            
        findings = []
        with open(self.log_file) as f:
            for line in f:
                if line.strip():
                    findings.append(json.loads(line))
        return findings[-limit:]  # Last N entries
    
    def active_threads(self) -> List[str]:
        """Get currently active investigation threads."""
        recent = self.load_recent(20)
        threads = []
        
        for finding in reversed(recent):  # Most recent first
            if finding.get("type") == "thread":
                thread = finding["thread"]
                status = finding["status"]
                
                if status == "active" and thread not in [t for t, _ in threads]:
                    threads.append((thread, "active"))
                elif status in ["completed", "abandoned"]:
                    # Remove from active if we find completion
                    threads = [(t, s) for t, s in threads if t != thread]
                    
        return [thread for thread, status in threads if status == "active"]
    
    def meta_reflect(self, trigger_count: int = 10) -> Dict[str, Any]:
        """Meta-investigation: find patterns across findings themselves."""
        recent = self.load_recent(50)  # Larger window for pattern detection
        
        if len(recent) < trigger_count:
            return {"status": "insufficient_data", "count": len(recent)}
        
        # Pattern detection across findings - handle both old "bug" and new "issue" types
        issues = [f for f in recent if f.get("type") in ["bug", "issue"]]
        discoveries = [f for f in recent if f.get("type") == "discovery"]
        
        # Issue clustering by location/type - handle both field names
        issue_locations = {}
        for issue in issues[-10:]:  # Last 10 issues
            location = issue.get("location", "unknown")
            module = location.split("/")[0] if "/" in location else location
            issue_locations[module] = issue_locations.get(module, 0) + 1
        
        # Investigation success patterns
        thread_outcomes = {}
        for finding in reversed(recent):
            if finding.get("type") == "thread":
                thread = finding["thread"]
                status = finding["status"]
                thread_outcomes[thread] = status
        
        completed_threads = [t for t, s in thread_outcomes.items() if s == "completed"]
        
        reflection = {
            "timestamp": time.strftime("%H:%M:%S"),
            "findings_analyzed": len(recent),
            "issue_hotspots": dict(sorted(issue_locations.items(), key=lambda x: x[1], reverse=True)[:3]),
            "completed_investigations": len(completed_threads),
            "pattern_insights": self._generate_pattern_insights(issues, discoveries, issue_locations),
            "type": "meta_reflection"
        }
        
        # Log the reflection
        with open(self.reflection_file, 'a') as f:
            f.write(json.dumps(reflection) + '\n')
        
        print(f"🧠 META-REFLECTION: Analyzed {len(recent)} findings")
        return reflection
    
    def _generate_pattern_insights(self, issues: List[Dict], discoveries: List[Dict], locations: Dict[str, int]) -> List[str]:
        """Generate insights from pattern analysis."""
        insights = []
        
        # Hot module detection
        if locations:
            hottest = max(locations.items(), key=lambda x: x[1])
            if hottest[1] >= 2:
                insights.append(f"Issue hotspot detected: {hottest[0]} module ({hottest[1]} issues)")
        
        # Investigation velocity
        if len(discoveries) >= 3:
            insights.append(f"High discovery rate: {len(discoveries)} discoveries recently")
        
        # Critical issue patterns - handle both old "bug" and new "issue" field names
        critical_issues = [i for i in issues if i.get("severity") == "critical"]
        if len(critical_issues) >= 2:
            insights.append(f"Multiple critical issues suggest systemic problems")
        
        return insights if insights else ["No clear patterns detected yet"]
    
    def summarize(self) -> Dict[str, Any]:
        """Efficient summary for fresh sessions."""
        recent = self.load_recent(20)
        
        issues = [f for f in recent if f.get("type") in ["bug", "issue"]]
        discoveries = [f for f in recent if f.get("type") == "discovery"]
        active = self.active_threads()
        
        # Check if meta-reflection is due
        total_findings = len([f for f in recent if f.get("type") in ["bug", "issue", "discovery"]])
        reflection_due = total_findings >= 10
        
        summary = {
            "recent_issues": len(issues),
            "recent_discoveries": len(discoveries), 
            "active_threads": active,
            "last_discovery": discoveries[-1] if discoveries else None,
            "reflection_due": reflection_due,
            "total_findings": total_findings
        }
        
        # Include last reflection if available
        if self.reflection_file.exists():
            try:
                with open(self.reflection_file) as f:
                    lines = [line for line in f if line.strip()]
                    if lines:
                        last_reflection = json.loads(lines[-1])
                        summary["last_reflection"] = last_reflection
            except:
                pass
        
        return summary