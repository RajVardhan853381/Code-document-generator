# 🚀 Universal Multi-Language GenAI Code Documentation Writer

An AI-powered tool that analyzes codebases in **15+ programming languages** and automatically generates comprehensive docstrings/comments and README files.

## 🌟 Features

### Multi-Language Support
- **Tier 1 Languages (MVP)**: Python, JavaScript, TypeScript, Java, C#, Go, PHP, Ruby, C++
- **Tier 2 Languages**: Rust, Swift, Kotlin, Dart, Scala, R
- **Automatic Language Detection**: Using Guesslang + file extension analysis
- **Universal Parsing**: Powered by Tree-sitter for accurate AST analysis

### Intelligent Documentation Generation
- **Language-Specific Formats**: JSDoc, Javadoc, Sphinx, XML Documentation, PHPDoc, YARD, Rustdoc, and more
- **Context-Aware AI**: Gemini API integration with language-specific prompts
- **Format Compliance**: Follows established standards for each language

### Advanced Features
- **Multi-Language README Generation**: Comprehensive project documentation
- **Cross-Language Analysis**: Understand multi-language repository architecture
- **Batch Processing**: Handle entire repositories efficiently
- **Export Options**: Maintain original file structure with generated documentation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           WEB INTERFACE                     │
│     (Multi-language file upload)            │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│          FASTAPI BACKEND                    │
│  - Multi-file Upload Handler                │
│  - Language Detection Service               │
│  - Task Queue for Batch Processing          │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│     UNIVERSAL CODE ANALYZER                 │
│  - Tree-sitter Multi-language Parser        │
│  - Language Detection (Guesslang)           │
│  - Universal AST Walker                     │
│  - Code Structure Extractor                 │
└──────────────────┬──────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼────┐  ┌──────▼──────┐  ┌───▼────┐
│Prompt  │  │     LLM     │  │Doc     │
│Engine  │  │  (Gemini)   │  │Format  │
└────────┘  └─────────────┘  └────────┘
```

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.9+
Git
```

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd "Code Documentation Tool"
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

5. **Install Tree-sitter language parsers**
```bash
python scripts/setup_parsers.py
```

### Usage

#### Web Interface (Streamlit)
```bash
streamlit run app/web/streamlit_app.py
```

#### CLI Interface
```bash
# Analyze a single file
python -m app.cli analyze path/to/file.py

# Analyze entire directory
python -m app.cli analyze path/to/project/ --recursive

# Generate README
python -m app.cli readme path/to/project/
```

#### API Server (FastAPI)
```bash
uvicorn app.api.main:app --reload
# Access API docs at http://localhost:8000/docs
```

## 📁 Project Structure

```
Code Documentation Tool/
├── app/
│   ├── core/
│   │   ├── analyzers/          # Language-specific code analyzers
│   │   ├── formatters/         # Documentation format generators
│   │   ├── parsers/            # Tree-sitter parser management
│   │   ├── generators/         # Documentation generators
│   │   └── llm/                # LLM integration
│   ├── api/                    # FastAPI backend
│   ├── web/                    # Streamlit web interface
│   └── cli/                    # Command-line interface
├── tests/                      # Test suite
├── config/                     # Configuration files
├── scripts/                    # Setup and utility scripts
├── sample_repos/               # Sample test repositories
└── docs/                       # Documentation
```

## 🎯 Supported Languages & Formats

| Language       | Documentation Format | Status |
|----------------|---------------------|--------|
| JavaScript/TS  | JSDoc               | ✅     |
| Python         | Sphinx/Google       | ✅     |
| Java           | Javadoc             | ✅     |
| C#             | XML Documentation   | ✅     |
| Go             | Go Comments         | ✅     |
| PHP            | PHPDoc              | ✅     |
| Ruby           | YARD                | ✅     |
| C++            | Doxygen             | ✅     |
| Rust           | Rustdoc             | ✅     |
| Swift          | Swift DocC          | 🚧     |
| Kotlin         | KDoc                | 🚧     |

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/language_specific/
pytest tests/integration/
pytest tests/performance/

# Run with coverage
pytest --cov=app --cov-report=html
```

## 🔧 Configuration

Edit `config/settings.yaml` to customize:
- Supported languages
- Documentation formats
- LLM parameters
- Processing limits
- Export options

## 📊 Performance Targets

- **Single Language Repository (50 files)**: < 90 seconds
- **Multi-Language Repository (100 files)**: < 3 minutes
- **Large Repository (500 files)**: < 10 minutes
- **Language Detection Accuracy**: >90%
- **Documentation Quality**: >85% contextually correct

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Tree-sitter for universal parsing capabilities
- Guesslang for ML-based language detection
- Google Gemini API for AI-powered documentation generation

## 📞 Support

- Documentation: [docs/](docs/)
- Issues: GitHub Issues
- Discussions: GitHub Discussions

---

Built with ❤️ by the GenAI Documentation Team
