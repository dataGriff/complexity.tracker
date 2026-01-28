"""Repository management for cloning and managing code repositories."""
import os
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from git import Repo, GitCommandError
import requests


class RepositoryManager:
    """Manager for cloning and handling repositories."""
    
    def __init__(self, clone_directory: str = "repos", github_token: Optional[str] = None):
        """Initialize repository manager.
        
        Args:
            clone_directory: Directory to clone repositories into
            github_token: Optional GitHub token for API access
        """
        self.clone_directory = Path(clone_directory)
        self.clone_directory.mkdir(parents=True, exist_ok=True)
        self.github_token = github_token
        self.repos_info: List[Dict] = []
    
    def add_repository(self, repo_url: str, name: Optional[str] = None):
        """Add a repository to be analyzed.
        
        Args:
            repo_url: URL or full name of repository (e.g., 'owner/repo' or 'https://github.com/owner/repo')
            name: Optional custom name for the repository
        """
        # Normalize repo URL
        if not repo_url.startswith('http'):
            # Assume it's in the format 'owner/repo'
            repo_url = f"https://github.com/{repo_url}"
        
        # Extract name from URL if not provided
        if name is None:
            name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
        
        self.repos_info.append({
            'url': repo_url,
            'name': name,
            'local_path': self.clone_directory / name
        })
    
    def add_repositories_from_list(self, repo_list: List[str]):
        """Add multiple repositories from a list.
        
        Args:
            repo_list: List of repository URLs or names
        """
        for repo in repo_list:
            self.add_repository(repo)
    
    def add_repositories_from_organization(self, org_name: str, max_repos: Optional[int] = None):
        """Add all repositories from a GitHub organization.
        
        Args:
            org_name: GitHub organization name
            max_repos: Optional maximum number of repositories to fetch
        """
        api_url = f"https://api.github.com/orgs/{org_name}/repos"
        headers = {}
        if self.github_token:
            headers['Authorization'] = f"Bearer {self.github_token}"
        
        page = 1
        per_page = 100
        
        while True:
            params = {'page': page, 'per_page': per_page}
            response = requests.get(api_url, headers=headers, params=params, timeout=30)
            
            if response.status_code != 200:
                error_msg = f"Failed to fetch repositories for organization {org_name}: HTTP {response.status_code}"
                if response.status_code == 401:
                    error_msg += " - Authentication failed. Check your GitHub token."
                elif response.status_code == 403:
                    error_msg += " - Rate limit exceeded or insufficient permissions."
                elif response.status_code == 404:
                    error_msg += " - Organization not found."
                raise Exception(error_msg)
            
            repos = response.json()
            if not repos:
                break
            
            for repo in repos:
                if max_repos and len(self.repos_info) >= max_repos:
                    return
                self.add_repository(repo['clone_url'], repo['name'])
            
            if len(repos) < per_page:
                break
            
            page += 1
    
    def clone_or_update_repositories(self) -> List[Dict]:
        """Clone or update all added repositories.
        
        Returns:
            List of repository information with local paths
        """
        results = []
        
        for repo_info in self.repos_info:
            local_path = repo_info['local_path']
            
            try:
                if local_path.exists():
                    # Update existing repository
                    print(f"Updating repository: {repo_info['name']}")
                    repo = Repo(local_path)
                    origin = repo.remotes.origin
                    origin.pull()
                    status = "updated"
                else:
                    # Clone new repository
                    print(f"Cloning repository: {repo_info['name']}")
                    Repo.clone_from(repo_info['url'], local_path)
                    status = "cloned"
                
                results.append({
                    **repo_info,
                    'status': status,
                    'success': True
                })
            except GitCommandError as e:
                print(f"Error processing repository {repo_info['name']}: {e}")
                results.append({
                    **repo_info,
                    'status': 'error',
                    'success': False,
                    'error': str(e)
                })
        
        return results
    
    def get_repository_paths(self) -> List[Path]:
        """Get list of local paths for all repositories.
        
        Returns:
            List of Path objects for local repository directories
        """
        return [repo['local_path'] for repo in self.repos_info if repo['local_path'].exists()]
    
    def cleanup(self):
        """Remove all cloned repositories."""
        if self.clone_directory.exists():
            shutil.rmtree(self.clone_directory)
