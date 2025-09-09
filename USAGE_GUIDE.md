# 🧠 Mindseye Evidence Compiler - Usage Guide

## Quick Start

### 1. Start the System
```bash
# Easy startup (recommended)
python start_mindseye.py

# Or manual startup
python mindseye_cli.py serve --port 8080
```

### 2. Open Web Interface
- Open your browser to: `http://localhost:8080`
- The interface will automatically load your evidence data

## Web Interface Features

### 🎯 Interactive Dashboard
- **Real-time Statistics**: View total bubbles, processed files, and evidence files
- **Quick Actions**: Compile evidence, browse files, add reports, export data
- **System Control**: Change evidence paths, clear data, view logs

### 🎈 Bubble Visualization
- **Interactive Canvas**: Click and view bubbles representing your evidence
- **Bubble Details**: Click any bubble to see full content, metadata, and links
- **Visual Navigation**: Bubbles are positioned randomly with different colors
- **Real-time Updates**: Data refreshes automatically after compilation

### 📁 File Management
- **File Browser**: Browse all evidence files with file types and sizes
- **File Preview**: Click files to view their content
- **File Types**: Supports `.txt` and `.md` files
- **Organized Structure**: Files are organized by type (incidents, reports, protocols)

### 📝 Report Entry
- **Add New Reports**: Create new evidence reports directly in the web interface
- **Report Types**: Incident reports, protocols, quality reports, safety reports
- **Rich Content**: Support for URLs, formatting, and metadata
- **Auto-Compilation**: New reports are automatically compiled into bubbles

### 📊 Data Export
- **JSON Export**: Export all bubble data as JSON
- **CSV Export**: Export compilation logs as CSV
- **Real-time Data**: Always get the latest compiled data

## Example Evidence Structure

The system comes with a comprehensive example evidence folder:

```
example_evidence/
├── incidents/
│   ├── patient_fall_2025_001.txt
│   └── medication_error_2025_002.txt
├── protocols/
│   └── infection_control_protocol.md
├── reports/
│   └── patient_safety_quarterly_2025_q1.md
└── images/
    └── (PNG files for bubble images)
```

## Using the System

### 1. Viewing Evidence
1. Open the web interface
2. Click "Browse Files" to see all evidence files
3. Click on any bubble to view its details
4. Use the bubble canvas to navigate between evidence items

### 2. Adding New Evidence
1. Click "Add Report" in the dashboard
2. Fill in the report form:
   - Title: Descriptive name for the report
   - Type: Select from incident, protocol, quality, safety, or other
   - Content: The main report content
   - URLs: Related links (one per line)
3. Click "Save Report"
4. The system will automatically compile the new report

### 3. Compiling Evidence
1. Click "Compile Evidence" in the dashboard
2. The system will scan for new or changed files
3. New bubbles will appear on the canvas
4. Statistics will update automatically

### 4. Exporting Data
1. Click "Export Data" in the dashboard
2. Choose to export bubbles JSON or compilation logs
3. Files will download to your computer

## Command Line Usage

### Basic Commands
```bash
# Compile evidence
python mindseye_cli.py compile --evidence-root ./example_evidence

# View statistics
python mindseye_cli.py stats

# Start web server
python mindseye_cli.py serve --port 8080

# Initialize evidence structure
python mindseye_cli.py init --evidence-root ./my_evidence
```

### Advanced Usage
```bash
# Compile with custom paths
python mindseye_cli.py compile --evidence-root /path/to/evidence --output-dir /path/to/output

# Start server on different host/port
python mindseye_cli.py serve --host 0.0.0.0 --port 9000

# Verbose compilation
python mindseye_cli.py compile --verbose
```

## File Formats

### Supported Input Files
- **Text Files** (`.txt`): Plain text evidence files
- **Markdown Files** (`.md`): Formatted documentation with headers, links, etc.

### Generated Output Files
- **bubbles.json**: Complete bubble data in MindReader format
- **compiler_log.csv**: Processing log with file hashes and timestamps
- **compiler.log**: Detailed system logs

## Bubble Format

Each evidence file becomes a bubble with:
- **Title**: Filename without extension
- **Description**: First 500 characters of content
- **Position**: Random x,y coordinates
- **Color**: Random pastel HSL color
- **Metadata**: Creation date, time, URLs, etc.
- **Links**: Extracted URLs from the content

## Troubleshooting

### Common Issues

1. **No bubbles showing**
   - Check if evidence files exist in the specified directory
   - Run compilation: Click "Compile Evidence"
   - Check file types: Only `.txt` and `.md` files are processed

2. **Web interface not loading**
   - Make sure the server is running: `python mindseye_cli.py serve`
   - Check the port: Default is 8080
   - Try a different browser or clear cache

3. **Files not found**
   - Check the evidence path in the dashboard
   - Make sure files are in the correct directory
   - Check file permissions

4. **Compilation errors**
   - Check the logs: Click "View Logs" in the dashboard
   - Verify file formats are correct
   - Check disk space and permissions

### Getting Help

1. **Check Logs**: Use the "View Logs" feature in the web interface
2. **System Statistics**: View the dashboard for current status
3. **File Browser**: Use the file browser to verify your evidence files
4. **Command Line**: Use `python mindseye_cli.py stats` for detailed information

## Security and Privacy

- **Offline Operation**: All processing happens locally
- **No Data Transmission**: Your evidence never leaves your computer
- **File Integrity**: SHA-256 hashing ensures data integrity
- **Audit Trail**: Complete logging of all processing activities

## Performance Tips

1. **Large Evidence Collections**: The system handles large collections efficiently
2. **File Organization**: Organize files in subdirectories for better management
3. **Regular Compilation**: Compile evidence regularly to keep data current
4. **Browser Performance**: Use modern browsers for best performance

## Future Features

The system is designed to be easily extensible:
- Database integration
- Cloud backup capabilities
- User authentication
- Advanced search and filtering
- Collaborative features
- Mobile app support

---

**Ready to use!** The Mindseye Evidence Compiler is now fully functional with a beautiful, interactive web interface that allows you to view, manage, and interact with your evidence data in real-time.
