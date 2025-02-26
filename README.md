# Session Stopwatcher

This repository contains two main components:

1. **Web-based Stopwatch Application** - A comprehensive stopwatch tool for timing and tracking sessions
2. **Manifest Generator** - A Python utility for collecting participant information and study metadata

## Manifest Generator

The Manifest Generator is a Python-based command-line tool designed for research studies to document participant information, study parameters, and configuration details. The tool guides researchers through a series of prompts and saves the collected data as a structured JSON file.

### Features

- Collection of participant demographics and identifiers
- Study configuration parameters (subject knowledge, behavioral profiles)
- Eye-tracking metrics documentation
- Audio recording configuration
- Error handling and validation of input
- Logging system for troubleshooting
- Automatic file naming with timestamps and participant IDs

### Installation

No external dependencies are required. The tool uses only Python standard library modules.

```bash
# Clone the repository
git clone https://github.com/yourusername/Session_Stopwatcher.git

# Navigate to the Manifest Generator directory
cd Session_Stopwatcher/Manifest-Generator
```

### Usage

Simply run the Python script:

```bash
python manifest.py
```

Follow the prompts to input all required information. The resulting JSON file will be saved to the user's Downloads folder by default, named with the pattern `participant_{ID}_{timestamp}.json`.

### Deployment

For deployment in production environments:

1. Ensure Python 3.x is installed on the target system
2. Copy the manifest.py file to a known location
3. Make the file executable if needed: `chmod +x manifest.py`
4. Consider adding the script to your system path for easy access

### Configuration Options

The manifest generator can be configured through edits to the script:

- Changing default file paths
- Modifying the logger configuration
- Adjusting the valid ranges for numeric inputs
- Adding or removing data collection prompts

### Error Handling

The script includes comprehensive error handling:

- Input validation with user feedback
- Exception handling for file operations
- Graceful exit on keyboard interrupts
- Backup file creation on unexpected errors

## Stopwatch Web Application

The repository also includes a comprehensive web-based stopwatch application for timing sessions and collecting time-based data.

For more information on the Stopwatch application, see the main HTML file (index.html).
