#!/usr/bin/env python3
"""
Setup script for Music Platform Backend
Run this to set up the development environment
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🎵 Music Platform Backend Setup")
    print("=" * 40)
    
    # Check if Python is installed
    try:
        python_version = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✅ Python found: {python_version.stdout.strip()}")
    except:
        print("❌ Python not found. Please install Python 3.8+")
        return
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("💡 Try: python -m pip install -r requirements.txt")
        return
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("\n⚠️  .env file not found!")
        print("📝 Please copy .env.example to .env and fill in your credentials:")
        print("   - Aiven MySQL credentials")
        print("   - Jamendo API client ID")
        print("   - Session secret")
        
        create_env = input("\n🤔 Create .env from .env.example now? (y/n): ")
        if create_env.lower() == 'y':
            run_command("copy .env.example .env", "Creating .env file")
            print("\n📝 Please edit .env file with your actual credentials before running the app")
    else:
        print("✅ .env file found")
    
    print("\n🚀 Setup completed!")
    print("\nNext steps:")
    print("1. Edit .env file with your credentials")
    print("2. Get Jamendo API key from: https://developer.jamendo.com")
    print("3. Run: python app.py")
    print("\n📚 API Documentation will be available at: http://localhost:5000")

if __name__ == "__main__":
    main()
