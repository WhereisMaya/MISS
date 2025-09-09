#!/usr/bin/env python3
"""
Mindseye Evidence Compiler - Startup Script
Quick start script for the Mindseye evidence compilation system.

Author: AI Assistant
Purpose: Easy startup for Maya Patterson's evidence management needs
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def main():
    """Main startup function."""
    print("🧠 Mindseye Evidence Compiler - Startup")
    print("=" * 50)
    
    # Check if evidence directory exists
    evidence_dir = Path("evidence")
    if not evidence_dir.exists():
        print("📁 Creating evidence directory structure...")
        subprocess.run([sys.executable, "mindseye_cli.py", "init", "--evidence-root", "evidence"])
    
    # Compile evidence if needed
    print("🔍 Checking for evidence files...")
    evidence_files = list(evidence_dir.rglob("*.txt")) + list(evidence_dir.rglob("*.md"))
    
    if evidence_files:
        print(f"📄 Found {len(evidence_files)} evidence files")
        print("🔧 Compiling evidence...")
        result = subprocess.run([
            sys.executable, "mindseye_cli.py", "compile", 
            "--evidence-root", "evidence", "--output-dir", "."
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Evidence compiled successfully!")
        else:
            print("❌ Compilation failed:")
            print(result.stderr)
    else:
        print("📝 No evidence files found. Add .txt or .md files to the evidence/ directory.")
    
    # Show statistics
    print("\n📊 Current Statistics:")
    subprocess.run([sys.executable, "mindseye_cli.py", "stats", "--evidence-root", "evidence"])
    
    # Start web server
    print("\n🌐 Starting web interface...")
    print("📱 The web interface will open in your browser")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open("http://localhost:8080")
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the web server
        subprocess.run([sys.executable, "mindseye_cli.py", "serve", "--port", "8080"])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
