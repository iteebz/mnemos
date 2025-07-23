"""Biological Memory Management - Automatic, invisible, fault-tolerant.

This module implements self-regulating memory like biological systems:
- Automatic compression triggers based on memory pressure
- Graceful degradation under stress
- Pattern preservation over raw retention
- Zero-ceremony operation for Claude

DESIGN PRINCIPLES:
- Invisible operation (no manual intervention needed)
- Fault tolerant (graceful handling of corruption/errors)  
- Future-proof (extensible trigger systems)
- Biologically inspired (works like human memory)
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class MemoryPressure(Enum):
    """Memory pressure levels for auto-compression triggers."""
    LOW = "low"        # < 50 entries
    MEDIUM = "medium"  # 50-100 entries  
    HIGH = "high"      # 100-200 entries
    CRITICAL = "critical"  # > 200 entries


@dataclass
class CompressionTrigger:
    """Configuration for when and how to compress memory."""
    name: str
    condition: Callable[['MemoryState'], bool]
    keep_recent: int
    priority: int  # Higher = more urgent
    description: str


@dataclass 
class MemoryState:
    """Current state of investigation memory."""
    total_entries: int
    recent_entries: int
    discoveries: int
    patterns: int
    unresolved_issues: int
    memory_age_hours: float
    last_compression_hours: Optional[float]
    
    @property
    def pressure_level(self) -> MemoryPressure:
        """Calculate current memory pressure."""
        if self.total_entries < 50:
            return MemoryPressure.LOW
        elif self.total_entries < 100:
            return MemoryPressure.MEDIUM
        elif self.total_entries < 200:
            return MemoryPressure.HIGH
        else:
            return MemoryPressure.CRITICAL


class BiologicalMemoryManager:
    """Self-regulating memory system inspired by biological memory.
    
    Like the human brain, this system:
    - Automatically consolidates memories during low activity
    - Preserves important patterns while forgetting routine details
    - Gracefully handles memory pressure without data loss
    - Operates invisibly without manual intervention
    """
    
    def __init__(self, log_file: Path, compressor: 'MnemosCompressor'):
        self.log_file = log_file
        self.compressor = compressor
        self.logger = logging.getLogger(__name__)
        
        # Compression triggers - ordered by priority
        self.triggers = [
            CompressionTrigger(
                name="critical_pressure",
                condition=lambda state: state.pressure_level == MemoryPressure.CRITICAL,
                keep_recent=20,
                priority=100,
                description="Emergency compression at >200 entries"
            ),
            CompressionTrigger(
                name="high_pressure_aged",
                condition=lambda state: (
                    state.pressure_level == MemoryPressure.HIGH and 
                    state.memory_age_hours > 2.0
                ),
                keep_recent=25,
                priority=80,
                description="High memory pressure with aged content"
            ),
            CompressionTrigger(
                name="routine_maintenance", 
                condition=lambda state: (
                    state.total_entries > 75 and
                    state.last_compression_hours is not None and
                    state.last_compression_hours > 4.0
                ),
                keep_recent=30,
                priority=40,
                description="Routine maintenance compression"
            ),
            CompressionTrigger(
                name="discovery_preservation",
                condition=lambda state: (
                    state.discoveries > 10 and
                    state.total_entries > 60
                ),
                keep_recent=35,
                priority=60,
                description="Compress to preserve discovery patterns"
            )
        ]
    
    def check_memory_health(self) -> MemoryState:
        """Analyze current memory state for auto-compression decisions."""
        try:
            findings = self.compressor.load_findings(1000)
            
            if not findings:
                return MemoryState(0, 0, 0, 0, 0, 0.0, None)
            
            # Analyze memory composition
            discoveries = len([f for f in findings if f.get("type") == "discovery"])
            patterns = len([f for f in findings if f.get("type") in ["pattern", "principle"]])
            
            # Find unresolved issues
            all_issues = [f for f in findings if f.get("type") == "issue"]
            resolved_ids = {f.get("issue_id") for f in findings if f.get("type") == "resolved"}
            unresolved_issues = len([i for i in all_issues if i.get("id") not in resolved_ids])
            
            # Calculate memory age (simplified - would use proper timestamps in production)
            memory_age_hours = len(findings) * 0.1  # Rough proxy
            
            # Find last compression
            last_compression_hours = None
            for finding in reversed(findings):
                if finding.get("type") == "semantic_summary":
                    # Would calculate actual time difference in production
                    last_compression_hours = 1.0  # Simplified
                    break
            
            return MemoryState(
                total_entries=len(findings),
                recent_entries=min(20, len(findings)),
                discoveries=discoveries,
                patterns=patterns,
                unresolved_issues=unresolved_issues,
                memory_age_hours=memory_age_hours,
                last_compression_hours=last_compression_hours
            )
            
        except Exception as e:
            self.logger.error(f"Memory health check failed: {e}")
            # Return safe defaults on error
            return MemoryState(0, 0, 0, 0, 0, 0.0, None)
    
    def should_compress(self, state: MemoryState) -> Optional[CompressionTrigger]:
        """Determine if compression should trigger and which strategy to use."""
        # Find highest priority trigger that matches current state
        for trigger in sorted(self.triggers, key=lambda t: t.priority, reverse=True):
            try:
                if trigger.condition(state):
                    return trigger
            except Exception as e:
                self.logger.warning(f"Trigger {trigger.name} evaluation failed: {e}")
                continue
        
        return None
    
    def auto_compress_if_needed(self, force: bool = False) -> Dict[str, Any]:
        """Main entry point - check if compression needed and execute.
        
        This method should be called:
        - After every memory write operation
        - Periodically during idle time
        - When memory pressure is detected
        
        Returns compression result or None if no compression occurred.
        """
        try:
            # Health check
            state = self.check_memory_health()
            
            # Skip if memory is too small to compress
            if state.total_entries < 25 and not force:
                return {"status": "no_action_needed", "reason": "memory_too_small"}
            
            # Check compression triggers
            trigger = self.should_compress(state)
            if not trigger and not force:
                return {"status": "no_action_needed", "reason": "no_triggers_matched"}
            
            # Execute compression with appropriate strategy
            keep_recent = trigger.keep_recent if trigger else 15
            
            self.logger.info(f"Auto-compression triggered: {trigger.name if trigger else 'forced'}")
            self.logger.info(f"Memory state: {state.total_entries} entries, {state.pressure_level.value} pressure")
            
            result = self.compressor.compress_findings(keep_recent)
            
            # Enhance result with trigger information
            if result.get("status") == "reversible_compression":
                result["trigger"] = trigger.name if trigger else "manual"
                result["trigger_description"] = trigger.description if trigger else "Manual compression"
                result["memory_pressure"] = state.pressure_level.value
                result["auto_compression"] = True
                
                self.logger.info(f"Auto-compression completed: {result['original_count']} → {result['compressed_count']} entries")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Auto-compression failed: {e}")
            return {
                "status": "compression_failed", 
                "error": str(e),
                "auto_compression": True
            }
    
    def get_memory_status(self) -> Dict[str, Any]:
        """Get current memory status for debugging/monitoring."""
        state = self.check_memory_health()
        trigger = self.should_compress(state)
        
        return {
            "memory_state": {
                "total_entries": state.total_entries,
                "pressure_level": state.pressure_level.value,
                "discoveries": state.discoveries,
                "patterns": state.patterns,
                "unresolved_issues": state.unresolved_issues
            },
            "compression_recommendation": {
                "should_compress": trigger is not None,
                "trigger_name": trigger.name if trigger else None,
                "trigger_description": trigger.description if trigger else None,
                "keep_recent": trigger.keep_recent if trigger else None
            },
            "health": "healthy" if state.total_entries < 150 else "under_pressure"
        }
    
    def configure_trigger(self, trigger_name: str, **kwargs) -> bool:
        """Dynamically configure compression triggers.
        
        This allows future tuning without code changes.
        """
        try:
            for trigger in self.triggers:
                if trigger.name == trigger_name:
                    # Update trigger parameters
                    if "keep_recent" in kwargs:
                        trigger.keep_recent = kwargs["keep_recent"]
                    if "priority" in kwargs:
                        trigger.priority = kwargs["priority"]
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Trigger configuration failed: {e}")
            return False


class AutoCompressionIntegration:
    """Integration layer that hooks auto-compression into the main Mnemos flow.
    
    This provides the zero-ceremony interface that Claude uses.
    """
    
    def __init__(self, log_file: Path, compressor: 'MnemosCompressor'):
        self.memory_manager = BiologicalMemoryManager(log_file, compressor)
        self.compressor = compressor
        
    def post_write_hook(self) -> Optional[Dict[str, Any]]:
        """Called after every memory write to check if compression needed.
        
        This is the key integration point - makes compression invisible.
        """
        return self.memory_manager.auto_compress_if_needed()
    
    def manual_compress(self, keep_recent: int = 15) -> Dict[str, Any]:
        """Manual compression that still uses the biological system."""
        return self.memory_manager.auto_compress_if_needed(force=True)
    
    def memory_status(self) -> Dict[str, Any]:
        """Get memory health status for debugging."""
        return self.memory_manager.get_memory_status()
    
    def health_check(self) -> bool:
        """Quick health check - returns True if memory system is healthy."""
        try:
            status = self.memory_status()
            return status["health"] == "healthy"
        except:
            return False