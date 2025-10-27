#!/usr/bin/env python3
"""
Chatbot Startup Script

This script provides an easy way to start the chatbot with different configurations.
"""

import os
import sys
import subprocess
import argparse

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_cors
        print("✅ Core dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_ai_dependencies():
    """Check if AI dependencies are available"""
    try:
        import openai
        print("✅ AI dependencies are available")
        return True
    except ImportError:
        print("ℹ️  AI dependencies not installed (optional)")
        return False

def run_basic_chatbot():
    """Run the basic chatbot without AI"""
    print("🚀 Starting basic chatbot...")
    os.system("python app.py")

def run_ai_chatbot():
    """Run the chatbot with AI integration"""
    print("🤖 Starting AI-powered chatbot...")
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set")
        print("   AI features will not be available")
        print("   Set your API key: export OPENAI_API_KEY=your-api-key")
    
    os.environ['USE_AI'] = 'true'
    os.system("python app_with_ai.py")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def install_ai_dependencies():
    """Install AI dependencies"""
    print("🤖 Installing AI dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "openai"])

def main():
    parser = argparse.ArgumentParser(description="Chatbot Startup Script")
    parser.add_argument("--mode", choices=["basic", "ai"], default="basic",
                       help="Choose chatbot mode: basic or ai")
    parser.add_argument("--install", action="store_true",
                       help="Install dependencies before starting")
    parser.add_argument("--install-ai", action="store_true",
                       help="Install AI dependencies")
    parser.add_argument("--check", action="store_true",
                       help="Check dependencies and exit")
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("🤖 AI Chatbot Startup Script")
    print("=" * 50)
    
    if args.install:
        install_dependencies()
        return
    
    if args.install_ai:
        install_ai_dependencies()
        return
    
    if args.check:
        check_dependencies()
        check_ai_dependencies()
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 To install dependencies, run:")
        print("   python run.py --install")
        return
    
    # Run appropriate mode
    if args.mode == "ai":
        check_ai_dependencies()
        run_ai_chatbot()
    else:
        run_basic_chatbot()

if __name__ == "__main__":
    main()
