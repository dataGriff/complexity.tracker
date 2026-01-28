"""JSON reporter for exporting raw data."""
import json
from pathlib import Path
from typing import Dict, Any, List
from complexity_tracker.reporters import BaseReporter


class JsonReporter(BaseReporter):
    """Reporter for generating JSON output."""
    
    def generate(self, results: List[Dict[str, Any]], summary: Dict[str, Any], output_dir: Path):
        """Generate JSON report.
        
        Args:
            results: List of repository analysis results
            summary: Summary statistics
            output_dir: Output directory for reports
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save detailed results
        results_file = output_dir / 'complexity_results.json'
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Detailed results saved to: {results_file}")
        
        # Save summary
        summary_file = output_dir / 'complexity_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Summary saved to: {summary_file}")
