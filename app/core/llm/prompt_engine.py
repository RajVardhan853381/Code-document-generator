"""
Multi-Language Prompt Engine for generating language-specific documentation prompts.
"""

from typing import Dict, Any, List, Optional
import logging
from pathlib import Path

from config import get_config


logger = logging.getLogger(__name__)


class MultiLanguagePromptEngine:
    """Generates language-specific prompts for documentation generation."""
    
    def __init__(self):
        """Initialize prompt engine."""
        self.config = get_config()
        self.prompt_templates = self._load_prompt_templates()
    
    def _load_prompt_templates(self) -> Dict[str, str]:
        """Load prompt templates from configuration."""
        return {
            'function_analysis': self._get_function_analysis_template(),
            'class_analysis': self._get_class_analysis_template(),
            'readme_generation': self._get_readme_generation_template(),
            'module_documentation': self._get_module_documentation_template(),
        }
    
    def _get_function_analysis_template(self) -> str:
        """Get function analysis prompt template."""
        return """Analyze the following {language} function and generate comprehensive documentation.

**Function Details:**
- Name: {function_name}
- Parameters: {parameters}
- Return Type: {return_type}
- Context: {context}

**Current Code:**
```{language}
{source_code}
```

**Task:** Generate documentation in {doc_format} format that includes:

1. **Brief Description**: One-line summary of what the function does
2. **Detailed Explanation**: Comprehensive description of functionality
3. **Parameters**: Detailed description of each parameter with types and purpose
4. **Returns**: Description of return value and type
5. **Exceptions/Errors**: Any exceptions or errors that might be raised
6. **Examples**: Usage example if applicable
7. **Notes**: Any important notes, side effects, or considerations

**Important**: 
- Follow {doc_format} conventions strictly
- Be concise but comprehensive
- Use proper formatting for {language}
- Include type information where available
"""
    
    def _get_class_analysis_template(self) -> str:
        """Get class analysis prompt template."""
        return """Analyze the following {language} class and generate comprehensive documentation.

**Class Details:**
- Name: {class_name}
- Methods: {method_count} methods
- Inheritance: {inheritance_info}
- Context: {context}

**Current Code:**
```{language}
{source_code}
```

**Task:** Generate documentation in {doc_format} format covering:

1. **Class Overview**: Purpose and responsibility of the class
2. **Constructor**: Description of initialization parameters
3. **Attributes/Properties**: Key instance variables and their purposes
4. **Methods Summary**: Brief description of each public method
5. **Usage Example**: Example of how to instantiate and use the class
6. **Inheritance**: Information about parent classes and interfaces
7. **Notes**: Design patterns, threading considerations, etc.

**Important**: 
- Follow {doc_format} conventions for {language}
- Focus on public API
- Explain relationships and dependencies
- Include type information for statically-typed languages
"""
    
    def _get_readme_generation_template(self) -> str:
        """Get README generation prompt template."""
        return """Generate a comprehensive README.md for a multi-language software project.

**Project Analysis:**
- Languages Detected: {languages}
- Primary Language: {primary_language}
- Total Files: {file_count}
- Architecture Type: {architecture_type}

**Key Components:**
{components}

**Technology Stack:**
{tech_stack}

**Project Structure:**
```
{structure}
```

**Task:** Create a professional README.md with the following sections:

1. **Project Title & Description**
   - Clear, concise project name
   - One-paragraph project overview
   - Key features (bullet points)

2. **Architecture Overview**
   - Explain the multi-language architecture
   - Component relationships
   - System design diagram (text-based)

3. **Technology Stack**
   - List all programming languages used
   - Major frameworks and libraries
   - Database and infrastructure

4. **Getting Started**
   - Prerequisites for each language environment
   - Installation steps
   - Configuration requirements

5. **Usage**
   - Basic usage examples
   - API documentation (if applicable)
   - CLI commands (if applicable)

6. **Project Structure**
   - Directory organization
   - Key files and their purposes

7. **Development**
   - Setup development environment
   - Running tests
   - Contributing guidelines

8. **Deployment** (if applicable)
   - Deployment steps
   - Environment variables
   - Production considerations

9. **License & Contact**
   - License information
   - How to contribute
   - Contact information

**Important**:
- Use clear, professional language
- Include code examples where helpful
- Add badges for build status, version, etc.
- Make it accessible for developers of all skill levels
- Highlight the multi-language nature as a feature
"""
    
    def _get_module_documentation_template(self) -> str:
        """Get module documentation prompt template."""
        return """Analyze the following {language} module/file and generate module-level documentation.

**Module Details:**
- File: {file_name}
- Language: {language}
- Functions: {function_count}
- Classes: {class_count}
- Dependencies: {imports}

**Module Overview:**
{module_summary}

**Task:** Generate module-level documentation that includes:

1. **Module Purpose**: What this module does and why it exists
2. **Key Components**: Overview of main functions and classes
3. **Dependencies**: External libraries and internal imports
4. **Usage**: How to import and use this module
5. **Examples**: Common usage patterns

**Format**: Use {doc_format} conventions for {language}
"""
    
    def generate_function_prompt(
        self,
        function_info: Dict[str, Any],
        language: str,
        context: Optional[str] = None
    ) -> str:
        """Generate prompt for function documentation.
        
        Args:
            function_info: Dictionary containing function information
            language: Programming language
            context: Additional context about the function
            
        Returns:
            Generated prompt string
        """
        doc_format = self._get_doc_format_for_language(language)
        
        # Extract parameter information
        parameters = function_info.get('parameters', [])
        param_str = ', '.join([
            f"{p.get('name', 'arg')} ({p.get('type', 'any')})"
            for p in parameters
        ]) if parameters else 'None'
        
        # Extract return type
        return_type = function_info.get('return_type', 'unknown')
        
        template = self.prompt_templates['function_analysis']
        
        return template.format(
            language=language,
            function_name=function_info.get('name', 'unknown'),
            parameters=param_str,
            return_type=return_type,
            context=context or 'No additional context provided',
            source_code=function_info.get('source_code', ''),
            doc_format=doc_format
        )
    
    def generate_class_prompt(
        self,
        class_info: Dict[str, Any],
        language: str,
        context: Optional[str] = None
    ) -> str:
        """Generate prompt for class documentation.
        
        Args:
            class_info: Dictionary containing class information
            language: Programming language
            context: Additional context about the class
            
        Returns:
            Generated prompt string
        """
        doc_format = self._get_doc_format_for_language(language)
        
        # Extract inheritance information
        bases = class_info.get('bases', [])
        inheritance_info = ', '.join(bases) if bases else 'No inheritance'
        
        # Count methods
        methods = class_info.get('methods', [])
        method_count = len(methods)
        
        template = self.prompt_templates['class_analysis']
        
        return template.format(
            language=language,
            class_name=class_info.get('name', 'unknown'),
            method_count=method_count,
            inheritance_info=inheritance_info,
            context=context or 'No additional context provided',
            source_code=class_info.get('source_code', ''),
            doc_format=doc_format
        )
    
    def generate_readme_prompt(
        self,
        repository_analysis: Dict[str, Any]
    ) -> str:
        """Generate prompt for README creation.
        
        Args:
            repository_analysis: Dictionary containing repository analysis
            
        Returns:
            Generated prompt string
        """
        # Extract language statistics
        language_stats = repository_analysis.get('language_stats', {})
        languages = ', '.join(language_stats.keys())
        
        # Determine primary language
        primary_language = max(language_stats.items(), key=lambda x: x[1])[0] if language_stats else 'unknown'
        
        # Extract components
        components = self._summarize_components(repository_analysis)
        
        # Determine architecture type
        architecture_type = self._infer_architecture_type(repository_analysis)
        
        # Generate tech stack summary
        tech_stack = self._generate_tech_stack_summary(repository_analysis)
        
        # Generate structure summary
        structure = self._generate_structure_summary(repository_analysis)
        
        template = self.prompt_templates['readme_generation']
        
        return template.format(
            languages=languages,
            primary_language=primary_language,
            file_count=repository_analysis.get('total_files', 0),
            architecture_type=architecture_type,
            components=components,
            tech_stack=tech_stack,
            structure=structure
        )
    
    def generate_module_prompt(
        self,
        file_analysis: Dict[str, Any],
        language: str
    ) -> str:
        """Generate prompt for module documentation.
        
        Args:
            file_analysis: Dictionary containing file analysis
            language: Programming language
            
        Returns:
            Generated prompt string
        """
        doc_format = self._get_doc_format_for_language(language)
        
        template = self.prompt_templates['module_documentation']
        
        return template.format(
            language=language,
            file_name=file_analysis.get('file_path', 'unknown'),
            function_count=len(file_analysis.get('functions', [])),
            class_count=len(file_analysis.get('classes', [])),
            imports=', '.join([str(imp) for imp in file_analysis.get('imports', [])]),
            module_summary=self._generate_module_summary(file_analysis),
            doc_format=doc_format
        )
    
    def _get_doc_format_for_language(self, language: str) -> str:
        """Get appropriate documentation format for language.
        
        Args:
            language: Programming language name
            
        Returns:
            Documentation format name
        """
        format_map = {
            'python': 'Google-style docstring',
            'javascript': 'JSDoc',
            'typescript': 'TSDoc',
            'java': 'Javadoc',
            'csharp': 'XML documentation comment',
            'go': 'Go documentation comment',
            'php': 'PHPDoc',
            'ruby': 'YARD',
            'cpp': 'Doxygen',
            'rust': 'Rustdoc',
            'swift': 'Swift DocC',
            'kotlin': 'KDoc'
        }
        
        return format_map.get(language.lower(), 'standard comment')
    
    def _summarize_components(self, repo_analysis: Dict[str, Any]) -> str:
        """Summarize key components in the repository.
        
        Args:
            repo_analysis: Repository analysis data
            
        Returns:
            Component summary string
        """
        components = []
        
        for file_info in repo_analysis.get('files', [])[:10]:  # Top 10 files
            file_path = file_info.get('file_path', 'unknown')
            language = file_info.get('language', 'unknown')
            func_count = len(file_info.get('functions', []))
            class_count = len(file_info.get('classes', []))
            
            if func_count > 0 or class_count > 0:
                components.append(
                    f"- {file_path} ({language}): {class_count} classes, {func_count} functions"
                )
        
        return '\n'.join(components) if components else 'No major components detected'
    
    def _infer_architecture_type(self, repo_analysis: Dict[str, Any]) -> str:
        """Infer the architecture type of the project.
        
        Args:
            repo_analysis: Repository analysis data
            
        Returns:
            Architecture type description
        """
        language_count = len(repo_analysis.get('language_stats', {}))
        
        if language_count >= 3:
            return "Multi-language microservices architecture"
        elif language_count == 2:
            return "Full-stack application"
        else:
            return "Single-language application"
    
    def _generate_tech_stack_summary(self, repo_analysis: Dict[str, Any]) -> str:
        """Generate technology stack summary.
        
        Args:
            repo_analysis: Repository analysis data
            
        Returns:
            Tech stack summary
        """
        language_stats = repo_analysis.get('language_stats', {})
        
        lines = []
        for language, count in sorted(language_stats.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- {language.capitalize()}: {count} files")
        
        return '\n'.join(lines) if lines else 'Unknown technology stack'
    
    def _generate_structure_summary(self, repo_analysis: Dict[str, Any]) -> str:
        """Generate project structure summary.
        
        Args:
            repo_analysis: Repository analysis data
            
        Returns:
            Structure summary
        """
        repo_path = Path(repo_analysis.get('repository_path', ''))
        
        # Simple structure visualization
        structure = [
            f"{repo_path.name}/",
            "├── src/",
            "├── tests/",
            "├── docs/",
            "└── README.md"
        ]
        
        return '\n'.join(structure)
    
    def _generate_module_summary(self, file_analysis: Dict[str, Any]) -> str:
        """Generate module summary.
        
        Args:
            file_analysis: File analysis data
            
        Returns:
            Module summary
        """
        summaries = []
        
        # Summarize classes
        classes = file_analysis.get('classes', [])
        if classes:
            class_names = [c.get('name', 'unknown') for c in classes[:3]]
            summaries.append(f"Contains {len(classes)} class(es): {', '.join(class_names)}")
        
        # Summarize functions
        functions = file_analysis.get('functions', [])
        if functions:
            func_names = [f.get('name', 'unknown') for f in functions[:5]]
            summaries.append(f"Implements {len(functions)} function(s): {', '.join(func_names)}")
        
        return '. '.join(summaries) if summaries else 'Module contains code elements'
