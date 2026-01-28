"""Base analyzer interface."""
from abc import ABC, abstractmethod
from typing import Dict, Any
from pathlib import Path


class BaseAnalyzer(ABC):
    """Base class for all analyzers."""
    
    @abstractmethod
    def analyze(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze a repository.
        
        Args:
            repo_path: Path to repository
            
        Returns:
            Dictionary with analysis results
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get analyzer name.
        
        Returns:
            Name of the analyzer
        """
        pass
