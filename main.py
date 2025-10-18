#!/usr/bin/env python3
"""
Main entry point for Universal Code Documentation Writer.
Provides a unified interface to run different components.
"""

import sys
import click  # type: ignore[import]
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


@click.group()
def main():
    """Universal Code Documentation Writer - Main Entry Point."""
    pass


@main.command()  # type: ignore[misc]
@click.option('--host', default='0.0.0.0', help='API host')
@click.option('--port', default=8000, help='API port')
@click.option('--reload', is_flag=True, help='Enable auto-reload')
def api(host, port, reload):
    """Start the FastAPI server."""
    import uvicorn  # type: ignore[import]
    from app.api.main import app
    
    click.echo(f"🚀 Starting API server on {host}:{port}")
    uvicorn.run(
        "app.api.main:app",
        host=host,
        port=port,
        reload=reload
    )


@main.command()  # type: ignore[misc]
@click.option('--port', default=8501, help='Streamlit port')
def web(port):
    """Start the Streamlit web interface."""
    import subprocess
    
    click.echo(f"🌐 Starting web interface on port {port}")
    subprocess.run([
        'streamlit', 'run',
        'app/web/streamlit_app.py',
        '--server.port', str(port)
    ])


@main.command()  # type: ignore[misc]
@click.argument('args', nargs=-1)
def cli(args):
    """Run the CLI interface."""
    from app.cli import cli as cli_app
    
    sys.argv = ['cli'] + list(args)
    cli_app()


@main.command()  # type: ignore[misc]
def setup():
    """Run the setup script."""
    import subprocess
    
    click.echo("🔧 Running setup script...")
    subprocess.run(['python', 'scripts/setup.py'])


@main.command()  # type: ignore[misc]
def test():
    """Run tests."""
    import subprocess
    
    click.echo("🧪 Running tests...")
    subprocess.run(['pytest', '-v'])


@main.command()  # type: ignore[misc]
def info():
    """Display project information."""
    from app import __version__, __description__
    
    click.echo("\n" + "="*60)
    click.echo("Universal Multi-Language GenAI Code Documentation Writer")
    click.echo("="*60)
    click.echo(f"\nVersion: {__version__}")
    click.echo(f"Description: {__description__}\n")
    click.echo("Available commands:")
    click.echo("  api     - Start FastAPI server")
    click.echo("  web     - Start Streamlit web interface")
    click.echo("  cli     - Run CLI commands")
    click.echo("  setup   - Run setup script")
    click.echo("  test    - Run tests")
    click.echo("  info    - Show this information")
    click.echo("\nFor CLI help:")
    click.echo("  python main.py cli --help")
    click.echo("\nQuick start:")
    click.echo("  1. python main.py setup")
    click.echo("  2. Edit .env and add your API key")
    click.echo("  3. python main.py web")
    click.echo("\n" + "="*60 + "\n")


if __name__ == '__main__':
    main()
