#!/usr/bin/env python3
"""
Mindseye Evidence Compiler
A system for compiling evidence files into interactive bubble visualizations.

Author: AI Assistant
Purpose: Healthcare and safeguarding evidence compilation for international accountability
"""

import os
import json
import csv
import hashlib
import re
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

class MindseyeEvidenceCompiler:
    """Main class for compiling evidence files into Mindseye bubble format."""
    
    def __init__(self, evidence_root: str = "/evidence", output_dir: str = "."):
        """
        Initialize the evidence compiler.
        
        Args:
            evidence_root: Root directory to scan for evidence files
            output_dir: Directory to output compiled files
        """
        self.evidence_root = Path(evidence_root)
        self.output_dir = Path(output_dir)
        self.log_file = self.output_dir / "compiler_log.csv"
        self.bubbles_file = self.output_dir / "bubbles.json"
        self.processed_files = set()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.output_dir / "compiler.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Load existing processed files
        self._load_processed_files()
    
    def _load_processed_files(self):
        """Load previously processed files from the log."""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.processed_files.add(row['filename'])
                self.logger.info(f"Loaded {len(self.processed_files)} previously processed files")
            except Exception as e:
                self.logger.warning(f"Could not load processed files log: {e}")
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating hash for {file_path}: {e}")
            return ""
    
    def _extract_urls(self, content: str) -> List[Dict[str, str]]:
        """Extract URLs from file content."""
        url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
        urls = re.findall(url_pattern, content)
        
        extracted_urls = []
        for url in urls:
            # Extract domain for title
            domain_match = re.search(r'https?://([^/]+)', url)
            title = domain_match.group(1) if domain_match else url
            extracted_urls.append({
                "href": url,
                "title": title
            })
        
        return extracted_urls
    
    def _generate_random_position(self) -> tuple:
        """Generate random position and velocity for bubble."""
        x = random.uniform(50, 800)
        y = random.uniform(50, 600)
        vx = random.uniform(-2, 2)
        vy = random.uniform(-2, 2)
        return x, y, vx, vy
    
    def _generate_random_color(self) -> str:
        """Generate random pastel HSL color."""
        hue = random.uniform(0, 360)
        saturation = random.uniform(60, 100)
        lightness = random.uniform(60, 80)
        return f"hsl({hue:.2f}, {saturation:.1f}%, {lightness:.1f}%)"
    
    def _check_for_image(self, filename: str) -> str:
        """Check if corresponding image exists in images/ directory."""
        image_path = self.evidence_root / "images" / f"{filename}.png"
        if image_path.exists():
            return f"images/{filename}.png"
        return ""
    
    def _create_bubble(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Create a bubble object from file data."""
        filename = file_path.stem
        x, y, vx, vy = self._generate_random_position()
        
        # Extract URLs from content
        urls = self._extract_urls(content)
        
        # Check for image
        image = self._check_for_image(filename)
        
        # Get current date and time
        now = datetime.now()
        created_date = now.strftime("%Y-%m-%d")
        created_time = now.strftime("%H:%M:%S")
        
        bubble = {
            "title": filename,
            "description": content[:500] + "..." if len(content) > 500 else content,
            "x": x,
            "y": y,
            "vx": vx,
            "vy": vy,
            "color": self._generate_random_color(),
            "textColor": "yellow",
            "radius": 28,
            "font": "Trebuchet MS",
            "image": image,
            "glow": True,
            "fontSize": 8,
            "rotation": 0,
            "fixed": True,
            "static": True,
            "shape": "circle",
            "heightRatio": 1,
            "showPauseBorder": False,
            "createdDate": created_date,
            "createdTime": created_time,
            "goals": 0,
            "flashUntil": 0,
            "goalCooldown": 0,
            "ballVelocityBoost": 0,
            "ballVelocityDecay": 0,
            "attachments": [],
            "urls": urls
        }
        
        return bubble
    
    def _scan_evidence_files(self) -> List[Path]:
        """Scan evidence directory for .txt and .md files."""
        evidence_files = []
        
        if not self.evidence_root.exists():
            self.logger.warning(f"Evidence root directory {self.evidence_root} does not exist")
            return evidence_files
        
        for file_path in self.evidence_root.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in ['.txt', '.md']:
                evidence_files.append(file_path)
        
        self.logger.info(f"Found {len(evidence_files)} evidence files")
        return evidence_files
    
    def _process_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Process a single evidence file."""
        try:
            # Calculate file hash
            file_hash = self._calculate_file_hash(file_path)
            if not file_hash:
                return None
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create bubble
            bubble = self._create_bubble(file_path, content)
            
            # Log the processing
            self._log_file_processing(file_path, file_hash)
            
            return bubble
            
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {e}")
            return None
    
    def _log_file_processing(self, file_path: Path, file_hash: str):
        """Log file processing to CSV."""
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Ensure log file exists with headers
        log_exists = self.log_file.exists()
        
        with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not log_exists:
                writer.writerow(['filename', 'hash', 'timestamp', 'status'])
            
            writer.writerow([
                str(file_path.relative_to(self.evidence_root)),
                file_hash,
                timestamp,
                'processed'
            ])
    
    def compile_evidence(self) -> bool:
        """Main method to compile all evidence files."""
        self.logger.info("Starting evidence compilation...")
        
        # Scan for evidence files
        evidence_files = self._scan_evidence_files()
        if not evidence_files:
            self.logger.warning("No evidence files found")
            return False
        
        # Process files
        bubbles = []
        new_files_processed = 0
        
        for file_path in evidence_files:
            relative_path = str(file_path.relative_to(self.evidence_root))
            
            # Skip if already processed
            if relative_path in self.processed_files:
                self.logger.info(f"Skipping already processed file: {relative_path}")
                continue
            
            self.logger.info(f"Processing file: {relative_path}")
            bubble = self._process_file(file_path)
            
            if bubble:
                bubbles.append(bubble)
                new_files_processed += 1
                self.processed_files.add(relative_path)
        
        if not bubbles:
            self.logger.info("No new files to process")
            return True
        
        # Save bubbles to JSON
        try:
            with open(self.bubbles_file, 'w', encoding='utf-8') as f:
                json.dump(bubbles, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Successfully compiled {len(bubbles)} bubbles to {self.bubbles_file}")
            self.logger.info(f"Processed {new_files_processed} new files")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving bubbles file: {e}")
            return False
    
    def get_compilation_stats(self) -> Dict[str, Any]:
        """Get statistics about the compilation process."""
        stats = {
            "total_processed_files": len(self.processed_files),
            "bubbles_file_exists": self.bubbles_file.exists(),
            "log_file_exists": self.log_file.exists(),
            "evidence_root_exists": self.evidence_root.exists()
        }
        
        if self.bubbles_file.exists():
            try:
                with open(self.bubbles_file, 'r', encoding='utf-8') as f:
                    bubbles = json.load(f)
                stats["total_bubbles"] = len(bubbles)
            except:
                stats["total_bubbles"] = 0
        
        return stats


def main():
    """Main entry point for the evidence compiler."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Mindseye Evidence Compiler")
    parser.add_argument("--evidence-root", default="/evidence", 
                       help="Root directory to scan for evidence files")
    parser.add_argument("--output-dir", default=".", 
                       help="Output directory for compiled files")
    parser.add_argument("--stats", action="store_true", 
                       help="Show compilation statistics")
    
    args = parser.parse_args()
    
    # Create compiler instance
    compiler = MindseyeEvidenceCompiler(args.evidence_root, args.output_dir)
    
    if args.stats:
        stats = compiler.get_compilation_stats()
        print("Compilation Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    else:
        # Run compilation
        success = compiler.compile_evidence()
        if success:
            print("Evidence compilation completed successfully!")
        else:
            print("Evidence compilation failed. Check logs for details.")


if __name__ == "__main__":
    main()
