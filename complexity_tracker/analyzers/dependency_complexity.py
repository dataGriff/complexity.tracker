"""Dependency complexity analyzer."""
import os
import json
from pathlib import Path
from typing import Dict, Any, List
from complexity_tracker.analyzers import BaseAnalyzer


class DependencyComplexityAnalyzer(BaseAnalyzer):
    """Analyzer for dependency complexity across different package managers."""
    
    # Mapping of dependency files to their package managers
    DEPENDENCY_FILES = {
        'package.json': 'npm',
        'package-lock.json': 'npm',
        'requirements.txt': 'pip',
        'Pipfile': 'pip',
        'Pipfile.lock': 'pip',
        'poetry.lock': 'poetry',
        'pyproject.toml': 'poetry',
        'Gemfile': 'bundler',
        'Gemfile.lock': 'bundler',
        'pom.xml': 'maven',
        'build.gradle': 'gradle',
        'build.gradle.kts': 'gradle',
        'Cargo.toml': 'cargo',
        'Cargo.lock': 'cargo',
        'go.mod': 'go',
        'go.sum': 'go',
        'composer.json': 'composer',
        'composer.lock': 'composer',
        'yarn.lock': 'yarn',
        'pubspec.yaml': 'dart',
        'packages.config': 'nuget',
        'project.json': 'nuget',
    }
    
    def get_name(self) -> str:
        """Get analyzer name."""
        return "dependency_complexity"
    
    def analyze(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze dependency complexity in repository.
        
        Args:
            repo_path: Path to repository
            
        Returns:
            Dictionary with dependency metrics
        """
        results = {
            'total_dependencies': 0,
            'total_dependency_files': 0,
            'dependencies_by_manager': {},
            'dependency_files': []
        }
        
        try:
            # Search for dependency files
            for root, dirs, files in os.walk(repo_path):
                # Skip common directories
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'vendor', '__pycache__', '.venv', 'venv']]
                
                for file in files:
                    if file in self.DEPENDENCY_FILES:
                        file_path = Path(root) / file
                        package_manager = self.DEPENDENCY_FILES[file]
                        
                        # Count dependencies
                        dep_count = self._count_dependencies(file_path, package_manager)
                        
                        if dep_count > 0:
                            results['total_dependency_files'] += 1
                            results['total_dependencies'] += dep_count
                            
                            # Track by package manager
                            if package_manager not in results['dependencies_by_manager']:
                                results['dependencies_by_manager'][package_manager] = {
                                    'files': 0,
                                    'dependencies': 0
                                }
                            
                            results['dependencies_by_manager'][package_manager]['files'] += 1
                            results['dependencies_by_manager'][package_manager]['dependencies'] += dep_count
                            
                            results['dependency_files'].append({
                                'path': str(file_path.relative_to(repo_path)),
                                'package_manager': package_manager,
                                'dependencies': dep_count
                            })
        
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def _count_dependencies(self, file_path: Path, package_manager: str) -> int:
        """Count dependencies in a dependency file.
        
        Args:
            file_path: Path to dependency file
            package_manager: Type of package manager
            
        Returns:
            Number of dependencies
        """
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # JSON-based files
            if file_path.name in ['package.json', 'composer.json', 'project.json']:
                try:
                    data = json.loads(content)
                    count = 0
                    if 'dependencies' in data:
                        count += len(data['dependencies'])
                    if 'devDependencies' in data:
                        count += len(data['devDependencies'])
                    if 'peerDependencies' in data:
                        count += len(data['peerDependencies'])
                    if 'require' in data:  # Composer
                        count += len(data['require'])
                    if 'require-dev' in data:  # Composer
                        count += len(data['require-dev'])
                    return count
                except json.JSONDecodeError:
                    return 0
            
            # Line-based files (requirements.txt, go.mod, etc.)
            elif file_path.name in ['requirements.txt', 'Pipfile']:
                lines = [line.strip() for line in content.split('\n')]
                # Count non-empty, non-comment lines with version specifiers
                return len([line for line in lines if line and not line.startswith('#') and not line.startswith('[') and ('==' in line or '>=' in line or '~=' in line)])
            
            # Lock files (approximate count from content)
            elif 'lock' in file_path.name.lower():
                # For lock files, count package entries (rough estimate)
                if package_manager == 'npm':
                    try:
                        data = json.loads(content)
                        if 'packages' in data:
                            return len(data['packages'])
                        elif 'dependencies' in data:
                            return len(data['dependencies'])
                    except:
                        pass
                # For other lock files, count lines with package indicators
                return len([line for line in content.split('\n') if line.strip() and (
                    line.strip().startswith('name =') or 
                    line.strip().startswith('name:') or
                    '[[package]]' in line
                )])
            
            # TOML files
            elif file_path.suffix == '.toml':
                # Count dependencies sections
                lines = [line.strip() for line in content.split('\n')]
                count = 0
                in_deps_section = False
                for line in lines:
                    if '[dependencies]' in line or '[dev-dependencies]' in line:
                        in_deps_section = True
                    elif line.startswith('[') and in_deps_section:
                        in_deps_section = False
                    elif in_deps_section and '=' in line and not line.startswith('#'):
                        count += 1
                return count
            
            # Go mod files
            elif file_path.name == 'go.mod':
                lines = [line.strip() for line in content.split('\n')]
                return len([line for line in lines if line and not line.startswith('//') and 'require' not in line and 'module' not in line and 'go ' not in line and line.endswith(')')])
            
            # XML files (pom.xml)
            elif file_path.suffix == '.xml':
                # Simple count of <dependency> tags
                return content.count('<dependency>')
            
            # Gradle files
            elif 'gradle' in file_path.name:
                lines = [line.strip() for line in content.split('\n')]
                return len([line for line in lines if 'implementation' in line or 'api' in line or 'compile' in line])
            
            # Gemfile
            elif file_path.name.startswith('Gemfile'):
                lines = [line.strip() for line in content.split('\n')]
                return len([line for line in lines if line.startswith('gem ') and "'" in line])
            
            # YAML files
            elif file_path.suffix in ['.yaml', '.yml']:
                lines = [line.strip() for line in content.split('\n')]
                # Count dependency-like entries
                return len([line for line in lines if ':' in line and not line.startswith('#') and 'dependencies' not in line])
        
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            return 0
        
        return 0
