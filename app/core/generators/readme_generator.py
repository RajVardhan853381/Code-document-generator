"""
README Generator - Creates comprehensive README files for multi-language projects.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

from app.core.llm import DocumentationGenerator


logger = logging.getLogger(__name__)


class READMEGenerator:
    """Generates comprehensive README files for repositories."""
    
    def __init__(self):
        """Initialize README generator."""
        self.doc_generator = DocumentationGenerator()
    
    def generate_readme(
        self,
        repository_analysis: Dict[str, Any],
        project_name: Optional[str] = None
    ) -> str:
        """Generate README content for a repository.
        
        Args:
            repository_analysis: Repository analysis data
            project_name: Optional project name override
            
        Returns:
            Generated README content in Markdown format
        """
        # Use LLM to generate comprehensive README
        ai_generated = self.doc_generator.generate_readme(repository_analysis)
        
        # Enhance with structured sections
        readme_content = self._build_readme_structure(
            repository_analysis,
            ai_generated,
            project_name
        )
        
        return readme_content
    
    def _build_readme_structure(
        self,
        repo_analysis: Dict[str, Any],
        ai_content: str,
        project_name: Optional[str] = None
    ) -> str:
        """Build structured README content.
        
        Args:
            repo_analysis: Repository analysis
            ai_content: AI-generated content
            project_name: Project name
            
        Returns:
            Structured README markdown
        """
        sections = []
        
        # Title and badges
        sections.append(self._generate_title_section(repo_analysis, project_name))
        
        # Overview (from AI)
        sections.append(self._generate_overview_section(ai_content))
        
        # Features
        sections.append(self._generate_features_section(repo_analysis))
        
        # Technology Stack
        sections.append(self._generate_tech_stack_section(repo_analysis))
        
        # Architecture
        sections.append(self._generate_architecture_section(repo_analysis))
        
        # Getting Started
        sections.append(self._generate_getting_started_section(repo_analysis))
        
        # Project Structure
        sections.append(self._generate_structure_section(repo_analysis))
        
        # Usage
        sections.append(self._generate_usage_section(repo_analysis))
        
        # Contributing
        sections.append(self._generate_contributing_section())
        
        # License
        sections.append(self._generate_license_section())
        
        return '\n\n'.join(sections)
    
    def _generate_title_section(
        self,
        repo_analysis: Dict[str, Any],
        project_name: Optional[str] = None
    ) -> str:
        """Generate title and badges section."""
        repo_path = Path(repo_analysis.get('repository_path', ''))
        name = project_name or repo_path.name or "Project"
        
        language_stats = repo_analysis.get('language_stats', {})
        languages = list(language_stats.keys())[:5]
        
        title = f"# {name}\n\n"
        
        # Badges
        badges = []
        for lang in languages:
            badges.append(f"![{lang}](https://img.shields.io/badge/{lang}-blue)")
        
        if badges:
            title += ' '.join(badges) + '\n\n'
        
        return title
    
    def _generate_overview_section(self, ai_content: str) -> str:
        """Extract overview from AI-generated content."""
        return "## 📋 Overview\n\n" + self._extract_section(ai_content, "overview")
    
    def _generate_features_section(self, repo_analysis: Dict[str, Any]) -> str:
        """Generate features section."""
        content = "## ✨ Features\n\n"
        
        features = []
        
        # Detect features based on file analysis
        file_count = repo_analysis.get('total_files', 0)
        language_count = len(repo_analysis.get('language_stats', {}))
        
        if language_count > 1:
            features.append(f"Multi-language support ({language_count} languages)")
        
        features.append(f"Comprehensive codebase ({file_count} files)")
        
        # Add generic features
        features.extend([
            "Well-structured architecture",
            "Modular design",
            "Easy to extend and maintain"
        ])
        
        for feature in features:
            content += f"- {feature}\n"
        
        return content
    
    def _generate_tech_stack_section(self, repo_analysis: Dict[str, Any]) -> str:
        """Generate technology stack section."""
        content = "## 🛠️ Technology Stack\n\n"
        
        language_stats = repo_analysis.get('language_stats', {})
        
        if not language_stats:
            return content + "Technology stack information not available.\n"
        
        # Sort by file count
        sorted_languages = sorted(
            language_stats.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        content += "### Programming Languages\n\n"
        
        for language, count in sorted_languages:
            percentage = (count / sum(language_stats.values())) * 100
            content += f"- **{language.capitalize()}**: {count} files ({percentage:.1f}%)\n"
        
        return content
    
    def _generate_architecture_section(self, repo_analysis: Dict[str, Any]) -> str:
        """Generate architecture section."""
        content = "## 🏗️ Architecture\n\n"
        
        language_count = len(repo_analysis.get('language_stats', {}))
        
        if language_count >= 3:
            content += "This project follows a **multi-language microservices architecture**, "
            content += "with components written in different programming languages for optimal performance.\n\n"
        elif language_count == 2:
            content += "This is a **full-stack application** utilizing multiple programming languages "
            content += "for frontend and backend components.\n\n"
        else:
            content += "This project is implemented using a modular architecture pattern.\n\n"
        
        # Add architecture diagram placeholder
        content += "### System Components\n\n"
        content += "```\n"
        content += "┌─────────────────────┐\n"
        content += "│   Application       │\n"
        content += "└──────────┬──────────┘\n"
        content += "           │\n"
        content += "    ┌──────┴──────┐\n"
        content += "    │   Core      │\n"
        content += "    └─────────────┘\n"
        content += "```\n"
        
        return content
    
    def _generate_getting_started_section(self, repo_analysis: Dict[str, Any]) -> str:
        """Generate getting started section."""
        content = "## 🚀 Getting Started\n\n"
        
        content += "### Prerequisites\n\n"
        
        languages = list(repo_analysis.get('language_stats', {}).keys())
        
        for lang in languages:
            prereq = self._get_language_prerequisites(lang)
            if prereq:
                content += f"- {prereq}\n"
        
        content += "\n### Installation\n\n"
        content += "1. **Clone the repository**\n\n"
        content += "```bash\n"
        content += "git clone <repository-url>\n"
        content += "cd " + Path(repo_analysis.get('repository_path', 'project')).name + "\n"
        content += "```\n\n"
        
        content += "2. **Install dependencies**\n\n"
        
        for lang in languages:
            install_cmd = self._get_install_command(lang)
            if install_cmd:
                content += f"For {lang.capitalize()}:\n```bash\n{install_cmd}\n```\n\n"
        
        return content
    
    def _generate_structure_section(self, repo_analysis: Dict[str, Any]) -> str:
        """Generate project structure section."""
        content = "## 📁 Project Structure\n\n"
        
        content += "```\n"
        content += self._build_directory_tree(repo_analysis)
        content += "```\n"
        
        return content
    
    def _generate_usage_section(self, repo_analysis: Dict[str, Any]) -> str:
        """Generate usage section."""
        content = "## 💻 Usage\n\n"
        
        content += "### Basic Usage\n\n"
        content += "```bash\n"
        content += "# Run the application\n"
        content += "# Add specific commands based on your project\n"
        content += "```\n"
        
        return content
    
    def _generate_contributing_section(self) -> str:
        """Generate contributing section."""
        content = "## 🤝 Contributing\n\n"
        content += "Contributions are welcome! Please feel free to submit a Pull Request.\n\n"
        content += "1. Fork the repository\n"
        content += "2. Create your feature branch (`git checkout -b feature/AmazingFeature`)\n"
        content += "3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)\n"
        content += "4. Push to the branch (`git push origin feature/AmazingFeature`)\n"
        content += "5. Open a Pull Request\n"
        
        return content
    
    def _generate_license_section(self) -> str:
        """Generate license section."""
        content = "## 📄 License\n\n"
        content += "This project is licensed under the MIT License - see the LICENSE file for details.\n"
        
        return content
    
    def _get_language_prerequisites(self, language: str) -> str:
        """Get prerequisites for a language."""
        prereqs = {
            'python': 'Python 3.8+',
            'javascript': 'Node.js 14+',
            'typescript': 'Node.js 14+ and TypeScript',
            'java': 'Java JDK 11+',
            'csharp': '.NET 6.0+',
            'go': 'Go 1.18+',
            'php': 'PHP 8.0+',
            'ruby': 'Ruby 3.0+',
            'rust': 'Rust 1.60+',
        }
        
        return prereqs.get(language.lower(), '')
    
    def _get_install_command(self, language: str) -> str:
        """Get installation command for a language."""
        commands = {
            'python': 'pip install -r requirements.txt',
            'javascript': 'npm install',
            'typescript': 'npm install',
            'java': 'mvn install',
            'go': 'go mod download',
            'php': 'composer install',
            'ruby': 'bundle install',
            'rust': 'cargo build',
        }
        
        return commands.get(language.lower(), '')
    
    def _build_directory_tree(self, repo_analysis: Dict[str, Any]) -> str:
        """Build directory tree representation."""
        repo_path = Path(repo_analysis.get('repository_path', ''))
        
        tree = f"{repo_path.name}/\n"
        tree += "├── src/\n"
        tree += "├── tests/\n"
        tree += "├── docs/\n"
        tree += "├── README.md\n"
        tree += "└── LICENSE\n"
        
        return tree
    
    def _extract_section(self, ai_content: str, section_name: str) -> str:
        """Extract a specific section from AI-generated content."""
        # Simple extraction - return first paragraph
        paragraphs = ai_content.strip().split('\n\n')
        return paragraphs[0] if paragraphs else "AI-generated overview content will appear here."
