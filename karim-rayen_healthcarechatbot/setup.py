#!/usr/bin/env python3
"""
Healthcare Chatbot Setup Script
Quick setup and installation script for the healthcare chatbot application
"""

import sys
import subprocess
import os
import platform
from pathlib import Path

def print_header():
    """Print welcome header"""
    print("🏥" + "="*60 + "🏥")
    print("    Healthcare Chatbot - Quick Setup Script")
    print("🏥" + "="*60 + "🏥")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported!")
        print("   Please install Python 3.8 or higher")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible!")
    return True

def check_pip():
    """Check if pip is available"""
    print("\n🔍 Checking pip installation...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip is available!")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip is not available!")
        print("   Please install pip first")
        return False

def create_virtual_environment():
    """Create virtual environment"""
    venv_path = Path("chatbot_env")
    
    if venv_path.exists():
        print(f"\n📁 Virtual environment already exists at {venv_path}")
        return True
    
    print(f"\n🏗️ Creating virtual environment at {venv_path}...")
    
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print("✅ Virtual environment created successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_activation_command():
    """Get the command to activate virtual environment"""
    system = platform.system()
    
    if system == "Windows":
        return "chatbot_env\\Scripts\\activate"
    else:
        return "source chatbot_env/bin/activate"

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    
    # Determine which requirements file to use
    minimal_req = Path("requirements-minimal.txt")
    full_req = Path("requirements.txt")
    
    if minimal_req.exists():
        req_file = "requirements-minimal.txt"
        print("   Using minimal requirements for faster setup...")
    elif full_req.exists():
        req_file = "requirements.txt"
        print("   Using full requirements...")
    else:
        print("❌ No requirements file found!")
        return False
    
    try:
        # Get the python executable in the virtual environment
        system = platform.system()
        if system == "Windows":
            python_exe = Path("chatbot_env/Scripts/python.exe")
        else:
            python_exe = Path("chatbot_env/bin/python")
        
        if python_exe.exists():
            subprocess.run([str(python_exe), "-m", "pip", "install", "-r", req_file], 
                          check=True)
        else:
            # Fallback to system python
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file], 
                          check=True)
        
        print("✅ Packages installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        print("   Try installing manually with: pip install -r requirements-minimal.txt")
        return False

def check_main_file():
    """Check if main application file exists"""
    app_file = Path("app.py")
    if app_file.exists():
        print(f"\n✅ Main application file found: {app_file}")
        return True
    else:
        print(f"\n❌ Main application file not found: {app_file}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    activation_cmd = get_activation_command()
    
    print("\n🎉" + "="*50 + "🎉")
    print("     Setup Complete!")
    print("🎉" + "="*50 + "🎉")
    print()
    print("📋 Next Steps:")
    print(f"   1. Activate virtual environment: {activation_cmd}")
    print("   2. Start the application: streamlit run app.py")
    print("   3. Open your browser and go to: http://localhost:8501")
    print()
    print("💡 Tips:")
    print("   • Upload medical documents for analysis")
    print("   • Try voice input with audio files")
    print("   • Ask health-related questions")
    print("   • Check the README.md for more information")
    print()
    print("⚠️  Important: This tool is for informational purposes only!")
    print("   Always consult healthcare professionals for medical advice.")
    print()

def run_application():
    """Ask if user wants to run the application immediately"""
    print("🚀 Would you like to start the application now? (y/n): ", end="")
    choice = input().lower().strip()
    
    if choice in ['y', 'yes']:
        print("\n🚀 Starting Healthcare Chatbot...")
        print("   Opening in your default browser...")
        print("   Press Ctrl+C to stop the application when done.")
        print()
        
        try:
            # Get the python executable in the virtual environment
            system = platform.system()
            if system == "Windows":
                python_exe = Path("chatbot_env/Scripts/python.exe")
            else:
                python_exe = Path("chatbot_env/bin/python")
            
            if python_exe.exists():
                subprocess.run([str(python_exe), "-m", "streamlit", "run", "app.py"])
            else:
                # Fallback to system python
                subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
                
        except KeyboardInterrupt:
            print("\n\n👋 Application stopped. Thanks for using Healthcare Chatbot!")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Failed to start application: {e}")
            print("   Try running manually: streamlit run app.py")

def main():
    """Main setup function"""
    print_header()
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Check pip
    if not check_pip():
        sys.exit(1)
    
    # Step 3: Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Step 4: Install requirements
    if not install_requirements():
        print("\n⚠️  Setup completed with warnings. You may need to install packages manually.")
    
    # Step 5: Check main file
    if not check_main_file():
        print("\n❌ Setup incomplete. Main application file is missing.")
        sys.exit(1)
    
    # Step 6: Show next steps
    print_next_steps()
    
    # Step 7: Option to run immediately
    run_application()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        print("   Please check the README.md for manual setup instructions.")
        sys.exit(1)