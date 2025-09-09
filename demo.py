#!/usr/bin/env python3
"""
Mindseye Evidence Compiler - Demo Script
Demonstrates the system capabilities with example data.
"""

import subprocess
import time
import webbrowser
import os
from pathlib import Path

def main():
    """Run the Mindseye demo."""
    print("🧠 Mindseye Evidence Compiler - Interactive Demo")
    print("=" * 60)
    
    # Check if example evidence exists
    example_dir = Path("example_evidence")
    if not example_dir.exists():
        print("❌ Example evidence directory not found!")
        print("💡 Run 'python mindseye_cli.py init' first")
        return
    
    # Compile example evidence
    print("🔍 Compiling example evidence...")
    result = subprocess.run([
        "python", "mindseye_cli.py", "compile", 
        "--evidence-root", "example_evidence", "--output-dir", "."
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Evidence compiled successfully!")
    else:
        print("❌ Compilation failed:")
        print(result.stderr)
        return
    
    # Show statistics
    print("\n📊 Current Statistics:")
    subprocess.run(["python", "mindseye_cli.py", "stats", "--evidence-root", "example_evidence"])
    
    # Show example files
    print("\n📁 Example Evidence Files:")
    evidence_files = []
    for file_path in example_dir.rglob("*.txt"):
        evidence_files.append(file_path)
    for file_path in example_dir.rglob("*.md"):
        evidence_files.append(file_path)
    
    for i, file_path in enumerate(evidence_files, 1):
        print(f"  {i}. {file_path.relative_to(example_dir)}")
    
    # Show bubble data
    print("\n🎈 Generated Bubbles:")
    try:
        import json
        with open("bubbles.json", "r") as f:
            bubbles = json.load(f)
        
        for i, bubble in enumerate(bubbles, 1):
            print(f"  {i}. {bubble['title']} - {bubble['color']}")
            print(f"     Position: ({bubble['x']:.1f}, {bubble['y']:.1f})")
            print(f"     URLs: {len(bubble.get('urls', []))} links")
            print()
    except Exception as e:
        print(f"❌ Error loading bubbles: {e}")
    
    # Start web server
    print("🌐 Starting web interface...")
    print("📱 The web interface will open in your browser")
    print("⏹️  Press Ctrl+C to stop the demo")
    print("-" * 60)
    
    try:
        # Open browser after a short delay
        def open_browser():
            time.sleep(3)
            webbrowser.open("http://localhost:8080")
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the web server
        subprocess.run(["python", "mindseye_cli.py", "serve", "--port", "8080"])
        
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error starting demo: {e}")

if __name__ == "__main__":
    main()
