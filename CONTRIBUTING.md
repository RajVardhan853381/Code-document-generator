# Contributing to Universal Code Documentation Writer

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🎯 Project Vision

Our goal is to create a universal, AI-powered code documentation tool that works seamlessly across 15+ programming languages, making documentation effortless for developers worldwide.

## 📋 How to Contribute

### 1. Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/code-documentation-tool.git
   cd code-documentation-tool
   ```
3. **Set up the development environment**:
   ```bash
   python scripts/setup.py
   ```

### 2. Areas for Contribution

We welcome contributions in these areas:

#### 🌐 Language Support
- Add support for new programming languages
- Improve existing language parsers
- Add language-specific documentation format templates

#### 🤖 AI/LLM Integration
- Improve prompt engineering for better documentation
- Add support for new LLM providers
- Optimize API usage and caching

#### 🎨 User Interface
- Enhance the Streamlit web interface
- Improve CLI usability
- Add new visualization features

#### 🧪 Testing
- Write unit tests for language analyzers
- Add integration tests
- Create performance benchmarks

#### 📚 Documentation
- Improve user guides
- Add code examples
- Write language-specific documentation guides

#### 🐛 Bug Fixes
- Fix reported issues
- Improve error handling
- Enhance stability

### 3. Development Workflow

#### Creating a New Feature

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write code following our style guide
   - Add tests for new functionality
   - Update documentation

3. **Test your changes**:
   ```bash
   # Run tests
   pytest
   
   # Run linters
   black app/
   flake8 app/
   mypy app/
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add support for Kotlin language"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

### 4. Coding Standards

#### Python Style Guide

- Follow **PEP 8** style guide
- Use **type hints** for all functions
- Write **docstrings** for all public functions and classes
- Use **descriptive variable names**

Example:
```python
def analyze_code(file_path: str, language: str) -> Dict[str, Any]:
    """Analyze code file and extract structure.
    
    Args:
        file_path: Path to the code file
        language: Programming language name
        
    Returns:
        Dictionary containing analysis results
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If language is not supported
    """
    # Implementation here
    pass
```

#### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(analyzer): add Kotlin language support

Add Tree-sitter parser for Kotlin and implement
language-specific analysis features.

Closes #123
```

```
fix(llm): handle API timeout errors gracefully

Add retry logic and proper error handling for LLM API calls
to prevent application crashes on network issues.
```

### 5. Adding a New Language

To add support for a new programming language:

1. **Add language configuration** in `config/settings.yaml`:
   ```yaml
   languages:
     tier2:
       - kotlin  # Add new language
   
   documentation_formats:
     kotlin:
       default: "kdoc"
       supported: ["kdoc"]
   
   tree_sitter:
     languages:
       kotlin: "tree-sitter-kotlin"
   ```

2. **Create language analyzer** in `app/core/analyzers/`:
   ```python
   class KotlinAnalyzer(BaseAnalyzer):
       """Kotlin code analyzer."""
       
       def analyze(self, file_content: str, file_path: str) -> Dict[str, Any]:
           # Implementation
           pass
   ```

3. **Add formatter** in `app/core/formatters/`:
   ```python
   class KDocFormatter(BaseFormatter):
       """KDoc formatter for Kotlin."""
       
       def format_function_documentation(self, ...):
           # Implementation
           pass
   ```

4. **Add tests** in `tests/language_specific/`:
   ```python
   def test_kotlin_analyzer():
       # Test implementation
       pass
   ```

5. **Update documentation**:
   - Add language to README.md
   - Create language guide in `docs/language_support/kotlin.md`

### 6. Testing Guidelines

#### Writing Tests

- Write tests for all new features
- Use pytest for testing
- Aim for >85% code coverage
- Include both unit and integration tests

Example test:
```python
import pytest
from app.core.analyzers import KotlinAnalyzer

def test_kotlin_function_extraction():
    """Test extracting functions from Kotlin code."""
    analyzer = KotlinAnalyzer()
    
    kotlin_code = '''
    fun greet(name: String): String {
        return "Hello, $name!"
    }
    '''
    
    result = analyzer.analyze(kotlin_code, "test.kt")
    
    assert len(result['functions']) == 1
    assert result['functions'][0]['name'] == 'greet'
```

#### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_analyzer.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_analyzer.py::test_kotlin_function_extraction
```

### 7. Documentation Guidelines

- Keep documentation up-to-date
- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Update API documentation for new endpoints

### 8. Pull Request Process

1. **Ensure all tests pass**
2. **Update documentation** as needed
3. **Add your changes** to CHANGELOG.md
4. **Request review** from maintainers
5. **Address review comments**
6. **Maintainer will merge** when approved

#### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests added for new functionality
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Commit messages follow convention
- [ ] No merge conflicts

## 🏆 Recognition

Contributors will be:
- Listed in the project README
- Mentioned in release notes
- Credited in the documentation

## 📞 Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Create an Issue
- **Ideas**: Start a Discussion

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the project
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

---

**Questions?** Feel free to ask in GitHub Discussions or create an issue.
