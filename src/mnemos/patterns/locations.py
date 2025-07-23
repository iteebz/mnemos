"""Location-based issue clustering analysis."""

import json
from collections import defaultdict, Counter
from pathlib import Path
from typing import List, Dict, Any


class LocationClusters:
    """Analyzes issue patterns by location to identify hotspots."""
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
    
    def get_location_clusters(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get issue clusters by location."""
        if not self.log_file.exists():
            return []
        
        location_issues = defaultdict(list)
        
        with open(self.log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if entry.get('type') == 'issue' and 'location' in entry:
                        location_issues[entry['location']].append({
                            'problem': entry['problem'],
                            'severity': entry.get('severity', 'medium'),
                            'timestamp': entry['timestamp']
                        })
                except json.JSONDecodeError:
                    continue
        
        # Sort by issue count and return top locations
        sorted_locations = sorted(
            location_issues.items(), 
            key=lambda x: len(x[1]), 
            reverse=True
        )[:limit]
        
        return [
            {
                'location': location,
                'issue_count': len(issues),
                'recent_issues': issues[-3:],  # Last 3 issues
                'severity_distribution': Counter(i['severity'] for i in issues)
            }
            for location, issues in sorted_locations
        ]