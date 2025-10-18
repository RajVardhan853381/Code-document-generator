"""
Universal Code Documentation Writer - Core Package
"""

__version__ = "1.0.0"
__author__ = "GenAI Documentation Team"
__description__ = "AI-powered multi-language code documentation generator"

from app.core.universal_analyzer import UniversalCodeAnalyzer, LanguageDetector
from app.core.llm import DocumentationGenerator, LLMService
from app.core.generators.readme_generator import READMEGenerator


__all__ = [
    'UniversalCodeAnalyzer',
    'LanguageDetector',
    'DocumentationGenerator',
    'LLMService',
    'READMEGenerator',
]
