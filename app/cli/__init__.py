"""
Command-Line Interface for Code Documentation Tool.
"""

import click  # type: ignore[import]
from pathlib import Path
import sys
import logging
from rich.console import Console  # type: ignore[import]
from rich.progress import Progress, SpinnerColumn, TextColumn  # type: ignore[import]
from rich.table import Table  # type: ignore[import]

from app.core.universal_analyzer import UniversalCodeAnalyzer
from app.core.llm import DocumentationGenerator
from app.core.generators.readme_generator import READMEGenerator
from config import get_config


console = Console()
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Universal Multi-Language Code Documentation Writer.
    
    Generate comprehensive documentation for code in 15+ programming languages.
    """
    pass


@cli.command()  # type: ignore[misc]
@click.argument('path', type=click.Path(exists=True))
@click.option('--recursive', '-r', is_flag=True, help='Analyze directory recursively')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--format', '-f', type=click.Choice(['markdown', 'html', 'json']), default='markdown')
def analyze(path: str, recursive: bool, output: str, format: str):
    """Analyze code files and generate documentation.
    
    PATH: File or directory to analyze
    """
    console.print(f"\n[bold blue]🔍 Analyzing:[/bold blue] {path}\n")
    
    path_obj = Path(path)
    analyzer = UniversalCodeAnalyzer()
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Analyzing code...", total=None)
            
            if path_obj.is_file():
                # Analyze single file
                result = analyzer.parse_file(str(path_obj))
                _display_file_analysis(result)
            else:
                # Analyze directory
                result = analyzer.analyze_repository(str(path_obj))
                _display_repository_analysis(result)
            
            progress.update(task, completed=True)
        
        # Save output if specified
        if output:
            _save_output(result, output, format)
            console.print(f"\n[green]✓[/green] Output saved to: {output}")
        
    except Exception as e:
        console.print(f"\n[red]✗ Error:[/red] {str(e)}")
        sys.exit(1)


@cli.command()  # type: ignore[misc]
@click.argument('path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), default='README.md', help='Output README file')
@click.option('--name', '-n', type=str, help='Project name')
def readme(path: str, output: str, name: str):
    """Generate README file for a project.
    
    PATH: Project directory
    """
    console.print(f"\n[bold blue]📝 Generating README for:[/bold blue] {path}\n")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            # Analyze repository
            task1 = progress.add_task("Analyzing repository...", total=None)
            analyzer = UniversalCodeAnalyzer()
            repo_analysis = analyzer.analyze_repository(path)
            progress.update(task1, completed=True)
            
            # Generate README
            task2 = progress.add_task("Generating README...", total=None)
            readme_gen = READMEGenerator()
            readme_content = readme_gen.generate_readme(repo_analysis, name)
            progress.update(task2, completed=True)
        
        # Save README
        output_path = Path(output)
        output_path.write_text(readme_content, encoding='utf-8')
        
        console.print(f"\n[green]✓[/green] README generated successfully!")
        console.print(f"[green]✓[/green] Saved to: {output}")
        
    except Exception as e:
        console.print(f"\n[red]✗ Error:[/red] {str(e)}")
        sys.exit(1)


@cli.command()  # type: ignore[misc]
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--function', '-fn', type=str, help='Function name to document')
@click.option('--class-name', '-c', type=str, help='Class name to document')
def document(file_path: str, function: str, class_name: str):
    """Generate documentation for specific code elements.
    
    FILE_PATH: Path to code file
    """
    console.print(f"\n[bold blue]📚 Generating documentation for:[/bold blue] {file_path}\n")
    
    try:
        analyzer = UniversalCodeAnalyzer()
        doc_gen = DocumentationGenerator()
        
        # Analyze file
        file_analysis = analyzer.parse_file(file_path)
        language = file_analysis.get('language', 'unknown')
        
        if function:
            # Document specific function
            funcs = [f for f in file_analysis.get('functions', []) if f['name'] == function]
            if funcs:
                func_info = funcs[0]
                doc = doc_gen.generate_function_documentation(func_info, language)
                console.print(f"\n[green]Documentation for function '{function}':[/green]\n")
                console.print(doc)
            else:
                console.print(f"[yellow]Function '{function}' not found[/yellow]")
        
        elif class_name:
            # Document specific class
            classes = [c for c in file_analysis.get('classes', []) if c['name'] == class_name]
            if classes:
                class_info = classes[0]
                doc = doc_gen.generate_class_documentation(class_info, language)
                console.print(f"\n[green]Documentation for class '{class_name}':[/green]\n")
                console.print(doc)
            else:
                console.print(f"[yellow]Class '{class_name}' not found[/yellow]")
        
        else:
            console.print("[yellow]Please specify --function or --class-name[/yellow]")
    
    except Exception as e:
        console.print(f"\n[red]✗ Error:[/red] {str(e)}")
        sys.exit(1)


@cli.command()  # type: ignore[misc]
def languages():
    """List supported programming languages."""
    console.print("\n[bold]Supported Programming Languages[/bold]\n")
    
    config = get_config()
    
    # Create table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Tier", style="cyan")
    table.add_column("Languages", style="green")
    table.add_column("Documentation Format", style="yellow")
    
    # Tier 1
    tier1 = config.get('languages.tier1', [])
    table.add_row("Tier 1 (MVP)", ", ".join(tier1), "Full support")
    
    # Tier 2
    tier2 = config.get('languages.tier2', [])
    table.add_row("Tier 2", ", ".join(tier2), "Extended support")
    
    # Tier 3
    tier3 = config.get('languages.tier3', [])
    table.add_row("Tier 3", ", ".join(tier3), "Basic support")
    
    console.print(table)
    console.print()


def _display_file_analysis(result: dict):
    """Display file analysis results."""
    console.print(f"[cyan]Language:[/cyan] {result.get('language', 'unknown')}")
    console.print(f"[cyan]Functions:[/cyan] {len(result.get('functions', []))}")
    console.print(f"[cyan]Classes:[/cyan] {len(result.get('classes', []))}")
    console.print(f"[cyan]Lines:[/cyan] {result.get('line_count', 0)}")


def _display_repository_analysis(result: dict):
    """Display repository analysis results."""
    console.print(f"[cyan]Total Files:[/cyan] {result.get('total_files', 0)}")
    console.print(f"[cyan]Analyzed Files:[/cyan] {result.get('analyzed_files', 0)}")
    
    # Language statistics
    console.print("\n[bold]Language Distribution:[/bold]\n")
    
    table = Table(show_header=True)
    table.add_column("Language", style="cyan")
    table.add_column("Files", style="green")
    table.add_column("Percentage", style="yellow")
    
    language_stats = result.get('language_stats', {})
    total_files = sum(language_stats.values())
    
    for lang, count in sorted(language_stats.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_files * 100) if total_files > 0 else 0
        table.add_row(lang, str(count), f"{percentage:.1f}%")
    
    console.print(table)


def _save_output(result: dict, output_path: str, format: str):
    """Save analysis output to file."""
    import json
    
    output = Path(output_path)
    
    if format == 'json':
        output.write_text(json.dumps(result, indent=2), encoding='utf-8')
    elif format == 'markdown':
        # Convert to markdown
        md_content = _convert_to_markdown(result)
        output.write_text(md_content, encoding='utf-8')
    elif format == 'html':
        # Convert to HTML
        html_content = _convert_to_html(result)
        output.write_text(html_content, encoding='utf-8')


def _convert_to_markdown(result: dict) -> str:
    """Convert analysis result to markdown."""
    lines = ["# Code Analysis Report\n"]
    
    if 'language' in result:
        # Single file
        lines.append(f"## Language: {result['language']}\n")
        lines.append(f"- Functions: {len(result.get('functions', []))}")
        lines.append(f"- Classes: {len(result.get('classes', []))}")
    else:
        # Repository
        lines.append(f"## Repository Analysis\n")
        lines.append(f"- Total Files: {result.get('total_files', 0)}")
        lines.append(f"- Analyzed Files: {result.get('analyzed_files', 0)}\n")
        
        lines.append("### Language Distribution\n")
        for lang, count in result.get('language_stats', {}).items():
            lines.append(f"- {lang}: {count} files")
    
    return '\n'.join(lines)


def _convert_to_html(result: dict) -> str:
    """Convert analysis result to HTML."""
    html = "<html><head><title>Code Analysis</title></head><body>"
    html += "<h1>Code Analysis Report</h1>"
    html += "<pre>" + str(result) + "</pre>"
    html += "</body></html>"
    return html


if __name__ == '__main__':
    cli()
