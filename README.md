# 🧠 Mindseye Evidence Compiler

A comprehensive evidence management system designed for healthcare and safeguarding evidence compilation, specifically built for international accountability purposes. The system compiles evidence files into interactive bubble visualizations and provides robust logging and tracking capabilities.

## 🌟 Features

- **Recursive Evidence Scanning**: Automatically scans directories for `.txt` and `.md` files
- **Interactive Bubble Visualization**: Converts evidence into JSON bubble format for MindReader compatibility
- **Comprehensive Logging**: Tracks all processed files with hashing and timestamps
- **Web-Based GUI**: Modern, responsive interface for evidence management
- **Cross-Platform Support**: Works on Mac, Windows, and Linux
- **UTF-8 Support**: Handles international characters and content
- **Duplicate Detection**: Prevents reprocessing of already compiled files
- **Export Capabilities**: Export bubbles JSON and compilation logs
- **Future-Proof Architecture**: Modular design for easy extension

## 🚀 Quick Start

### 1. Initialize Evidence Structure
```bash
python mindseye_cli.py init --evidence-root /evidence
```

### 2. Start Web Interface
```bash
python mindseye_cli.py serve --port 8080
```

### 3. Compile Evidence
```bash
python mindseye_cli.py compile --evidence-root /evidence --output-dir .
```

### 4. View Statistics
```bash
python mindseye_cli.py stats
```

## 📁 Project Structure

```
MISS/
├── evidence_compiler.py      # Core evidence compilation engine
├── web_server.py             # Web server for GUI interface
├── mindseye_cli.py           # Command-line interface
├── index.html                # Web-based GUI
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── bubbles.json              # Generated bubble data (after compilation)
├── compiler_log.csv          # Processing log (after compilation)
└── evidence/                 # Evidence files directory
    ├── images/               # Images for bubbles
    ├── documents/            # Document files
    └── reports/              # Report files
```

## 🔧 Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Setup
1. Clone or download the project
2. Navigate to the project directory
3. (Optional) Create a virtual environment:
   ```bash
   python -m venv mindseye_env
   source mindseye_env/bin/activate  # On Windows: mindseye_env\Scripts\activate
   ```

## 📖 Usage

### Command Line Interface

#### Compile Evidence
```bash
# Basic compilation
python mindseye_cli.py compile

# With custom paths
python mindseye_cli.py compile --evidence-root /path/to/evidence --output-dir /path/to/output

# Verbose output
python mindseye_cli.py compile --verbose
```

#### View Statistics
```bash
python mindseye_cli.py stats --evidence-root /evidence --output-dir .
```

#### Start Web Server
```bash
# Default (localhost:8080)
python mindseye_cli.py serve

# Custom host and port
python mindseye_cli.py serve --host 0.0.0.0 --port 9000
```

#### Initialize Evidence Structure
```bash
python mindseye_cli.py init --evidence-root /evidence
```

### Web Interface

1. Start the web server: `python mindseye_cli.py serve`
2. Open your browser to `http://localhost:8080`
3. Use the GUI to:
   - Browse evidence files
   - Compile evidence
   - View bubble previews
   - Export data
   - Monitor compilation logs

### Direct Python API

```python
from evidence_compiler import MindseyeEvidenceCompiler

# Initialize compiler
compiler = MindseyeEvidenceCompiler("/evidence", ".")

# Compile evidence
success = compiler.compile_evidence()

# Get statistics
stats = compiler.get_compilation_stats()
print(f"Total bubbles: {stats['total_bubbles']}")
```

## 🎯 Bubble Format

Each evidence file is converted to a bubble with the following JSON structure:

```json
{
  "title": "filename_without_extension",
  "description": "First 500 characters of file content",
  "x": 39,
  "y": 290.81,
  "vx": -1.15,
  "vy": 0.80,
  "color": "hsl(146.92, 100%, 70%)",
  "textColor": "yellow",
  "radius": 28,
  "font": "Trebuchet MS",
  "image": "images/filename.png",
  "glow": true,
  "fontSize": 8,
  "rotation": 0,
  "fixed": true,
  "static": true,
  "shape": "circle",
  "heightRatio": 1,
  "showPauseBorder": false,
  "createdDate": "2025-01-27",
  "createdTime": "23:27:46",
  "goals": 0,
  "flashUntil": 0,
  "goalCooldown": 0,
  "ballVelocityBoost": 0,
  "ballVelocityDecay": 0,
  "attachments": [],
  "urls": [
    {
      "href": "https://example.com",
      "title": "example.com"
    }
  ]
}
```

## 📊 Logging

The system maintains detailed logs in CSV format (`compiler_log.csv`):

| Column | Description |
|--------|-------------|
| filename | Relative path to the processed file |
| hash | SHA-256 hash of the file content |
| timestamp | When the file was processed |
| status | Processing status (processed/error) |

## 🔒 Security & Privacy

- **Offline Operation**: Works without internet connection
- **File Hashing**: SHA-256 hashing for integrity verification
- **No Data Transmission**: All processing happens locally
- **UTF-8 Support**: Handles international content properly
- **Modular Design**: Easy to add encryption or cloud backup

## 🛠️ Development

### Adding New Features

The system is designed to be easily extensible:

1. **Database Integration**: Add database support in `evidence_compiler.py`
2. **Cloud Backup**: Implement cloud storage in a new module
3. **Authentication**: Add login system to `web_server.py`
4. **Advanced Filtering**: Extend file scanning logic
5. **Custom Formats**: Add support for additional file types

### Testing

```bash
# Create test evidence
python mindseye_cli.py init --evidence-root ./test_evidence

# Compile test evidence
python mindseye_cli.py compile --evidence-root ./test_evidence

# View results
python mindseye_cli.py stats --evidence-root ./test_evidence
```

## 📝 File Types Supported

- **Text Files** (`.txt`): Plain text evidence files
- **Markdown Files** (`.md`): Formatted documentation
- **Images** (`.png`): Automatically linked if matching filename exists

## 🌍 International Support

- Full UTF-8 support for international characters
- Cross-platform compatibility (Mac/Windows/Linux)
- Proper handling of file paths and encodings

## ⚠️ Important Notes

- **Evidence Integrity**: Files are hashed to prevent duplicate processing
- **Backup Recommended**: Always backup your evidence before processing
- **Large Files**: System handles large evidence collections efficiently
- **Memory Usage**: Processes files individually to minimize memory usage

## 🤝 Contributing

This system is designed for Maya Patterson's healthcare and safeguarding evidence compilation needs. The modular architecture allows for easy customization and extension based on specific requirements.

## 📄 License

This project is designed for evidence compilation and accountability purposes. Please ensure compliance with local data protection and privacy regulations when handling sensitive information.

---

**Built with ❤️ for evidence-based accountability and transparency**
