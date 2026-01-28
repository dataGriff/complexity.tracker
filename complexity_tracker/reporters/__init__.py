"""Base reporter interface."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pathlib import Path


class BaseReporter(ABC):
    """Base class for all reporters."""
    
    @abstractmethod
    def generate(self, results: List[Dict[str, Any]], summary: Dict[str, Any], output_dir: Path):
        """Generate report.
        
        Args:
            results: List of repository analysis results
            summary: Summary statistics
            output_dir: Output directory for reports
        """
        pass
