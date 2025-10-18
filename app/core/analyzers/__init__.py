"""
Language-specific analyzers for different programming languages.
Each analyzer extracts functions, classes, and other code elements.
"""

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_analyzer(language: str):
    """Get analyzer for a specific language.
    
    Args:
        language: Programming language name
        
    Returns:
        Analyzer module or None
    """
    analyzers = {
        'python': PythonAnalyzer(),
        'javascript': JavaScriptAnalyzer(),
        'typescript': TypeScriptAnalyzer(),
        'java': JavaAnalyzer(),
        'csharp': CSharpAnalyzer(),
        'go': GoAnalyzer(),
        'php': PHPAnalyzer(),
        'ruby': RubyAnalyzer(),
        'cpp': CppAnalyzer(),
        'rust': RustAnalyzer(),
    }
    
    return analyzers.get(language.lower())


class BaseAnalyzer:
    """Base class for language-specific analyzers."""
    
    def analyze(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """Analyze code file.
        
        Args:
            file_content: Content of the file
            file_path: Path to the file
            
        Returns:
            Analysis result
        """
        raise NotImplementedError


class PythonAnalyzer(BaseAnalyzer):
    """Python code analyzer."""
    
    def analyze(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """Analyze Python code.
        
        Args:
            file_content: Python source code
            file_path: Path to the file
            
        Returns:
            Analysis result with functions, classes, etc.
        """
        import ast
        
        try:
            tree = ast.parse(file_content)
            
            functions = []
            classes = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(self._extract_function(node, file_content))
                elif isinstance(node, ast.ClassDef):
                    classes.append(self._extract_class(node, file_content))
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports.append(self._extract_import(node))
            
            return {
                'functions': functions,
                'classes': classes,
                'imports': imports,
                'line_count': len(file_content.split('\n'))
            }
        
        except SyntaxError as e:
            logger.error(f"Syntax error in {file_path}: {e}")
            return {'error': str(e), 'functions': [], 'classes': [], 'imports': []}
    
    def _extract_function(self, node: Any, source: str) -> Dict[str, Any]:
        """Extract function information from AST node.
        
        Args:
            node: AST FunctionDef node
            source: Source code
            
        Returns:
            Function information
        """
        import ast
        
        # Extract parameters
        parameters = []
        for arg in node.args.args:
            param_info = {'name': arg.arg}
            if arg.annotation:
                param_info['type'] = ast.unparse(arg.annotation)
            parameters.append(param_info)
        
        # Extract return type
        return_type = None
        if node.returns:
            return_type = ast.unparse(node.returns)
        
        # Extract docstring
        docstring = ast.get_docstring(node)
        
        # Extract decorators
        decorators = [ast.unparse(dec) for dec in node.decorator_list]
        
        return {
            'name': node.name,
            'type': 'async_function' if isinstance(node, ast.AsyncFunctionDef) else 'function',
            'parameters': parameters,
            'return_type': return_type,
            'docstring': docstring,
            'decorators': decorators,
            'line_number': node.lineno,
            'end_line_number': node.end_lineno,
            'is_private': node.name.startswith('_'),
            'is_magic': node.name.startswith('__') and node.name.endswith('__')
        }
    
    def _extract_class(self, node: Any, source: str) -> Dict[str, Any]:
        """Extract class information from AST node.
        
        Args:
            node: AST ClassDef node
            source: Source code
            
        Returns:
            Class information
        """
        import ast
        
        # Extract base classes
        bases = [ast.unparse(base) for base in node.bases]
        
        # Extract methods
        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(self._extract_function(item, source))
        
        # Extract docstring
        docstring = ast.get_docstring(node)
        
        # Extract decorators
        decorators = [ast.unparse(dec) for dec in node.decorator_list]
        
        return {
            'name': node.name,
            'type': 'class',
            'bases': bases,
            'methods': methods,
            'docstring': docstring,
            'decorators': decorators,
            'line_number': node.lineno,
            'end_line_number': node.end_lineno,
            'is_private': node.name.startswith('_')
        }
    
    def _extract_import(self, node: Any) -> Dict[str, Any]:
        """Extract import information from AST node.
        
        Args:
            node: AST Import or ImportFrom node
            
        Returns:
            Import information
        """
        import ast
        
        if isinstance(node, ast.Import):
            return {
                'type': 'import',
                'modules': [alias.name for alias in node.names],
                'line_number': node.lineno
            }
        elif isinstance(node, ast.ImportFrom):
            return {
                'type': 'from_import',
                'module': node.module,
                'names': [alias.name for alias in node.names],
                'level': node.level,
                'line_number': node.lineno
            }
        
        # Fallback for unknown import types
        return {
            'type': 'unknown',
            'line_number': getattr(node, 'lineno', 0)
        }


class JavaScriptAnalyzer(BaseAnalyzer):
    """JavaScript code analyzer."""
    
    def analyze(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """Analyze JavaScript code.
        
        Args:
            file_content: JavaScript source code
            file_path: Path to the file
            
        Returns:
            Analysis result
        """
        # For MVP, we'll use regex-based parsing
        # In production, this would use Tree-sitter
        import re
        
        functions = self._extract_js_functions(file_content)
        classes = self._extract_js_classes(file_content)
        imports = self._extract_js_imports(file_content)
        exports = self._extract_js_exports(file_content)
        
        return {
            'functions': functions,
            'classes': classes,
            'imports': imports,
            'exports': exports,
            'line_count': len(file_content.split('\n'))
        }
    
    def _extract_js_functions(self, source: str) -> list:
        """Extract JavaScript function declarations."""
        import re
        
        functions = []
        
        # Function declarations: function name(...) { }
        pattern = r'(?:async\s+)?function\s+(\w+)\s*\((.*?)\)'
        for match in re.finditer(pattern, source):
            functions.append({
                'name': match.group(1),
                'type': 'function',
                'parameters': [p.strip() for p in match.group(2).split(',') if p.strip()],
                'is_async': 'async' in match.group(0)
            })
        
        # Arrow functions: const name = (...) => { }
        pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\((.*?)\)\s*=>'
        for match in re.finditer(pattern, source):
            functions.append({
                'name': match.group(1),
                'type': 'arrow_function',
                'parameters': [p.strip() for p in match.group(2).split(',') if p.strip()],
                'is_async': 'async' in match.group(0)
            })
        
        return functions
    
    def _extract_js_classes(self, source: str) -> list:
        """Extract JavaScript class declarations."""
        import re
        
        classes = []
        pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{'
        
        for match in re.finditer(pattern, source):
            classes.append({
                'name': match.group(1),
                'type': 'class',
                'extends': match.group(2)
            })
        
        return classes
    
    def _extract_js_imports(self, source: str) -> list:
        """Extract JavaScript import statements."""
        import re
        
        imports = []
        
        # import ... from '...'
        pattern = r'import\s+(?:{([^}]+)}|(\w+))\s+from\s+[\'"]([^\'"]+)[\'"]'
        for match in re.finditer(pattern, source):
            imports.append({
                'type': 'import',
                'names': match.group(1).split(',') if match.group(1) else [match.group(2)],
                'source': match.group(3)
            })
        
        # require('...')
        pattern = r'(?:const|let|var)\s+(?:{([^}]+)}|(\w+))\s*=\s*require\([\'"]([^\'"]+)[\'"]\)'
        for match in re.finditer(pattern, source):
            imports.append({
                'type': 'require',
                'names': match.group(1).split(',') if match.group(1) else [match.group(2)],
                'source': match.group(3)
            })
        
        return imports
    
    def _extract_js_exports(self, source: str) -> list:
        """Extract JavaScript export statements."""
        import re
        
        exports = []
        
        # export ...
        pattern = r'export\s+(?:default\s+)?(?:class|function|const|let|var)\s+(\w+)'
        for match in re.finditer(pattern, source):
            exports.append({
                'name': match.group(1),
                'is_default': 'default' in match.group(0)
            })
        
        return exports


class TypeScriptAnalyzer(JavaScriptAnalyzer):
    """TypeScript code analyzer (extends JavaScript analyzer)."""
    
    def analyze(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """Analyze TypeScript code."""
        result = super().analyze(file_content, file_path)
        
        # Add TypeScript-specific analysis
        interfaces = self._extract_interfaces(file_content)
        types = self._extract_types(file_content)
        
        result['interfaces'] = interfaces
        result['types'] = types
        
        return result
    
    def _extract_interfaces(self, source: str) -> list:
        """Extract TypeScript interface declarations."""
        import re
        
        interfaces = []
        pattern = r'interface\s+(\w+)(?:\s+extends\s+([\w,\s]+))?\s*\{'
        
        for match in re.finditer(pattern, source):
            interfaces.append({
                'name': match.group(1),
                'extends': match.group(2).split(',') if match.group(2) else []
            })
        
        return interfaces
    
    def _extract_types(self, source: str) -> list:
        """Extract TypeScript type declarations."""
        import re
        
        types = []
        pattern = r'type\s+(\w+)\s*='
        
        for match in re.finditer(pattern, source):
            types.append({
                'name': match.group(1)
            })
        
        return types


class JavaAnalyzer(BaseAnalyzer):
    """Java code analyzer."""
    
    def analyze(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """Analyze Java code."""
        import re
        
        classes = self._extract_java_classes(file_content)
        methods = self._extract_java_methods(file_content)
        imports = self._extract_java_imports(file_content)
        
        return {
            'classes': classes,
            'methods': methods,
            'imports': imports,
            'line_count': len(file_content.split('\n'))
        }
    
    def _extract_java_classes(self, source: str) -> list:
        """Extract Java class declarations."""
        import re
        
        classes = []
        pattern = r'(?:public\s+)?(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w,\s]+))?\s*\{'
        
        for match in re.finditer(pattern, source):
            classes.append({
                'name': match.group(1),
                'type': 'class',
                'extends': match.group(2),
                'implements': match.group(3).split(',') if match.group(3) else []
            })
        
        return classes
    
    def _extract_java_methods(self, source: str) -> list:
        """Extract Java method declarations."""
        import re
        
        methods = []
        pattern = r'(?:public|private|protected)\s+(?:static\s+)?(\w+)\s+(\w+)\s*\((.*?)\)'
        
        for match in re.finditer(pattern, source):
            methods.append({
                'return_type': match.group(1),
                'name': match.group(2),
                'parameters': [p.strip() for p in match.group(3).split(',') if p.strip()]
            })
        
        return methods
    
    def _extract_java_imports(self, source: str) -> list:
        """Extract Java import statements."""
        import re
        
        imports = []
        pattern = r'import\s+((?:static\s+)?[\w.]+);'
        
        for match in re.finditer(pattern, source):
            imports.append({
                'package': match.group(1),
                'is_static': 'static' in match.group(1)
            })
        
        return imports


class CSharpAnalyzer(BaseAnalyzer):
    """C# code analyzer."""
    
    def analyze(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """Analyze C# code."""
        # Similar to Java analyzer with C#-specific syntax
        return {
            'classes': [],
            'methods': [],
            'namespaces': [],
            'line_count': len(file_content.split('\n'))
        }


class GoAnalyzer(BaseAnalyzer):
    """Go code analyzer."""
    
    def analyze(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """Analyze Go code."""
        return {
            'functions': [],
            'structs': [],
            'interfaces': [],
            'line_count': len(file_content.split('\n'))
        }


class PHPAnalyzer(BaseAnalyzer):
    """PHP code analyzer."""
    
    def analyze(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """Analyze PHP code."""
        return {
            'functions': [],
            'classes': [],
            'line_count': len(file_content.split('\n'))
        }


class RubyAnalyzer(BaseAnalyzer):
    """Ruby code analyzer."""
    
    def analyze(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """Analyze Ruby code."""
        return {
            'methods': [],
            'classes': [],
            'modules': [],
            'line_count': len(file_content.split('\n'))
        }


class CppAnalyzer(BaseAnalyzer):
    """C++ code analyzer."""
    
    def analyze(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """Analyze C++ code."""
        return {
            'functions': [],
            'classes': [],
            'namespaces': [],
            'line_count': len(file_content.split('\n'))
        }


class RustAnalyzer(BaseAnalyzer):
    """Rust code analyzer."""
    
    def analyze(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """Analyze Rust code."""
        return {
            'functions': [],
            'structs': [],
            'traits': [],
            'line_count': len(file_content.split('\n'))
        }
