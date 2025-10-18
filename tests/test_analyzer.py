"""
Basic tests for Universal Code Analyzer.
"""

import pytest  # type: ignore[import]
from pathlib import Path

from app.core.universal_analyzer import UniversalCodeAnalyzer, LanguageDetector


class TestLanguageDetector:
    """Test language detection functionality."""
    
    def test_detect_python_by_extension(self):
        """Test Python detection by file extension."""
        detector = LanguageDetector()
        
        language = detector.detect_language("", "test.py")
        assert language == "python"
    
    def test_detect_javascript_by_extension(self):
        """Test JavaScript detection by file extension."""
        detector = LanguageDetector()
        
        language = detector.detect_language("", "test.js")
        assert language == "javascript"
    
    def test_detect_typescript_by_extension(self):
        """Test TypeScript detection by file extension."""
        detector = LanguageDetector()
        
        language = detector.detect_language("", "test.ts")
        assert language == "typescript"
    
    def test_unknown_extension(self):
        """Test unknown file extension."""
        detector = LanguageDetector()
        
        language = detector.detect_language("", "test.xyz")
        assert language == "unknown"


class TestUniversalCodeAnalyzer:
    """Test universal code analyzer."""
    
    def test_analyzer_initialization(self):
        """Test analyzer can be initialized."""
        analyzer = UniversalCodeAnalyzer()
        assert analyzer is not None
    
    def test_parse_python_code(self):
        """Test parsing Python code."""
        analyzer = UniversalCodeAnalyzer()
        
        python_code = '''
def hello(name):
    """Say hello."""
    return f"Hello, {name}!"

class Greeter:
    """A greeter class."""
    def greet(self, name):
        return hello(name)
'''
        
        result = analyzer.parse_file("test.py", python_code)
        
        assert result['language'] == 'python'
        assert len(result['functions']) >= 1
        assert len(result['classes']) >= 1
    
    def test_parse_javascript_code(self):
        """Test parsing JavaScript code."""
        analyzer = UniversalCodeAnalyzer()
        
        js_code = '''
function add(a, b) {
    return a + b;
}

class Calculator {
    constructor() {
        this.result = 0;
    }
}
'''
        
        result = analyzer.parse_file("test.js", js_code)
        
        assert result['language'] == 'javascript'
        assert len(result['functions']) >= 1
        assert len(result['classes']) >= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
