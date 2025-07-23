"""Clean, modular behavioral pattern recognition system."""

from .search import SearchPatterns
from .flows import InvestigationFlows
from .momentum import MomentumEngine
from .locations import LocationClusters

__all__ = ['BehavioralPatterns']


class BehavioralPatterns:
    """Unified interface for all behavioral pattern analysis."""
    
    def __init__(self, log_file):
        self.search = SearchPatterns(log_file)
        self.flows = InvestigationFlows(log_file)
        self.momentum = MomentumEngine(log_file)
        self.locations = LocationClusters(log_file)
    
    # Delegate to specialized components
    def track_search(self, term: str) -> None:
        return self.search.track_search(term)
    
    def get_search_breadcrumbs(self, current_term: str, limit: int = 5):
        return self.search.get_search_breadcrumbs(current_term, limit)
    
    def get_investigation_flows(self, limit: int = 3):
        return self.flows.get_investigation_flows(limit)
    
    def get_successful_patterns(self, pattern_type: str = None):
        return self.flows.get_successful_patterns(pattern_type)
    
    def get_momentum_suggestions(self, recent_entries: int = 3, limit: int = 3):
        return self.momentum.get_momentum_suggestions(recent_entries, limit)
    
    def get_location_clusters(self, limit: int = 5):
        return self.locations.get_location_clusters(limit)