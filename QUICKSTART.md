# 🚀 Quick Start Guide
## Universal Multi-Language Code Documentation Writer

## ⚡ **YOUR PROJECT IS READY TO USE!** ✅

All tests passed! Your system is fully configured with:
- ✅ **API Key Configured** (Gemini 2.0 Flash)
- ✅ **All Dependencies Installed**
- ✅ **Sample Files Created**
- ✅ **Integration Tests Passed**

### 🎯 Get Started in 30 Seconds

Choose your preferred interface and start documenting:

---

## 🎨 Option 1: Web Interface (Recommended)

```bash
python3 main.py web
```

**Opens at:** http://localhost:8501

### Features:
- 📤 **Drag & drop** your code files
- 🎯 **Auto-detect** programming language
- 🤖 **AI-powered** documentation (2-3s per function)
- 📄 **Download** results instantly
- 🎨 **Beautiful UI** with dark mode

---

## 💻 Option 2: Command Line Interface

### Analyze a single file:
```bash
python3 -m app.cli analyze path/to/your/file.py
```

### Generate README for a project:
```bash
python3 -m app.cli readme path/to/your/project
```

### Document an entire repository:
```bash
python3 -m app.cli document path/to/repository
```

### See all commands:
```bash
python3 -m app.cli --help
```

---

## 🌐 Option 3: REST API

### Start the server:
```bash
python3 main.py api
```

### Access the API:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Example request:
```bash
curl -X POST "http://localhost:8000/api/analyze/file" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_code.py"
```

## Step 2: Configure API Key

Edit the `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

**Note**: Without an API key, the tool will generate placeholder documentation instead of AI-powered content.

## Step 3: Try It Out!

### Option 1: Command-Line Interface (CLI)

#### View Supported Languages
```bash
python -m app.cli languages
```

#### Analyze a Single File
```bash
python -m app.cli analyze sample_repos/python_samples/calculator.py
```

#### Analyze a Directory
```bash
python -m app.cli analyze sample_repos/ --recursive
```

#### Generate README
```bash
python -m app.cli readme sample_repos/ --output README_GENERATED.md
```

#### Document Specific Function
```bash
python -m app.cli document sample_repos/python_samples/calculator.py --function add
```

### Option 2: Web Interface (Streamlit)

Start the web application:
```bash
streamlit run app/web/streamlit_app.py
```

Then:
1. Open your browser to http://localhost:8501
2. Choose your mode (Analyze Files, Generate README, or Document Code Element)
3. Upload your code files
4. Click the generate button!

## Step 4: Test with Your Own Code

### Single File Analysis

Create a test file or use an existing one:

```bash
# Analyze your Python file
python -m app.cli analyze /path/to/your/file.py

# Analyze your JavaScript file
python -m app.cli analyze /path/to/your/file.js

# Analyze your Java file
python -m app.cli analyze /path/to/your/file.java
```

### Multi-File Project

```bash
# Analyze entire project directory
python -m app.cli analyze /path/to/your/project --recursive --output analysis.json
```

### Generate Project README

```bash
# Generate README for your project
python -m app.cli readme /path/to/your/project --name "My Awesome Project"
```

## Supported Languages

### Tier 1 (Full Support - MVP)
✅ Python  
✅ JavaScript  
✅ TypeScript  
✅ Java  
✅ C#  
✅ Go  
✅ PHP  
✅ Ruby  
✅ C++  

### Tier 2 (Extended Support)
🚧 Rust  
🚧 Swift  
🚧 Kotlin  
🚧 Dart  
🚧 Scala  
🚧 R  

## Example Workflow

### 1. Analyze Your Codebase

```bash
python -m app.cli analyze ./my-project --recursive
```

Output:
```
🔍 Analyzing: ./my-project

Language Distribution:
┌────────────┬───────┬────────────┐
│ Language   │ Files │ Percentage │
├────────────┼───────┼────────────┤
│ python     │ 45    │ 60.0%      │
│ javascript │ 25    │ 33.3%      │
│ typescript │ 5     │ 6.7%       │
└────────────┴───────┴────────────┘
```

### 2. Generate Documentation

```bash
# Generate README
python -m app.cli readme ./my-project --name "My Project" --output README.md

# Document specific files
python -m app.cli document ./my-project/main.py --function main
```

### 3. Review and Customize

The generated documentation will be in the appropriate format for each language:
- **Python**: Google-style docstrings
- **JavaScript/TypeScript**: JSDoc
- **Java**: Javadoc
- **C#**: XML documentation comments
- And more!

## Troubleshooting

### Issue: "Import errors" when running

**Solution**: Make sure you're in the virtual environment:
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Issue: "API key not configured"

**Solution**: Edit `.env` file and add your Gemini API key.

### Issue: "Language not supported"

**Solution**: Check the supported languages list. The file extension must match a supported language.

### Issue: "Module not found"

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

## Advanced Usage

### Custom Configuration

Edit `config/settings.yaml` to customize:
- Language-specific documentation formats
- LLM parameters (temperature, max tokens)
- Processing limits
- Exclude patterns

### Python API

Use the tool programmatically:

```python
from app.core.universal_analyzer import UniversalCodeAnalyzer
from app.core.llm import DocumentationGenerator

# Analyze code
analyzer = UniversalCodeAnalyzer()
result = analyzer.parse_file("my_file.py")

# Generate documentation
doc_gen = DocumentationGenerator()
documentation = doc_gen.generate_function_documentation(
    function_info=result['functions'][0],
    language='python'
)

print(documentation)
```

### Batch Processing

Process multiple files programmatically:

```python
from pathlib import Path
from app.core.universal_analyzer import UniversalCodeAnalyzer

analyzer = UniversalCodeAnalyzer()
repo_analysis = analyzer.analyze_repository("./my-project")

print(f"Total files: {repo_analysis['total_files']}")
print(f"Languages: {repo_analysis['language_stats']}")
```

## Next Steps

1. **Explore Documentation Formats**: Check `docs/language_support/` for format examples
2. **Read the Full README**: See `README.md` for comprehensive information
3. **API Reference**: Check `docs/api_reference/` for detailed API documentation
4. **Contributing**: See `docs/CONTRIBUTING.md` to contribute to the project

## Getting Help

- **Documentation**: Check the `docs/` directory
- **Examples**: See `sample_repos/` for example code
- **Issues**: Report bugs or request features on GitHub

---

## Summary: Your First Documentation in 3 Commands

```bash
# 1. Setup
python scripts/setup.py

# 2. Configure (edit .env and add API key)
nano .env

# 3. Generate!
python -m app.cli analyze sample_repos/python_samples/calculator.py
```

**Happy documenting! 📚✨**
