"""Documentation token analyzer."""
import os
from pathlib import Path
from typing import Dict, Any, List
from complexity_tracker.analyzers import BaseAnalyzer


class DocumentationTokenAnalyzer(BaseAnalyzer):
    """Analyzer for counting tokens in documentation files."""
    
    # Documentation file extensions
    DOC_EXTENSIONS = ['.md', '.rst', '.txt', '.adoc', '.asciidoc']
    
    # Common documentation directories
    DOC_DIRS = ['docs', 'doc', 'documentation', 'wiki']
    
    def get_name(self) -> str:
        """Get analyzer name."""
        return "documentation_tokens"
    
    def analyze(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze documentation token count in repository.
        
        Args:
            repo_path: Path to repository
            
        Returns:
            Dictionary with documentation metrics
        """
        results = {
            'total_doc_files': 0,
            'total_tokens': 0,
            'total_characters': 0,
            'total_lines': 0,
            'average_tokens_per_file': 0,
            'doc_files_by_type': {},
            'largest_doc_files': [],
            'documentation_files': []
        }
        
        try:
            # Search for documentation files
            for root, dirs, files in os.walk(repo_path):
                # Skip hidden directories and common ignore patterns
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'vendor', '__pycache__']]
                
                current_path = Path(root)
                relative_root = current_path.relative_to(repo_path) if current_path != repo_path else Path('.')
                
                # Check if we're in a documentation directory
                is_doc_dir = any(doc_dir in str(relative_root).lower() for doc_dir in self.DOC_DIRS)
                
                for file in files:
                    file_path = Path(root) / file
                    ext = file_path.suffix.lower()
                    
                    # Include README files and files with doc extensions, or files in doc directories with text extensions
                    if (ext in self.DOC_EXTENSIONS or 
                        file.upper().startswith('README') or 
                        (is_doc_dir and ext in self.DOC_EXTENSIONS)):
                        
                        try:
                            content = file_path.read_text(encoding='utf-8', errors='ignore')
                            
                            # Count tokens (simple whitespace tokenization)
                            tokens = len(content.split())
                            characters = len(content)
                            lines = len(content.split('\n'))
                            
                            if tokens > 0:  # Only count non-empty files
                                results['total_doc_files'] += 1
                                results['total_tokens'] += tokens
                                results['total_characters'] += characters
                                results['total_lines'] += lines
                                
                                # Track by file type
                                if ext not in results['doc_files_by_type']:
                                    results['doc_files_by_type'][ext] = {
                                        'files': 0,
                                        'tokens': 0
                                    }
                                
                                results['doc_files_by_type'][ext]['files'] += 1
                                results['doc_files_by_type'][ext]['tokens'] += tokens
                                
                                doc_file_info = {
                                    'path': str(file_path.relative_to(repo_path)),
                                    'tokens': tokens,
                                    'characters': characters,
                                    'lines': lines,
                                    'type': ext
                                }
                                
                                results['documentation_files'].append(doc_file_info)
                                results['largest_doc_files'].append(doc_file_info)
                        
                        except Exception:
                            # Skip files that can't be read
                            continue
            
            # Calculate average
            if results['total_doc_files'] > 0:
                results['average_tokens_per_file'] = results['total_tokens'] / results['total_doc_files']
            
            # Sort largest doc files by token count
            results['largest_doc_files'].sort(key=lambda x: x['tokens'], reverse=True)
            results['largest_doc_files'] = results['largest_doc_files'][:10]  # Keep top 10
        
        except Exception as e:
            results['error'] = str(e)
        
        return results
