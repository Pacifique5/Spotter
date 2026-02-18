#!/usr/bin/env python
"""
Quick setup script for Fuel Route Optimizer API.
"""

import os
import sys
import subprocess


def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n→ {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stderr:
            print(e.stderr)
        return False


def check_env_file():
    """Check if .env file exists."""
    if not os.path.exists('.env'):
        print("\n⚠ Warning: .env file not found!")
        print("Please create a .env file with your OpenRouteService API key:")
        print("\nOPENROUTE_API_KEY=your_api_key_here")
        print("\nGet a free key at: https://openrouteservice.org/dev/#/signup")
        return False
    return True


def main():
    """Run setup process."""
    print("="*60)
    print("Fuel Route Optimizer API - Setup")
    print("="*60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        return 1
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing dependencies"
    ):
        return 1
    
    # Check for .env file
    env_exists = check_env_file()
    
    # Run migrations
    if not run_command(
        f"{sys.executable} manage.py migrate",
        "Running database migrations"
    ):
        return 1
    
    # Success message
    print("\n" + "="*60)
    print("✓ Setup completed successfully!")
    print("="*60)
    
    if not env_exists:
        print("\n⚠ Don't forget to create your .env file before starting the server!")
    
    print("\nTo start the server, run:")
    print(f"  {sys.executable} manage.py runserver")
    
    print("\nTo test the API, run:")
    print(f"  {sys.executable} demo_script.py")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
