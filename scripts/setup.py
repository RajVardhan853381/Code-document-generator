#!/usr/bin/env python3
"""
Setup script for Universal Code Documentation Writer.
This script helps set up the development environment.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def run_command(command, description):
    """Run a shell command and print its output."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} - Done")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return False


def create_directories():
    """Create necessary directories."""
    print_header("Creating Directory Structure")
    
    directories = [
        'logs',
        'uploads',
        'outputs',
        'temp',
        'parsers',
        'tests/language_specific',
        'tests/integration',
        'tests/performance',
        'sample_repos/python_samples',
        'sample_repos/javascript_samples',
        'sample_repos/java_samples',
        'docs/language_support',
        'docs/api_reference',
        'docs/user_guides',
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {directory}")
        else:
            print(f"⏭️  Already exists: {directory}")


def setup_environment():
    """Set up Python environment."""
    print_header("Setting Up Python Environment")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Create virtual environment if it doesn't exist
    if not Path('venv').exists():
        print("\n🔧 Creating virtual environment...")
        if run_command('python -m venv venv', 'Create virtual environment'):
            print("✅ Virtual environment created")
        else:
            print("❌ Failed to create virtual environment")
            return False
    else:
        print("⏭️  Virtual environment already exists")
    
    return True


def install_dependencies():
    """Install Python dependencies."""
    print_header("Installing Dependencies")
    
    # Determine pip command based on OS
    if os.name == 'nt':  # Windows
        pip_cmd = 'venv\\Scripts\\pip'
    else:  # Unix-like
        pip_cmd = 'venv/bin/pip'
    
    # Upgrade pip
    run_command(f'{pip_cmd} install --upgrade pip', 'Upgrade pip')
    
    # Install requirements
    if Path('requirements.txt').exists():
        run_command(f'{pip_cmd} install -r requirements.txt', 'Install requirements')
    else:
        print("⚠️  requirements.txt not found")
        return False
    
    return True


def setup_env_file():
    """Set up .env file if it doesn't exist."""
    print_header("Setting Up Environment Variables")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from .env.example...")
        env_file.write_text(env_example.read_text())
        print("✅ .env file created")
        print("\n⚠️  IMPORTANT: Please edit .env and add your API keys:")
        print("   - GEMINI_API_KEY")
        print("   - OPENAI_API_KEY (optional)")
    elif env_file.exists():
        print("⏭️  .env file already exists")
    else:
        print("⚠️  .env.example not found")


def create_sample_files():
    """Create sample Python files for testing."""
    print_header("Creating Sample Files")
    
    # Sample Python file
    sample_py = Path('sample_repos/python_samples/calculator.py')
    if not sample_py.exists():
        sample_py.write_text("""
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class Calculator:
    def __init__(self):
        self.result = 0
    
    def calculate(self, operation, a, b):
        if operation == 'add':
            return add(a, b)
        elif operation == 'subtract':
            return subtract(a, b)
        elif operation == 'multiply':
            return multiply(a, b)
        elif operation == 'divide':
            return divide(a, b)
        else:
            raise ValueError("Unknown operation")
""")
        print("✅ Created sample Python file")
    
    # Sample JavaScript file
    sample_js = Path('sample_repos/javascript_samples/utils.js')
    if not sample_js.exists():
        sample_js.write_text("""
function formatDate(date) {
    return date.toISOString().split('T')[0];
}

function capitalizeString(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

class DataProcessor {
    constructor(data) {
        this.data = data;
    }
    
    process() {
        return this.data.map(item => item.toUpperCase());
    }
}

module.exports = { formatDate, capitalizeString, DataProcessor };
""")
        print("✅ Created sample JavaScript file")


def print_next_steps():
    """Print next steps for the user."""
    print_header("Setup Complete! 🎉")
    
    print("Next steps:\n")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix-like
        print("   source venv/bin/activate")
    
    print("\n2. Configure your API keys in .env file:")
    print("   - Edit .env and add your GEMINI_API_KEY")
    
    print("\n3. Try the CLI:")
    print("   python -m app.cli languages")
    print("   python -m app.cli analyze sample_repos/python_samples/calculator.py")
    
    print("\n4. Start the web interface:")
    print("   streamlit run app/web/streamlit_app.py")
    
    print("\n5. Read the documentation:")
    print("   See README.md for more information")
    
    print("\n" + "="*60 + "\n")


def main():
    """Main setup function."""
    print_header("Universal Code Documentation Writer - Setup")
    
    print("This script will set up your development environment.\n")
    
    # Run setup steps
    steps = [
        ("Creating directories", create_directories),
        ("Setting up Python environment", setup_environment),
        ("Installing dependencies", install_dependencies),
        ("Setting up environment variables", setup_env_file),
        ("Creating sample files", create_sample_files),
    ]
    
    for step_name, step_func in steps:
        result = step_func()
        if result is False:
            print(f"\n❌ Setup failed at step: {step_name}")
            sys.exit(1)
    
    # Print next steps
    print_next_steps()


if __name__ == '__main__':
    main()
