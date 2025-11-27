"""
Lowaah Setup Script
Automates the initial setup process
"""

import os
import sys
import subprocess


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"⚙️  {description}")
    print(f"{'='*60}")
    
    try:
        if sys.platform == 'win32':
            result = subprocess.run(command, shell=True, check=True)
        else:
            result = subprocess.run(command, shell=True, check=True, executable='/bin/bash')
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                  لواح - LOWAAH                            ║
    ║         Saudi Sign Language Assistant Setup               ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Run migrations
    if not run_command(
        f"{sys.executable} manage.py migrate",
        "Running database migrations"
    ):
        print("❌ Failed to run migrations")
        sys.exit(1)
    
    # Collect static files
    if not run_command(
        f"{sys.executable} manage.py collectstatic --noinput",
        "Collecting static files"
    ):
        print("⚠️  Warning: Failed to collect static files (non-critical)")
    
    # Train AI model
    print(f"\n{'='*60}")
    print("🤖 Training AI gesture recognition model")
    print(f"{'='*60}")
    
    if not run_command(
        f"{sys.executable} lowaah_app/ai/train_model.py",
        "Training gesture classifier"
    ):
        print("❌ Failed to train model")
        sys.exit(1)
    
    # Success message
    print(f"\n{'='*60}")
    print("✅ Setup completed successfully!")
    print(f"{'='*60}")
    print("\n🚀 To start the development server, run:")
    print(f"   {sys.executable} manage.py runserver")
    print("\n📱 Then visit: http://127.0.0.1:8000/")
    print("\n💡 Tips:")
    print("   • Click the camera icon to enable gesture detection")
    print("   • Use Alt+C to toggle camera panel")
    print("   • See README.md for full documentation")
    print("\n")


if __name__ == '__main__':
    main()

