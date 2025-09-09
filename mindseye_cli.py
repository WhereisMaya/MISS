#!/usr/bin/env python3
"""
Mindseye Evidence Compiler CLI
Command-line interface for the Mindseye evidence compilation system.

Author: AI Assistant
Purpose: Easy-to-use CLI for evidence compilation
"""

import argparse
import sys
from pathlib import Path
from evidence_compiler import MindseyeEvidenceCompiler

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Mindseye Evidence Compiler - Healthcare & Safeguarding Evidence Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic compilation
  python mindseye_cli.py compile

  # Compile with custom paths
  python mindseye_cli.py compile --evidence-root /path/to/evidence --output-dir /path/to/output

  # Show statistics
  python mindseye_cli.py stats

  # Start web server
  python mindseye_cli.py serve --port 8080

  # Create sample evidence structure
  python mindseye_cli.py init --evidence-root /evidence
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Compile command
    compile_parser = subparsers.add_parser('compile', help='Compile evidence files')
    compile_parser.add_argument('--evidence-root', default='/evidence', 
                               help='Root directory to scan for evidence files')
    compile_parser.add_argument('--output-dir', default='.', 
                               help='Output directory for compiled files')
    compile_parser.add_argument('--verbose', '-v', action='store_true', 
                               help='Enable verbose output')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show compilation statistics')
    stats_parser.add_argument('--evidence-root', default='/evidence', 
                             help='Evidence root directory')
    stats_parser.add_argument('--output-dir', default='.', 
                             help='Output directory')
    
    # Serve command
    serve_parser = subparsers.add_parser('serve', help='Start web server')
    serve_parser.add_argument('--host', default='localhost', 
                             help='Host to bind to')
    serve_parser.add_argument('--port', type=int, default=8080, 
                             help='Port to bind to')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize evidence directory structure')
    init_parser.add_argument('--evidence-root', default='/evidence', 
                            help='Evidence root directory to create')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'compile':
            compile_evidence(args)
        elif args.command == 'stats':
            show_stats(args)
        elif args.command == 'serve':
            start_server(args)
        elif args.command == 'init':
            init_evidence_structure(args)
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def compile_evidence(args):
    """Compile evidence files."""
    print("🧠 Mindseye Evidence Compiler")
    print("=" * 50)
    
    # Create evidence root if it doesn't exist
    evidence_root = Path(args.evidence_root)
    if not evidence_root.exists():
        print(f"📁 Creating evidence directory: {evidence_root}")
        evidence_root.mkdir(parents=True, exist_ok=True)
    
    # Initialize compiler
    compiler = MindseyeEvidenceCompiler(str(evidence_root), args.output_dir)
    
    print(f"📂 Evidence root: {evidence_root}")
    print(f"📤 Output directory: {args.output_dir}")
    print()
    
    # Run compilation
    print("🔍 Scanning for evidence files...")
    success = compiler.compile_evidence()
    
    if success:
        print("✅ Compilation completed successfully!")
        
        # Show results
        stats = compiler.get_compilation_stats()
        print(f"📊 Total bubbles: {stats.get('total_bubbles', 0)}")
        print(f"📄 Processed files: {stats.get('total_processed_files', 0)}")
        print(f"📋 Log file: {compiler.log_file}")
        print(f"🎯 Bubbles file: {compiler.bubbles_file}")
    else:
        print("❌ Compilation failed. Check logs for details.")
        sys.exit(1)

def show_stats(args):
    """Show compilation statistics."""
    print("📊 Mindseye Compilation Statistics")
    print("=" * 50)
    
    compiler = MindseyeEvidenceCompiler(args.evidence_root, args.output_dir)
    stats = compiler.get_compilation_stats()
    
    print(f"📂 Evidence root: {stats.get('evidence_root_exists', False)}")
    print(f"📤 Output directory: {args.output_dir}")
    print(f"🎯 Bubbles file: {stats.get('bubbles_file_exists', False)}")
    print(f"📋 Log file: {stats.get('log_file_exists', False)}")
    print(f"📄 Total processed files: {stats.get('total_processed_files', 0)}")
    print(f"🎈 Total bubbles: {stats.get('total_bubbles', 0)}")
    
    # Show evidence files if directory exists
    evidence_root = Path(args.evidence_root)
    if evidence_root.exists():
        evidence_files = list(evidence_root.rglob("*.txt")) + list(evidence_root.rglob("*.md"))
        print(f"📁 Evidence files found: {len(evidence_files)}")
        
        if evidence_files:
            print("\n📄 Evidence files:")
            for file_path in evidence_files[:10]:  # Show first 10
                print(f"  - {file_path.relative_to(evidence_root)}")
            if len(evidence_files) > 10:
                print(f"  ... and {len(evidence_files) - 10} more")

def start_server(args):
    """Start the web server."""
    from web_server import run_server
    run_server(args.host, args.port)

def init_evidence_structure(args):
    """Initialize evidence directory structure with sample files."""
    print("🏗️  Initializing Mindseye Evidence Structure")
    print("=" * 50)
    
    evidence_root = Path(args.evidence_root)
    
    # Create directory structure
    evidence_root.mkdir(parents=True, exist_ok=True)
    (evidence_root / "images").mkdir(exist_ok=True)
    (evidence_root / "documents").mkdir(exist_ok=True)
    (evidence_root / "reports").mkdir(exist_ok=True)
    
    print(f"📁 Created evidence structure at: {evidence_root}")
    
    # Create sample evidence files
    sample_files = [
        ("sample_incident.txt", "Sample incident report for testing the Mindseye system."),
        ("patient_notes.md", "# Patient Notes\n\nThis is a sample patient documentation file."),
        ("safety_protocol.txt", "Safety protocol documentation for healthcare workers."),
        ("reports/quarterly_summary.md", "# Quarterly Summary\n\nSummary of activities and incidents."),
    ]
    
    for filename, content in sample_files:
        file_path = evidence_root / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📄 Created: {filename}")
    
    print(f"\n✅ Evidence structure initialized!")
    print(f"📂 Evidence root: {evidence_root}")
    print(f"🌐 Run 'python mindseye_cli.py serve' to start the web interface")
    print(f"🔍 Run 'python mindseye_cli.py compile' to compile evidence")

if __name__ == "__main__":
    main()
