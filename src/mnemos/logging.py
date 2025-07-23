
"""Mnemos unified logging - tactical, strategic, and operational findings."""

import json
import time
import uuid
from pathlib import Path
from typing import Dict, Any


class MnemosLogger:
    """Core logging functionality for Mnemos investigation system."""
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
        
    def observation(self, what: str, context: str = "") -> str:
        """Log raw findings - what you see, data points."""
        obs_id = str(uuid.uuid4())[:8]
        finding = {
            "id": obs_id,
            "timestamp": time.strftime("%H:%M:%S"),
            "what": what,
            "context": context,
            "type": "observation"
        }
        
        self._write_finding(finding)
        print(f"👁️ OBSERVATION: {what}")
        return obs_id
    
    def insight(self, understanding: str, evidence: str = "") -> str:
        """Log analyzed understanding - what observations mean."""
        insight_id = str(uuid.uuid4())[:8]
        finding = {
            "id": insight_id,
            "timestamp": time.strftime("%H:%M:%S"),
            "understanding": understanding,
            "evidence": evidence,
            "type": "insight"
        }
        
        self._write_finding(finding)
        print(f"💡 INSIGHT: {understanding}")
        return insight_id
    
    def discovery(self, breakthrough: str, impact: str, solution: str = "") -> str:
        """Log major findings that change everything - breakthroughs."""
        discovery_id = str(uuid.uuid4())[:8]
        finding = {
            "id": discovery_id,
            "timestamp": time.strftime("%H:%M:%S"),
            "breakthrough": breakthrough,
            "impact": impact,
            "solution": solution,
            "type": "discovery"
        }
        
        self._write_finding(finding)
        print(f"🎯 DISCOVERY: {breakthrough}")
        return discovery_id
    
    def issue(self, problem: str, location: str, severity: str = "medium") -> str:
        """Log discovered issues concisely."""
        issue_id = str(uuid.uuid4())[:8]
        finding = {
            "id": issue_id,
            "timestamp": time.strftime("%H:%M:%S"),
            "problem": problem,
            "location": location, 
            "severity": severity,
            "status": "open",
            "type": "issue"
        }
        
        self._write_finding(finding)
        print(f"🐛 ISSUE [{issue_id}]: {problem} at {location}")
        return issue_id
    
    def resolve(self, issue_id: str, solution: str) -> str:
        """Mark issue as resolved with explicit ID linking."""
        resolved_id = str(uuid.uuid4())[:8]
        finding = {
            "id": resolved_id,
            "timestamp": time.strftime("%H:%M:%S"),
            "issue_id": issue_id,
            "solution": solution,
            "type": "resolved"
        }
        
        self._write_finding(finding)
        print(f"✅ RESOLVE [{issue_id}]: {solution}")
        return resolved_id
    
    # Strategic memory methods
    def pattern(self, insight: str, value: str) -> str:
        """Log architectural patterns that persist across projects."""
        pattern_id = str(uuid.uuid4())[:8]
        finding = {
            "id": pattern_id,
            "timestamp": time.strftime("%H:%M:%S"),
            "insight": insight,
            "value": value,
            "type": "pattern"
        }
        
        self._write_finding(finding)
        print(f"🏗️ PATTERN: {insight}")
        return pattern_id
    
    def principle(self, rule: str, rationale: str) -> str:
        """Log design principles and rules."""
        principle_id = str(uuid.uuid4())[:8]
        finding = {
            "id": principle_id,
            "timestamp": time.strftime("%H:%M:%S"),
            "rule": rule,
            "rationale": rationale,
            "type": "principle"
        }
        
        self._write_finding(finding)
        print(f"⚖️ PRINCIPLE: {rule}")
        return principle_id
    
    def antipattern(self, problem: str, why_bad: str) -> str:
        """Log things to avoid and why."""
        antipattern_id = str(uuid.uuid4())[:8]
        finding = {
            "id": antipattern_id,
            "timestamp": time.strftime("%H:%M:%M"),
            "problem": problem,
            "why_bad": why_bad,
            "type": "antipattern"
        }
        
        self._write_finding(finding)
        print(f"🚫 ANTIPATTERN: {problem}")
        return antipattern_id
    
    def consideration(self, idea: str, context: str = "") -> str:
        """Log future considerations - ideas to evaluate later, not actionable tasks."""
        consideration_id = str(uuid.uuid4())[:8]
        finding = {
            "id": consideration_id,
            "timestamp": time.strftime("%H:%M:%S"),
            "idea": idea,
            "context": context,
            "type": "consideration"
        }
        
        self._write_finding(finding)
        print(f"💭 CONSIDERATION: {idea}")
        return consideration_id
    
    def thread(self, name: str, status: str = "active") -> Dict[str, Any]:
        """Track investigation threads - what you're currently digging into."""
        finding = {
            "timestamp": time.strftime("%H:%M:%S"),
            "thread": name,
            "status": status,  # active, completed, abandoned
            "type": "thread"
        }
        
        self._write_finding(finding)
        return finding
    
    def search(self, term: str, search_type: str = None, limit: int = 10) -> list:
        """Search investigation history for patterns and discoveries."""
        if not self.log_file.exists():
            return []
        
        results = []
        with open(self.log_file, 'r') as f:
            for line in f:
                try:
                    finding = json.loads(line.strip())
                    
                    # Type filtering
                    if search_type and finding.get('type') != search_type:
                        continue
                    
                    # Text search across all text fields
                    searchable_text = []
                    for key, value in finding.items():
                        if isinstance(value, str) and key != 'id':
                            searchable_text.append(value.lower())
                    
                    if any(term.lower() in text for text in searchable_text):
                        results.append(finding)
                        
                except json.JSONDecodeError:
                    continue
        
        # Return most recent first, limited
        return results[-limit:] if results else []
    
    def _write_finding(self, finding: Dict[str, Any]) -> None:
        """Write finding to log file."""
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(finding) + '\n')

    def undo(self) -> bool:
        """Remove the last finding from the log file."""
        if not self.log_file.exists():
            return False
        
        with open(self.log_file, "r+") as f:
            lines = f.readlines()
            if not lines:
                return False
            
            # Move the pointer to the beginning of the last line
            f.seek(0)
            f.truncate()
            f.writelines(lines[:-1])
            
        print("⏪ UNDO: Last entry removed.")
        return True
