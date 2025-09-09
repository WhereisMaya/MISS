#!/usr/bin/env python3
"""
Mindseye Evidence Compiler Web Server
Simple web server to serve the GUI and handle API requests.

Author: AI Assistant
Purpose: Web interface for Mindseye evidence compilation system
"""

import os
import json
import csv
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import logging

# Import our evidence compiler
from evidence_compiler import MindseyeEvidenceCompiler

class MindseyeWebHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Mindseye web interface."""
    
    def __init__(self, *args, **kwargs):
        self.compiler = None
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            if path == '/' or path == '/index.html':
                self.serve_index()
            elif path == '/api/stats':
                self.serve_stats()
            elif path == '/api/bubbles':
                self.serve_bubbles()
            elif path == '/api/log':
                self.serve_log()
            elif path == '/api/files':
                self.serve_files()
            else:
                self.send_error(404, "Not Found")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            if path == '/api/compile':
                self.handle_compile()
            elif path == '/api/clear-log':
                self.handle_clear_log()
            else:
                self.send_error(404, "Not Found")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def serve_index(self):
        """Serve the main HTML page."""
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "index.html not found")
    
    def serve_stats(self):
        """Serve compilation statistics."""
        try:
            # Initialize compiler with default paths
            compiler = MindseyeEvidenceCompiler()
            stats = compiler.get_compilation_stats()
            
            # Add additional stats
            stats['evidence_root'] = str(compiler.evidence_root)
            stats['last_compilation'] = self.get_last_compilation_time()
            
            self.send_json_response(stats)
        except Exception as e:
            self.send_error(500, f"Error getting stats: {str(e)}")
    
    def serve_bubbles(self):
        """Serve bubbles JSON data."""
        try:
            bubbles_file = Path("bubbles.json")
            if bubbles_file.exists():
                with open(bubbles_file, 'r', encoding='utf-8') as f:
                    bubbles = json.load(f)
                self.send_json_response(bubbles)
            else:
                self.send_json_response([])
        except Exception as e:
            self.send_error(500, f"Error loading bubbles: {str(e)}")
    
    def serve_log(self):
        """Serve compilation log as CSV."""
        try:
            log_file = Path("compiler_log.csv")
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/csv; charset=utf-8')
                self.send_header('Content-Disposition', 'attachment; filename="compiler_log.csv"')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                self.send_error(404, "No log file found")
        except Exception as e:
            self.send_error(500, f"Error loading log: {str(e)}")
    
    def serve_files(self):
        """Serve list of evidence files."""
        try:
            evidence_root = Path("/evidence")
            files = []
            
            if evidence_root.exists():
                for file_path in evidence_root.rglob("*"):
                    if file_path.is_file() and file_path.suffix.lower() in ['.txt', '.md']:
                        files.append({
                            'name': file_path.name,
                            'path': str(file_path.relative_to(evidence_root)),
                            'size': file_path.stat().st_size,
                            'extension': file_path.suffix[1:],
                            'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                        })
            
            self.send_json_response(files)
        except Exception as e:
            self.send_error(500, f"Error scanning files: {str(e)}")
    
    def handle_compile(self):
        """Handle evidence compilation request."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            evidence_root = data.get('evidence_root', '/evidence')
            output_dir = data.get('output_dir', '.')
            
            # Initialize compiler
            compiler = MindseyeEvidenceCompiler(evidence_root, output_dir)
            
            # Run compilation
            success = compiler.compile_evidence()
            
            if success:
                stats = compiler.get_compilation_stats()
                response = {
                    'success': True,
                    'message': 'Compilation completed successfully',
                    'new_files': stats.get('total_bubbles', 0),
                    'total_processed': stats.get('total_processed_files', 0)
                }
            else:
                response = {
                    'success': False,
                    'error': 'Compilation failed. Check logs for details.'
                }
            
            self.send_json_response(response)
        except Exception as e:
            self.send_error(500, f"Error during compilation: {str(e)}")
    
    def handle_clear_log(self):
        """Handle log clearing request."""
        try:
            log_file = Path("compiler_log.csv")
            if log_file.exists():
                log_file.unlink()
            
            response = {
                'success': True,
                'message': 'Log cleared successfully'
            }
            self.send_json_response(response)
        except Exception as e:
            response = {
                'success': False,
                'error': f'Error clearing log: {str(e)}'
            }
            self.send_json_response(response)
    
    def send_json_response(self, data):
        """Send JSON response."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        self.wfile.write(json_data.encode('utf-8'))
    
    def get_last_compilation_time(self):
        """Get the timestamp of the last compilation."""
        try:
            log_file = Path("compiler_log.csv")
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                    if rows:
                        return rows[-1].get('timestamp', 'Unknown')
            return 'Never'
        except:
            return 'Unknown'
    
    def log_message(self, format, *args):
        """Override to reduce log noise."""
        pass


def run_server(host='localhost', port=8080):
    """Run the web server."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, MindseyeWebHandler)
    
    print(f"🧠 Mindseye Evidence Compiler Web Server")
    print(f"🌐 Server running at http://{host}:{port}")
    print(f"📁 Evidence root: /evidence")
    print(f"📄 Open your browser and navigate to the URL above")
    print(f"⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.shutdown()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Mindseye Evidence Compiler Web Server")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind to")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    run_server(args.host, args.port)


if __name__ == "__main__":
    main()
