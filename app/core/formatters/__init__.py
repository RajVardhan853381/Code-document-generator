"""
Documentation formatters for different programming languages.
Converts AI-generated documentation to language-specific formats.
"""

from typing import Dict, Any, List
import re
import logging


logger = logging.getLogger(__name__)


class BaseFormatter:
    """Base class for documentation formatters."""
    
    def format_function_documentation(
        self,
        function_info: Dict[str, Any],
        generated_doc: str
    ) -> str:
        """Format function documentation.
        
        Args:
            function_info: Function information
            generated_doc: AI-generated documentation
            
        Returns:
            Formatted documentation string
        """
        raise NotImplementedError
    
    def format_class_documentation(
        self,
        class_info: Dict[str, Any],
        generated_doc: str
    ) -> str:
        """Format class documentation.
        
        Args:
            class_info: Class information
            generated_doc: AI-generated documentation
            
        Returns:
            Formatted documentation string
        """
        raise NotImplementedError


class JSDocFormatter(BaseFormatter):
    """JSDoc formatter for JavaScript/TypeScript."""
    
    def format_function_documentation(
        self,
        function_info: Dict[str, Any],
        generated_doc: str
    ) -> str:
        """Format function documentation as JSDoc.
        
        Args:
            function_info: Function information
            generated_doc: AI-generated documentation
            
        Returns:
            JSDoc formatted string
        """
        lines = ['/**']
        
        # Extract description from generated doc
        description = self._extract_description(generated_doc)
        if description:
            for line in description.split('\n'):
                lines.append(f' * {line}')
            lines.append(' *')
        
        # Add parameters
        parameters = function_info.get('parameters', [])
        for param in parameters:
            param_name = param.get('name', 'param')
            param_type = param.get('type', 'any')
            param_desc = self._extract_param_description(generated_doc, param_name)
            
            lines.append(f' * @param {{{param_type}}} {param_name} - {param_desc}')
        
        # Add return type
        if function_info.get('return_type'):
            return_type = function_info['return_type']
            return_desc = self._extract_return_description(generated_doc)
            lines.append(f' * @returns {{{return_type}}} {return_desc}')
        
        # Add examples if present
        examples = self._extract_examples(generated_doc)
        if examples:
            lines.append(' * @example')
            for example in examples:
                lines.append(f' * {example}')
        
        lines.append(' */')
        
        return '\n'.join(lines)
    
    def format_class_documentation(
        self,
        class_info: Dict[str, Any],
        generated_doc: str
    ) -> str:
        """Format class documentation as JSDoc."""
        lines = ['/**']
        
        # Class description
        description = self._extract_description(generated_doc)
        if description:
            for line in description.split('\n'):
                lines.append(f' * {line}')
            lines.append(' *')
        
        # Add class tag
        lines.append(f' * @class {class_info.get("name", "Class")}')
        
        # Add extends if applicable
        extends = class_info.get('extends')
        if extends:
            lines.append(f' * @extends {extends}')
        
        lines.append(' */')
        
        return '\n'.join(lines)
    
    def _extract_description(self, doc: str) -> str:
        """Extract description from generated documentation."""
        # Simple extraction - first paragraph
        paragraphs = doc.strip().split('\n\n')
        return paragraphs[0] if paragraphs else "No description provided."
    
    def _extract_param_description(self, doc: str, param_name: str) -> str:
        """Extract parameter description."""
        pattern = rf'{param_name}[:\s]+(.+?)(?:\n|$)'
        match = re.search(pattern, doc, re.IGNORECASE)
        return match.group(1).strip() if match else "Parameter description"
    
    def _extract_return_description(self, doc: str) -> str:
        """Extract return value description."""
        pattern = r'[Rr]eturn[s]?[:\s]+(.+?)(?:\n|$)'
        match = re.search(pattern, doc)
        return match.group(1).strip() if match else "Return value description"
    
    def _extract_examples(self, doc: str) -> List[str]:
        """Extract code examples."""
        # Look for example section
        pattern = r'[Ee]xample[s]?:?\s*\n((?:.*\n)+?)(?:\n\n|$)'
        match = re.search(pattern, doc)
        
        if match:
            example_text = match.group(1)
            return [line.strip() for line in example_text.split('\n') if line.strip()]
        
        return []


class GoogleDocstringFormatter(BaseFormatter):
    """Google-style docstring formatter for Python."""
    
    def format_function_documentation(
        self,
        function_info: Dict[str, Any],
        generated_doc: str
    ) -> str:
        """Format function documentation as Google-style docstring.
        
        Args:
            function_info: Function information
            generated_doc: AI-generated documentation
            
        Returns:
            Google-style docstring
        """
        lines = ['"""']
        
        # Function description
        description = self._extract_description(generated_doc)
        if description:
            lines.append(description)
            lines.append('')
        
        # Args section
        parameters = function_info.get('parameters', [])
        if parameters:
            lines.append('Args:')
            for param in parameters:
                param_name = param.get('name', 'arg')
                param_type = param.get('type', '')
                param_desc = self._extract_param_description(generated_doc, param_name)
                
                if param_type:
                    lines.append(f'    {param_name} ({param_type}): {param_desc}')
                else:
                    lines.append(f'    {param_name}: {param_desc}')
            lines.append('')
        
        # Returns section
        if function_info.get('return_type'):
            return_type = function_info['return_type']
            return_desc = self._extract_return_description(generated_doc)
            
            lines.append('Returns:')
            lines.append(f'    {return_type}: {return_desc}')
            lines.append('')
        
        # Raises section
        raises = self._extract_raises(generated_doc)
        if raises:
            lines.append('Raises:')
            for exception in raises:
                lines.append(f'    {exception}')
            lines.append('')
        
        # Examples section
        examples = self._extract_examples(generated_doc)
        if examples:
            lines.append('Examples:')
            for example in examples:
                lines.append(f'    {example}')
            lines.append('')
        
        # Remove trailing empty line if present
        if lines[-1] == '':
            lines.pop()
        
        lines.append('"""')
        
        return '\n'.join(lines)
    
    def format_class_documentation(
        self,
        class_info: Dict[str, Any],
        generated_doc: str
    ) -> str:
        """Format class documentation as Google-style docstring."""
        lines = ['"""']
        
        # Class description
        description = self._extract_description(generated_doc)
        if description:
            lines.append(description)
            lines.append('')
        
        # Attributes section
        attributes = self._extract_attributes(generated_doc)
        if attributes:
            lines.append('Attributes:')
            for attr in attributes:
                lines.append(f'    {attr}')
            lines.append('')
        
        # Remove trailing empty line
        if lines[-1] == '':
            lines.pop()
        
        lines.append('"""')
        
        return '\n'.join(lines)
    
    def _extract_description(self, doc: str) -> str:
        """Extract description."""
        paragraphs = doc.strip().split('\n\n')
        return paragraphs[0] if paragraphs else "No description provided."
    
    def _extract_param_description(self, doc: str, param_name: str) -> str:
        """Extract parameter description."""
        pattern = rf'{param_name}[:\s]+(.+?)(?:\n|$)'
        match = re.search(pattern, doc, re.IGNORECASE)
        return match.group(1).strip() if match else "Parameter description"
    
    def _extract_return_description(self, doc: str) -> str:
        """Extract return description."""
        pattern = r'[Rr]eturn[s]?[:\s]+(.+?)(?:\n|$)'
        match = re.search(pattern, doc)
        return match.group(1).strip() if match else "Return value description"
    
    def _extract_raises(self, doc: str) -> List[str]:
        """Extract exception information."""
        pattern = r'[Rr]aises?[:\s]+(.+?)(?:\n|$)'
        match = re.search(pattern, doc)
        
        if match:
            return [match.group(1).strip()]
        
        return []
    
    def _extract_examples(self, doc: str) -> List[str]:
        """Extract examples."""
        pattern = r'[Ee]xample[s]?:?\s*\n((?:.*\n)+?)(?:\n\n|$)'
        match = re.search(pattern, doc)
        
        if match:
            example_text = match.group(1)
            return [line.strip() for line in example_text.split('\n') if line.strip()]
        
        return []
    
    def _extract_attributes(self, doc: str) -> List[str]:
        """Extract class attributes."""
        pattern = r'[Aa]ttribute[s]?:?\s*\n((?:.*\n)+?)(?:\n\n|$)'
        match = re.search(pattern, doc)
        
        if match:
            attr_text = match.group(1)
            return [line.strip() for line in attr_text.split('\n') if line.strip()]
        
        return []


class JavadocFormatter(BaseFormatter):
    """Javadoc formatter for Java."""
    
    def format_function_documentation(
        self,
        function_info: Dict[str, Any],
        generated_doc: str
    ) -> str:
        """Format as Javadoc."""
        lines = ['/**']
        
        # Description
        description = self._extract_description(generated_doc)
        for line in description.split('\n'):
            lines.append(f' * {line}')
        lines.append(' *')
        
        # Parameters
        for param in function_info.get('parameters', []):
            param_name = param.get('name', 'param')
            param_desc = f"Parameter {param_name}"
            lines.append(f' * @param {param_name} {param_desc}')
        
        # Return
        if function_info.get('return_type', 'void') != 'void':
            lines.append(f' * @return Return value description')
        
        lines.append(' */')
        
        return '\n'.join(lines)
    
    def format_class_documentation(
        self,
        class_info: Dict[str, Any],
        generated_doc: str
    ) -> str:
        """Format class documentation as Javadoc."""
        lines = ['/**']
        
        description = self._extract_description(generated_doc)
        for line in description.split('\n'):
            lines.append(f' * {line}')
        
        lines.append(' */')
        
        return '\n'.join(lines)
    
    def _extract_description(self, doc: str) -> str:
        """Extract description."""
        paragraphs = doc.strip().split('\n\n')
        return paragraphs[0] if paragraphs else "No description provided."


class XMLDocFormatter(BaseFormatter):
    """XML documentation formatter for C#."""
    
    def format_function_documentation(
        self,
        function_info: Dict[str, Any],
        generated_doc: str
    ) -> str:
        """Format as XML documentation comments."""
        lines = ['/// <summary>']
        
        description = self._extract_description(generated_doc)
        lines.append(f'/// {description}')
        lines.append('/// </summary>')
        
        # Parameters
        for param in function_info.get('parameters', []):
            param_name = param.get('name', 'param')
            lines.append(f'/// <param name="{param_name}">Parameter description</param>')
        
        # Returns
        if function_info.get('return_type'):
            lines.append(f'/// <returns>Return value description</returns>')
        
        return '\n'.join(lines)
    
    def format_class_documentation(
        self,
        class_info: Dict[str, Any],
        generated_doc: str
    ) -> str:
        """Format class documentation as XML."""
        lines = ['/// <summary>']
        description = self._extract_description(generated_doc)
        lines.append(f'/// {description}')
        lines.append('/// </summary>')
        
        return '\n'.join(lines)
    
    def _extract_description(self, doc: str) -> str:
        """Extract description."""
        paragraphs = doc.strip().split('\n\n')
        return paragraphs[0] if paragraphs else "No description provided."


def get_formatter(language: str) -> BaseFormatter:
    """Get formatter for a specific language.
    
    Args:
        language: Programming language name
        
    Returns:
        Appropriate formatter instance
    """
    formatters = {
        'python': GoogleDocstringFormatter(),
        'javascript': JSDocFormatter(),
        'typescript': JSDocFormatter(),
        'java': JavadocFormatter(),
        'csharp': XMLDocFormatter(),
    }
    
    return formatters.get(language.lower(), BaseFormatter())
