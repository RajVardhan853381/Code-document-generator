"""
Configuration management for the Universal Code Documentation Writer.
Handles loading and validation of configuration from multiple sources.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml  # type: ignore[import]
from pydantic import Field  # type: ignore[import]
from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore[import]


class AppSettings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    
    # Environment
    environment: str = "development"
    
    # API Keys  
    gemini_api_key: str = ""
    openai_api_key: str = ""
    
    # Database
    database_url: str = "sqlite:///./code_doc.db"
    redis_url: str = "redis://localhost:6379/0"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    api_workers: int = 4
    
    # Streamlit Configuration
    streamlit_port: int = 8501
    streamlit_server_address: str = "localhost"
    
    # LLM Configuration
    default_llm_provider: str = "gemini"
    llm_temperature: float = 0.3
    llm_max_tokens: int = 2048
    llm_timeout: int = 30
    
    # Processing Configuration
    max_file_size_mb: int = 10
    max_files_per_batch: int = 100
    enable_parallel_processing: bool = True
    max_workers: int = 4
    
    # Language Support
    supported_languages: str = "python,javascript,typescript,java,csharp,go,php,ruby,cpp,rust,swift,kotlin"
    
    # Storage Configuration
    upload_dir: str = "./uploads"
    output_dir: str = "./outputs"
    temp_dir: str = "./temp"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    # Security
    secret_key: str = "change-me-in-production"
    allowed_origins: str = "http://localhost:3000,http://localhost:8501"
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    
    # Feature Flags
    enable_cross_language_analysis: bool = True
    enable_readme_generation: bool = True
    enable_quality_scoring: bool = False
    
    def get_supported_languages_list(self) -> List[str]:
        """Get list of supported languages."""
        return [lang.strip() for lang in self.supported_languages.split(",")]
    
    def get_allowed_origins_list(self) -> List[str]:
        """Get list of allowed CORS origins."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


class ConfigManager:
    """Manages application configuration from multiple sources."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to YAML configuration file
        """
        self.config_path = config_path or Path(__file__).parent / "settings.yaml"
        self.settings = AppSettings()
        self._yaml_config: Dict[str, Any] = {}
        
        if self.config_path.exists():
            self._load_yaml_config()
    
    def _load_yaml_config(self) -> None:
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            self._yaml_config = yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        # Check environment settings first
        if hasattr(self.settings, key.replace('.', '_')):
            return getattr(self.settings, key.replace('.', '_'))
        
        # Check YAML config
        keys = key.split('.')
        value = self._yaml_config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_language_config(self, language: str) -> Dict[str, Any]:
        """Get configuration for a specific programming language.
        
        Args:
            language: Programming language name
            
        Returns:
            Language-specific configuration
        """
        return {
            'documentation_format': self.get(f'documentation_formats.{language}.default', 'standard'),
            'supported_formats': self.get(f'documentation_formats.{language}.supported', ['standard']),
            'tree_sitter_parser': self.get(f'tree_sitter.languages.{language}', None),
        }
    
    def get_llm_config(self, provider: Optional[str] = None) -> Dict[str, Any]:
        """Get LLM configuration.
        
        Args:
            provider: LLM provider name (defaults to configured provider)
            
        Returns:
            LLM configuration
        """
        provider = provider or self.settings.default_llm_provider
        return self.get(f'llm.providers.{provider}', {})
    
    def get_processing_config(self) -> Dict[str, Any]:
        """Get processing configuration.
        
        Returns:
            Processing configuration
        """
        return {
            'max_file_size_mb': self.settings.max_file_size_mb,
            'max_files_per_batch': self.settings.max_files_per_batch,
            'parallel_processing': self.settings.enable_parallel_processing,
            'max_workers': self.settings.max_workers,
            'timeout_seconds': self.get('processing.timeout_seconds', 300),
            'exclude_patterns': self.get('processing.exclude_patterns', []),
        }
    
    def get_supported_languages(self, tier: Optional[str] = None) -> List[str]:
        """Get list of supported programming languages.
        
        Args:
            tier: Language tier (tier1, tier2, tier3) or None for all
            
        Returns:
            List of supported languages
        """
        if tier:
            return self.get(f'languages.{tier}', [])
        
        all_languages = []
        for t in ['tier1', 'tier2', 'tier3']:
            all_languages.extend(self.get(f'languages.{t}', []))
        
        return all_languages
    
    def is_language_supported(self, language: str) -> bool:
        """Check if a language is supported.
        
        Args:
            language: Programming language name
            
        Returns:
            True if language is supported
        """
        return language.lower() in [lang.lower() for lang in self.get_supported_languages()]
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration.
        
        Returns:
            Output configuration
        """
        return self.get('output', {
            'preserve_structure': True,
            'create_backup': True,
            'overwrite_existing': False,
            'include_timestamp': True,
            'export_formats': ['markdown', 'html', 'json']
        })
    
    def get_readme_config(self) -> Dict[str, Any]:
        """Get README generation configuration.
        
        Returns:
            README configuration
        """
        return self.get('readme', {
            'sections': ['overview', 'architecture', 'setup', 'usage', 'api'],
            'include_badges': True,
            'include_toc': True,
            'include_examples': True
        })


# Global configuration instance
_config_manager: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """Get global configuration manager instance.
    
    Returns:
        ConfigManager instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def reload_config(config_path: Optional[Path] = None) -> None:
    """Reload configuration from file.
    
    Args:
        config_path: Path to configuration file
    """
    global _config_manager
    _config_manager = ConfigManager(config_path)


# Export settings for direct access
settings = AppSettings()
