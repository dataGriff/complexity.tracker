"""Chart generator for complexity visualizations."""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, Any, List


class ChartGenerator:
    """Generator for complexity charts."""
    
    def __init__(self, output_dir: Path):
        """Initialize chart generator.
        
        Args:
            output_dir: Directory to save charts
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_complexity_by_repo(self, results: List[Dict[str, Any]]):
        """Generate bar chart of complexity by repository.
        
        Args:
            results: List of repository analysis results
        """
        repos = []
        complexities = []
        
        for result in results:
            code_analysis = result['analyses'].get('code_complexity', {})
            if 'average_complexity' in code_analysis:
                repos.append(result['repository'])
                complexities.append(code_analysis['average_complexity'])
        
        if not repos:
            return
        
        plt.figure(figsize=(12, 6))
        plt.bar(repos, complexities, color='steelblue')
        plt.xlabel('Repository')
        plt.ylabel('Average Cyclomatic Complexity')
        plt.title('Average Code Complexity by Repository')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        output_file = self.output_dir / 'complexity_by_repo.png'
        plt.savefig(output_file, dpi=150)
        plt.close()
        
        print(f"Chart saved: {output_file}")
    
    def generate_dependencies_by_repo(self, results: List[Dict[str, Any]]):
        """Generate bar chart of dependencies by repository.
        
        Args:
            results: List of repository analysis results
        """
        repos = []
        deps = []
        
        for result in results:
            dep_analysis = result['analyses'].get('dependency_complexity', {})
            if 'total_dependencies' in dep_analysis:
                repos.append(result['repository'])
                deps.append(dep_analysis['total_dependencies'])
        
        if not repos:
            return
        
        plt.figure(figsize=(12, 6))
        plt.bar(repos, deps, color='coral')
        plt.xlabel('Repository')
        plt.ylabel('Number of Dependencies')
        plt.title('Dependencies by Repository')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        output_file = self.output_dir / 'dependencies_by_repo.png'
        plt.savefig(output_file, dpi=150)
        plt.close()
        
        print(f"Chart saved: {output_file}")
    
    def generate_documentation_by_repo(self, results: List[Dict[str, Any]]):
        """Generate bar chart of documentation tokens by repository.
        
        Args:
            results: List of repository analysis results
        """
        repos = []
        tokens = []
        
        for result in results:
            doc_analysis = result['analyses'].get('documentation_tokens', {})
            if 'total_tokens' in doc_analysis:
                repos.append(result['repository'])
                tokens.append(doc_analysis['total_tokens'])
        
        if not repos:
            return
        
        plt.figure(figsize=(12, 6))
        plt.bar(repos, tokens, color='mediumseagreen')
        plt.xlabel('Repository')
        plt.ylabel('Number of Documentation Tokens')
        plt.title('Documentation Tokens by Repository')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        output_file = self.output_dir / 'documentation_by_repo.png'
        plt.savefig(output_file, dpi=150)
        plt.close()
        
        print(f"Chart saved: {output_file}")
    
    def generate_complexity_distribution(self, results: List[Dict[str, Any]]):
        """Generate histogram of complexity distribution.
        
        Args:
            results: List of repository analysis results
        """
        all_complexities = []
        
        for result in results:
            code_analysis = result['analyses'].get('code_complexity', {})
            files = code_analysis.get('files_analyzed', [])
            for file_info in files:
                if file_info['functions'] > 0:
                    avg_complexity = file_info['complexity'] / file_info['functions']
                    all_complexities.append(avg_complexity)
        
        if not all_complexities:
            return
        
        plt.figure(figsize=(10, 6))
        plt.hist(all_complexities, bins=30, color='steelblue', edgecolor='black')
        plt.xlabel('Average Complexity per File')
        plt.ylabel('Frequency')
        plt.title('Distribution of Code Complexity')
        plt.tight_layout()
        
        output_file = self.output_dir / 'complexity_distribution.png'
        plt.savefig(output_file, dpi=150)
        plt.close()
        
        print(f"Chart saved: {output_file}")
    
    def generate_top_complex_functions(self, results: List[Dict[str, Any]], top_n: int = 10):
        """Generate chart of top complex functions across all repositories.
        
        Args:
            results: List of repository analysis results
            top_n: Number of top functions to display
        """
        all_functions = []
        
        for result in results:
            code_analysis = result['analyses'].get('code_complexity', {})
            high_complexity = code_analysis.get('high_complexity_functions', [])
            for func in high_complexity[:5]:  # Top 5 from each repo
                all_functions.append({
                    'label': f"{result['repository']}/{func['file']}/{func['function']}",
                    'complexity': func['complexity']
                })
        
        # Sort and get top N
        all_functions.sort(key=lambda x: x['complexity'], reverse=True)
        all_functions = all_functions[:top_n]
        
        if not all_functions:
            return
        
        labels = [f['label'] for f in all_functions]
        complexities = [f['complexity'] for f in all_functions]
        
        plt.figure(figsize=(12, 8))
        plt.barh(range(len(labels)), complexities, color='crimson')
        plt.yticks(range(len(labels)), labels, fontsize=8)
        plt.xlabel('Cyclomatic Complexity')
        plt.title(f'Top {top_n} Most Complex Functions')
        plt.tight_layout()
        
        output_file = self.output_dir / 'top_complex_functions.png'
        plt.savefig(output_file, dpi=150)
        plt.close()
        
        print(f"Chart saved: {output_file}")
    
    def generate_all_charts(self, results: List[Dict[str, Any]]):
        """Generate all available charts.
        
        Args:
            results: List of repository analysis results
        """
        print("\nGenerating charts...")
        self.generate_complexity_by_repo(results)
        self.generate_dependencies_by_repo(results)
        self.generate_documentation_by_repo(results)
        self.generate_complexity_distribution(results)
        self.generate_top_complex_functions(results)
