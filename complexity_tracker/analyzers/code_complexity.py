"""Code complexity analyzer using multiple tools."""
import os
from pathlib import Path
from typing import Dict, Any, List
import lizard
from complexity_tracker.analyzers import BaseAnalyzer


class CodeComplexityAnalyzer(BaseAnalyzer):
    """Analyzer for code complexity metrics (cyclomatic complexity, etc.)."""
    
    def __init__(self, exclude_patterns: List[str] = None):
        """Initialize code complexity analyzer.
        
        Args:
            exclude_patterns: List of patterns to exclude from analysis
        """
        self.exclude_patterns = exclude_patterns or []
    
    def get_name(self) -> str:
        """Get analyzer name."""
        return "code_complexity"
    
    def _should_exclude(self, file_path: Path, repo_path: Path) -> bool:
        """Check if file should be excluded.
        
        Args:
            file_path: Path to file
            repo_path: Root path of repository
            
        Returns:
            True if file should be excluded
        """
        relative_path = str(file_path.relative_to(repo_path))
        for pattern in self.exclude_patterns:
            pattern = pattern.replace('*/', '')
            if pattern in relative_path:
                return True
        return False
    
    def analyze(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze code complexity in repository.
        
        Args:
            repo_path: Path to repository
            
        Returns:
            Dictionary with complexity metrics
        """
        results = {
            'total_files': 0,
            'total_functions': 0,
            'total_lines_of_code': 0,
            'total_complexity': 0,
            'average_complexity': 0,
            'max_complexity': 0,
            'high_complexity_functions': [],
            'complexity_by_language': {},
            'files_analyzed': []
        }
        
        try:
            # Use lizard for language-agnostic complexity analysis
            for root, dirs, files in os.walk(repo_path):
                # Skip hidden directories and common ignore patterns
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'vendor', '__pycache__']]
                
                for file in files:
                    file_path = Path(root) / file
                    
                    # Skip non-code files
                    if file_path.suffix in ['.md', '.txt', '.json', '.xml', '.yaml', '.yml', '.lock', '.min.js']:
                        continue
                    
                    # Check exclusion patterns
                    if self._should_exclude(file_path, repo_path):
                        continue
                    
                    try:
                        # Analyze file with lizard
                        analysis = lizard.analyze_file(str(file_path))
                        
                        if analysis.function_list:
                            results['total_files'] += 1
                            file_complexity = 0
                            
                            for func in analysis.function_list:
                                results['total_functions'] += 1
                                complexity = func.cyclomatic_complexity
                                file_complexity += complexity
                                results['total_complexity'] += complexity
                                results['max_complexity'] = max(results['max_complexity'], complexity)
                                
                                # Track high complexity functions (> 10 is considered complex)
                                if complexity > 10:
                                    results['high_complexity_functions'].append({
                                        'file': str(file_path.relative_to(repo_path)),
                                        'function': func.name,
                                        'complexity': complexity,
                                        'lines': func.nloc
                                    })
                            
                            # Track by language
                            ext = file_path.suffix
                            if ext not in results['complexity_by_language']:
                                results['complexity_by_language'][ext] = {
                                    'files': 0,
                                    'functions': 0,
                                    'total_complexity': 0
                                }
                            
                            results['complexity_by_language'][ext]['files'] += 1
                            results['complexity_by_language'][ext]['functions'] += len(analysis.function_list)
                            results['complexity_by_language'][ext]['total_complexity'] += file_complexity
                            
                            results['total_lines_of_code'] += analysis.nloc
                            
                            results['files_analyzed'].append({
                                'path': str(file_path.relative_to(repo_path)),
                                'functions': len(analysis.function_list),
                                'complexity': file_complexity,
                                'lines': analysis.nloc
                            })
                    
                    except Exception as e:
                        # Skip files that can't be analyzed
                        continue
            
            # Calculate average
            if results['total_functions'] > 0:
                results['average_complexity'] = results['total_complexity'] / results['total_functions']
            
            # Sort high complexity functions by complexity
            results['high_complexity_functions'].sort(key=lambda x: x['complexity'], reverse=True)
            
        except Exception as e:
            results['error'] = str(e)
        
        return results
