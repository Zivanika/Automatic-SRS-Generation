"""
Setup script for SRS Generation API
This script helps you set up the environment
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_env_file():
    """Check if .env file exists"""
    print("\nChecking environment configuration...")
    env_file = Path(".env")
    
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("   Creating .env file from template...")
        
        with open(".env", "w") as f:
            f.write("# OpenAI API Configuration\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n\n")
            f.write("# Server Configuration\n")
            f.write("PORT=5000\n")
        
        print("✅ .env file created")
        print("   ⚠️  Please edit .env and add your OpenAI API key!")
        return False
    else:
        print("✅ .env file exists")
        
        # Check if API key is set
        with open(".env", "r") as f:
            content = f.read()
            if "your_openai_api_key_here" in content or not any("OPENAI_API_KEY=sk-" in line for line in content.split("\n")):
                print("   ⚠️  OpenAI API key not configured properly")
                print("   Please edit .env and add your real API key")
                return False
        
        print("   ✅ OpenAI API key appears to be configured")
        return True

def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking dependencies...")
    required_packages = [
        "fastapi",
        "uvicorn",
        "langchain",
        "langchain_openai",
        "reportlab",
        "python-docx",
        "python-dotenv",
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed")
    return True

def create_directories():
    """Create necessary directories"""
    print("\nCreating required directories...")
    
    dirs = ["pdfs", "docs"]
    for dir_name in dirs:
        path = Path(dir_name)
        if not path.exists():
            path.mkdir()
            print(f"✅ Created {dir_name}/ directory")
        else:
            print(f"✅ {dir_name}/ directory exists")
    
    return True

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("\nNext Steps:")
    print("1. Make sure your OpenAI API key is set in .env")
    print("2. Start the server:")
    print("   python app.py")
    print("\n3. Test the API:")
    print("   python test_api.py")
    print("\n4. View API documentation:")
    print("   http://localhost:5000/docs")
    print("\n5. Check out the migration guide:")
    print("   Read MIGRATION_GUIDE.md for details")
    print("="*60)

def main():
    """Run all setup checks"""
    print("="*60)
    print("SRS Generation API - Setup")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("Dependencies", check_dependencies),
        ("Directories", create_directories),
    ]
    
    all_passed = True
    for name, check_func in checks:
        if not check_func():
            all_passed = False
    
    if all_passed:
        print("\n✅ All checks passed!")
    else:
        print("\n⚠️  Some checks failed. Please review the messages above.")
    
    print_next_steps()

if __name__ == "__main__":
    main()

