import os
import subprocess
import sys
import platform
from pathlib import Path

def create_virtualenv(venv_dir):
    """Create a virtual environment."""
    if not venv_dir.exists():
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
        print("Virtual environment created.")
    else:
        print("Virtual environment already exists.")

def install_requirements(venv_dir, requirements_file):
    """Install the required packages in the virtual environment."""
    pip_executable = venv_dir / "Scripts" / "pip" if platform.system() == "Windows" else venv_dir / "bin" / "pip"
    if not pip_executable.exists():
        raise FileNotFoundError("Pip not found in the virtual environment. Something went wrong during virtualenv creation.")
    
    print("Installing requirements...")
    subprocess.check_call([str(pip_executable), "install", "-r", requirements_file])
    print("Requirements installed successfully.")

def run_app(venv_dir, app_file):
    """Run the Flask app."""
    python_executable = venv_dir / "Scripts" / "python" if platform.system() == "Windows" else venv_dir / "bin" / "python"
    if not python_executable.exists():
        raise FileNotFoundError("Python executable not found in the virtual environment. Something went wrong during virtualenv creation.")
    
    print("Running the app...")
    subprocess.check_call([str(python_executable), app_file])

if __name__ == "__main__":
    # Paths
    base_dir = Path(__file__).parent.resolve()
    venv_dir = base_dir / "venv"
    requirements_file = base_dir / "requirements.txt"
    app_file = base_dir / "app.py"

    # Check if requirements.txt exists
    if not requirements_file.exists():
        print("Error: requirements.txt not found.")
        sys.exit(1)

    # Check if app.py exists
    if not app_file.exists():
        print("Error: app.py not found.")
        sys.exit(1)

    try:
        # Create a virtual environment
        create_virtualenv(venv_dir)

        # Install required packages
        install_requirements(venv_dir, str(requirements_file))

        # Run the Flask app
        run_app(venv_dir, str(app_file))
    except subprocess.CalledProcessError as e:
        print(f"Error during setup or execution: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
