"""
Universal Code Analyzer - Core module for multi-language code analysis.
Uses Tree-sitter for parsing and Guesslang for language detection.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import logging

try:
    from guesslang import Guess  # type: ignore[import]
    GUESSLANG_AVAILABLE = True
except ImportError:
    GUESSLANG_AVAILABLE = False
    Guess = None

try:
    from tree_sitter import Language, Parser, Node, Tree  # type: ignore[import]
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False
    Language = None
    Parser = None
    Node = None
    Tree = None

from config import get_config


logger = logging.getLogger(__name__)


class LanguageDetector:
    """Detects programming language using multiple methods."""
    
    # File extension to language mapping
    EXTENSION_MAP = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.cs': 'csharp',
        '.go': 'go',
        '.php': 'php',
        '.rb': 'ruby',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.hpp': 'cpp',
        '.h': 'cpp',
        '.rs': 'rust',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.kts': 'kotlin',
        '.dart': 'dart',
        '.scala': 'scala',
        '.r': 'r',
        '.R': 'r',
    }
    
    def __init__(self):
        """Initialize language detector."""
        self.guesslang = Guess() if GUESSLANG_AVAILABLE else None  # type: ignore[misc]
        self.config = get_config()
    
    def detect_language(self, file_content: str, file_path: Optional[str] = None) -> str:
        """Detect programming language using multiple methods.
        
        Args:
            file_content: Content of the file
            file_path: Path to the file (optional)
            
        Returns:
            Detected language name
        """
        detected_language = 'unknown'
        
        # Method 1: File extension mapping
        if file_path:
            extension = Path(file_path).suffix.lower()
            if extension in self.EXTENSION_MAP:
                detected_language = self.EXTENSION_MAP[extension]
                logger.debug(f"Detected {detected_language} from extension: {extension}")
        
        # Method 2: Content-based detection using Guesslang
        if detected_language == 'unknown' and file_content.strip() and self.guesslang:
            try:
                guessed_language = self.guesslang.language_name(file_content)
                if guessed_language:
                    detected_language = guessed_language.lower()
                    logger.debug(f"Detected {detected_language} using Guesslang")
            except Exception as e:
                logger.warning(f"Guesslang detection failed: {e}")
        
        # Method 3: Validate with supported languages
        if not self.config.is_language_supported(detected_language):
            logger.warning(f"Language {detected_language} is not supported")
            detected_language = 'unknown'
        
        return detected_language
    
    @staticmethod
    def get_language_from_extension(file_path: str) -> str:
        """Get language from file extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Language name or 'unknown'
        """
        extension = Path(file_path).suffix.lower()
        return LanguageDetector.EXTENSION_MAP.get(extension, 'unknown')


class CodeElement:
    """Represents a code element (function, class, method, etc.)."""
    
    def __init__(
        self,
        element_type: str,
        name: str,
        start_line: int,
        end_line: int,
        source_code: str,
        **kwargs
    ):
        """Initialize code element.
        
        Args:
            element_type: Type of element (function, class, method, etc.)
            name: Name of the element
            start_line: Starting line number
            end_line: Ending line number
            source_code: Source code of the element
            **kwargs: Additional attributes
        """
        self.element_type = element_type
        self.name = name
        self.start_line = start_line
        self.end_line = end_line
        self.source_code = source_code
        self.attributes = kwargs
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation.
        
        Returns:
            Dictionary representation
        """
        return {
            'type': self.element_type,
            'name': self.name,
            'start_line': self.start_line,
            'end_line': self.end_line,
            'source_code': self.source_code,
            **self.attributes
        }


class UniversalCodeAnalyzer:
    """Universal code analyzer supporting multiple programming languages."""
    
    def __init__(self):
        """Initialize universal code analyzer."""
        self.config = get_config()
        self.language_detector = LanguageDetector()
        self.parsers: Dict[str, Any] = {}  # Parser type when available
        self.languages: Dict[str, Any] = {}  # Language type when available
        
        # Initialize supported languages
        self._initialize_parsers()
    
    def _initialize_parsers(self) -> None:
        """Initialize Tree-sitter parsers for supported languages."""
        # This will be implemented with actual Tree-sitter bindings
        # For now, we'll set up the structure
        supported_languages = self.config.get_supported_languages()
        logger.info(f"Initializing parsers for {len(supported_languages)} languages")
        
        # Note: In production, this would load compiled Tree-sitter language bindings
        # For now, we're creating a placeholder structure
        if TREE_SITTER_AVAILABLE and Parser:
            for lang in supported_languages:
                parser = Parser()  # type: ignore[misc]
                self.parsers[lang] = parser
                logger.debug(f"Parser initialized for {lang}")
        else:
            logger.warning("Tree-sitter not available, using fallback analysis")
    
    def detect_language(self, file_content: str, file_path: Optional[str] = None) -> str:
        """Detect programming language.
        
        Args:
            file_content: Content of the file
            file_path: Path to the file
            
        Returns:
            Detected language name
        """
        return self.language_detector.detect_language(file_content, file_path)
    
    def parse_file(self, file_path: str, file_content: Optional[str] = None) -> Dict[str, Any]:
        """Parse a code file and extract structure.
        
        Args:
            file_path: Path to the file
            file_content: Content of the file (optional, will be read if not provided)
            
        Returns:
            Dictionary containing parsed code structure
        """
        # Read file content if not provided
        if file_content is None:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
        
        # Detect language
        language = self.detect_language(file_content, file_path)
        
        if language == 'unknown':
            logger.warning(f"Unknown language for file: {file_path}")
            return self._fallback_analysis(file_content, file_path)
        
        # Parse using language-specific analyzer
        try:
            result = self._parse_with_language(file_content, language, file_path)
            result['language'] = language
            result['file_path'] = file_path
            return result
        except Exception as e:
            logger.error(f"Parsing failed for {file_path}: {e}")
            return self._fallback_analysis(file_content, file_path)
    
    def _parse_with_language(
        self,
        file_content: str,
        language: str,
        file_path: str
    ) -> Dict[str, Any]:
        """Parse file using language-specific parser.
        
        Args:
            file_content: Content of the file
            language: Detected language
            file_path: Path to the file
            
        Returns:
            Parsed structure
        """
        # Import language-specific analyzer
        analyzer_module = self._get_language_analyzer(language)
        
        if analyzer_module:
            return analyzer_module.analyze(file_content, file_path)
        
        # Fallback to generic analysis
        return self._generic_analysis(file_content, language)
    
    def _get_language_analyzer(self, language: str):
        """Get language-specific analyzer module.
        
        Args:
            language: Programming language name
            
        Returns:
            Analyzer module or None
        """
        try:
            # Dynamically import language analyzer
            from app.core.analyzers import get_analyzer
            return get_analyzer(language)
        except ImportError:
            logger.warning(f"No specific analyzer found for {language}")
            return None
    
    def _generic_analysis(self, file_content: str, language: str) -> Dict[str, Any]:
        """Perform generic code analysis.
        
        Args:
            file_content: Content of the file
            language: Programming language
            
        Returns:
            Generic analysis result
        """
        lines = file_content.split('\n')
        
        return {
            'language': language,
            'line_count': len(lines),
            'functions': [],
            'classes': [],
            'imports': [],
            'exports': [],
            'raw_content': file_content
        }
    
    def _fallback_analysis(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """Fallback analysis for unknown languages.
        
        Args:
            file_content: Content of the file
            file_path: Path to the file
            
        Returns:
            Basic analysis result
        """
        return {
            'language': 'unknown',
            'file_path': file_path,
            'line_count': len(file_content.split('\n')),
            'error': 'Language not supported or could not be detected',
            'raw_content': file_content
        }
    
    def analyze_repository(self, repo_path: str) -> Dict[str, Any]:
        """Analyze an entire repository.
        
        Args:
            repo_path: Path to the repository
            
        Returns:
            Repository analysis including all files
        """
        repo_path_obj = Path(repo_path)
        
        if not repo_path_obj.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        # Find all code files
        code_files = self._find_code_files(repo_path_obj)
        
        # Analyze each file
        file_analyses = []
        language_stats = {}
        
        for file_path in code_files:
            try:
                analysis = self.parse_file(str(file_path))
                file_analyses.append(analysis)
                
                # Track language statistics
                lang = analysis.get('language', 'unknown')
                language_stats[lang] = language_stats.get(lang, 0) + 1
                
            except Exception as e:
                logger.error(f"Failed to analyze {file_path}: {e}")
        
        return {
            'repository_path': str(repo_path_obj),
            'total_files': len(code_files),
            'analyzed_files': len(file_analyses),
            'language_stats': language_stats,
            'files': file_analyses
        }
    
    def _find_code_files(self, repo_path: Path) -> List[Path]:
        """Find all code files in a repository.
        
        Args:
            repo_path: Path to the repository
            
        Returns:
            List of code file paths
        """
        code_files = []
        exclude_patterns = self.config.get('processing.exclude_patterns', [])
        supported_extensions = set(LanguageDetector.EXTENSION_MAP.keys())
        
        for file_path in repo_path.rglob('*'):
            # Skip directories
            if not file_path.is_file():
                continue
            
            # Skip excluded patterns
            if any(pattern in str(file_path) for pattern in exclude_patterns):
                continue
            
            # Check if extension is supported
            if file_path.suffix.lower() in supported_extensions:
                code_files.append(file_path)
        
        return code_files
