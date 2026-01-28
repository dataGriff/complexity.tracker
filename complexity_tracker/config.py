"""Configuration management for complexity tracker."""
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class Config:
    """Configuration class for complexity tracker."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Path to configuration file (YAML or JSON)
        """
        self.config = {}
        if config_path:
            self.load(config_path)
        else:
            self._set_defaults()
    
    def _set_defaults(self):
        """Set default configuration values."""
        self.config = {
            "repositories": {
                "type": "list",  # Options: list, organization, all
                "repos": []
            },
            "github": {
                "token": None,  # Optional GitHub token
                "api_url": "https://api.github.com"
            },
            "analysis": {
                "code_complexity": True,
                "dependency_complexity": True,
                "documentation_tokens": True,
                "exclude_patterns": [
                    "*/test/*",
                    "*/tests/*",
                    "*/node_modules/*",
                    "*/vendor/*",
                    "*/.git/*"
                ]
            },
            "output": {
                "directory": "complexity_reports",
                "format": ["html", "json"],
                "charts": True
            },
            "clone_directory": "repos"
        }
    
    def load(self, config_path: str):
        """Load configuration from file.
        
        Args:
            config_path: Path to configuration file
        """
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(path, 'r') as f:
            if path.suffix in ['.yaml', '.yml']:
                loaded_config = yaml.safe_load(f)
            elif path.suffix == '.json':
                loaded_config = json.load(f)
            else:
                raise ValueError(f"Unsupported configuration format: {path.suffix}")
        
        self._set_defaults()
        self._merge_config(loaded_config)
    
    def _merge_config(self, loaded_config: Dict[str, Any]):
        """Merge loaded configuration with defaults.
        
        Args:
            loaded_config: Configuration loaded from file
        """
        def deep_merge(base: Dict, update: Dict) -> Dict:
            """Recursively merge dictionaries."""
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    deep_merge(base[key], value)
                else:
                    base[key] = value
            return base
        
        self.config = deep_merge(self.config, loaded_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., 'repositories.type')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., 'repositories.type')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def save(self, config_path: str):
        """Save configuration to file.
        
        Args:
            config_path: Path to save configuration
        """
        path = Path(config_path)
        with open(path, 'w') as f:
            if path.suffix in ['.yaml', '.yml']:
                yaml.dump(self.config, f, default_flow_style=False)
            elif path.suffix == '.json':
                json.dump(self.config, f, indent=2)
            else:
                raise ValueError(f"Unsupported configuration format: {path.suffix}")
