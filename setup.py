#!/usr/bin/env python3
"""
Setup script for Depression Detection System
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        'data/raw',
        'data/processed', 
        'data/models',
        'logs',
        'app/templates',
        'app/static/css',
        'app/static/js',
        'app/static/images'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def install_dependencies():
    """Install Python dependencies"""
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Install spaCy model
    if not run_command("python -m spacy download en_core_web_sm", "Installing spaCy English model"):
        return False
    
    return True

def setup_environment():
    """Set up environment file"""
    env_file = Path('.env')
    env_example = Path('env_example.txt')
    
    if not env_file.exists() and env_example.exists():
        # Copy example to .env
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✓ Created .env file from template")
        print("⚠️  Please update .env file with your actual API keys and configuration")
    else:
        print("✓ Environment file already exists")

def main():
    """Main setup function"""
    print("🚀 Setting up Depression Detection System...")
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not install_dependencies():
        print("❌ Dependency installation failed. Please check the error messages above.")
        return False
    
    # Setup environment
    print("\n🔧 Setting up environment...")
    setup_environment()
    
    print("\n✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your API keys")
    print("2. Place your dataset file (augmented_dataset_75000.csv) in the project root")
    print("3. Run: python train_models.py --dataset augmented_dataset_75000.csv")
    print("4. Run: python run.py to start the web application")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
