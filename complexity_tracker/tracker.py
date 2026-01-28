"""Main complexity tracker orchestrator."""
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from complexity_tracker.config import Config
from complexity_tracker.repository_manager import RepositoryManager
from complexity_tracker.analyzers.code_complexity import CodeComplexityAnalyzer
from complexity_tracker.analyzers.dependency_complexity import DependencyComplexityAnalyzer
from complexity_tracker.analyzers.documentation_tokens import DocumentationTokenAnalyzer


class ComplexityTracker:
    """Main complexity tracker class."""
    
    def __init__(self, config: Config):
        """Initialize complexity tracker.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.repository_manager = RepositoryManager(
            clone_directory=config.get('clone_directory', 'repos'),
            github_token=config.get('github.token')
        )
        
        # Initialize analyzers based on configuration
        self.analyzers = []
        if config.get('analysis.code_complexity', True):
            self.analyzers.append(
                CodeComplexityAnalyzer(
                    exclude_patterns=config.get('analysis.exclude_patterns', [])
                )
            )
        
        if config.get('analysis.dependency_complexity', True):
            self.analyzers.append(DependencyComplexityAnalyzer())
        
        if config.get('analysis.documentation_tokens', True):
            self.analyzers.append(DocumentationTokenAnalyzer())
        
        self.results: List[Dict[str, Any]] = []
    
    def setup_repositories(self):
        """Setup repositories based on configuration."""
        repo_config = self.config.get('repositories', {})
        repo_type = repo_config.get('type', 'list')
        
        if repo_type == 'list':
            # Add specific repositories from list
            repos = repo_config.get('repos', [])
            self.repository_manager.add_repositories_from_list(repos)
        
        elif repo_type == 'organization':
            # Add all repositories from organization
            org_name = repo_config.get('organization')
            if not org_name:
                raise ValueError("Organization name not specified in configuration")
            
            max_repos = repo_config.get('max_repos')
            self.repository_manager.add_repositories_from_organization(org_name, max_repos)
        
        else:
            raise ValueError(f"Unsupported repository type: {repo_type}")
    
    def clone_repositories(self):
        """Clone or update all repositories."""
        print("Cloning/updating repositories...")
        return self.repository_manager.clone_or_update_repositories()
    
    def analyze_repositories(self):
        """Analyze all repositories."""
        print("\nAnalyzing repositories...")
        repo_paths = self.repository_manager.get_repository_paths()
        
        for repo_path in repo_paths:
            print(f"\nAnalyzing: {repo_path.name}")
            repo_result = {
                'repository': repo_path.name,
                'path': str(repo_path),
                'timestamp': datetime.now().isoformat(),
                'analyses': {}
            }
            
            # Run all analyzers
            for analyzer in self.analyzers:
                analyzer_name = analyzer.get_name()
                print(f"  Running {analyzer_name} analyzer...")
                
                try:
                    analysis_result = analyzer.analyze(repo_path)
                    repo_result['analyses'][analyzer_name] = analysis_result
                except Exception as e:
                    print(f"  Error in {analyzer_name}: {e}")
                    repo_result['analyses'][analyzer_name] = {'error': str(e)}
            
            self.results.append(repo_result)
        
        return self.results
    
    def get_results(self) -> List[Dict[str, Any]]:
        """Get analysis results.
        
        Returns:
            List of repository analysis results
        """
        return self.results
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics across all repositories.
        
        Returns:
            Dictionary with summary statistics
        """
        summary = {
            'total_repositories': len(self.results),
            'timestamp': datetime.now().isoformat(),
            'aggregated_metrics': {}
        }
        
        # Aggregate metrics across all repositories
        for result in self.results:
            for analyzer_name, analysis in result['analyses'].items():
                if analyzer_name not in summary['aggregated_metrics']:
                    summary['aggregated_metrics'][analyzer_name] = {}
                
                # Aggregate different metrics based on analyzer type
                if analyzer_name == 'code_complexity':
                    for key in ['total_files', 'total_functions', 'total_complexity', 'total_lines_of_code']:
                        if key in analysis:
                            summary['aggregated_metrics'][analyzer_name][key] = \
                                summary['aggregated_metrics'][analyzer_name].get(key, 0) + analysis[key]
                    
                    # Track max complexity across all repos
                    if 'max_complexity' in analysis:
                        summary['aggregated_metrics'][analyzer_name]['max_complexity'] = max(
                            summary['aggregated_metrics'][analyzer_name].get('max_complexity', 0),
                            analysis['max_complexity']
                        )
                
                elif analyzer_name == 'dependency_complexity':
                    for key in ['total_dependencies', 'total_dependency_files']:
                        if key in analysis:
                            summary['aggregated_metrics'][analyzer_name][key] = \
                                summary['aggregated_metrics'][analyzer_name].get(key, 0) + analysis[key]
                
                elif analyzer_name == 'documentation_tokens':
                    for key in ['total_doc_files', 'total_tokens', 'total_characters', 'total_lines']:
                        if key in analysis:
                            summary['aggregated_metrics'][analyzer_name][key] = \
                                summary['aggregated_metrics'][analyzer_name].get(key, 0) + analysis[key]
        
        # Calculate overall complexity score (weighted average)
        if 'code_complexity' in summary['aggregated_metrics']:
            code_metrics = summary['aggregated_metrics']['code_complexity']
            if code_metrics.get('total_functions', 0) > 0:
                summary['aggregated_metrics']['code_complexity']['average_complexity'] = \
                    code_metrics['total_complexity'] / code_metrics['total_functions']
        
        return summary
    
    def run(self):
        """Run the complete complexity tracking workflow."""
        print("=" * 60)
        print("Complexity Tracker")
        print("=" * 60)
        
        # Setup repositories
        self.setup_repositories()
        
        # Clone/update repositories
        clone_results = self.clone_repositories()
        
        # Analyze repositories
        self.analyze_repositories()
        
        # Get summary
        summary = self.get_summary()
        
        print("\n" + "=" * 60)
        print("Analysis Complete")
        print("=" * 60)
        print(f"Total repositories analyzed: {summary['total_repositories']}")
        
        return self.results, summary
