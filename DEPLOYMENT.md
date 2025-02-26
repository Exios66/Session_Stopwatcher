# Deployment & Configuration Guide for Manifest Generator

## Deployment Options

### 1. Basic Deployment

The simplest deployment method is to copy the `manifest.py` script to the target machine and run it with Python:

```bash
python /path/to/manifest.py
```

### 2. Package Deployment

For easier distribution, you can package the script:

```bash
# Install PyInstaller
pip install pyinstaller

# Create a standalone executable
pyinstaller --onefile Manifest-Generator/manifest.py
```

The executable will be created in the `dist` directory and can be distributed to users without requiring Python installation.

### 3. Scheduled Operation

For automated data collection, set up scheduled runs using cron (Linux/Mac) or Task Scheduler (Windows):

**Linux/Mac (cron):**

```bash
# Edit crontab
crontab -e

# Add a line to run daily at 9am
0 9 * * * /usr/bin/python /path/to/manifest.py
```

**Windows (Task Scheduler):**

1. Open Task Scheduler
2. Create a new Basic Task
3. Set the trigger (daily, weekly, etc.)
4. Set the action to "Start a program"
5. Browse to `python.exe` as the program and add the path to manifest.py as argument

## Configuration Options

### Logging Configuration

The logging system can be configured by modifying these parameters in the script:

```python
# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Can be changed to DEBUG, WARNING, ERROR, or CRITICAL
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("manifest_generator.log"),  # Change log file path
        logging.StreamHandler(sys.stdout)  # Remove for silent operation
    ]
)
```

### File Output Location

By default, files are saved to the user's Downloads folder. This can be modified in the `save_data` function:

```python
# Change output directory
downloads_path = Path.home() / "Documents"  # Change to preferred directory
```

### Input Validation Parameters

Numeric input validations can be adjusted by changing the parameters in function calls:

```python
# Example: Change subject knowledge topics range from 1-5 to 1-10
data["subject_knowledge_topics"] = get_two_unique_numbers(
    "Enter first subject knowledge topic (1-10): ",
    "Enter second subject knowledge topic (1-10): ",
    1, 10  # Modified range
)
```

## Operational Variables

### Version Tracking

The manifest generator includes version information in the generated JSON:

```python
data["generator_version"] = "1.1.0"  # Update this value for new releases
```

### Metadata Fields

Additional metadata fields can be added to the `data` dictionary:

```python
# Example: Add organization or study identifier
data["organization"] = "Research Institute XYZ"
data["study_id"] = "STUDY-2023-001"
```

### Error Handling & Backup

The script includes robust error handling and creates backup files in case of exceptions:

```python
# Backup path can be modified here:
backup_path = Path.cwd() / f"backup_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
```

## Production Considerations

### Data Security

1. **File Permissions**: Ensure the script and log files have appropriate permissions

   ```bash
   chmod 700 manifest.py
   chmod 600 manifest_generator.log
   ```

2. **Data Encryption**: For sensitive participant data, consider encrypting the JSON output:

   ```python
   # Add encryption before writing to file (requires additional packages)
   from cryptography.fernet import Fernet
   key = Fernet.generate_key()
   cipher = Fernet(key)
   encrypted_data = cipher.encrypt(json.dumps(data).encode())
   # Write encrypted_data to file
   ```

### Testing & Validation

Before production deployment:

1. Test with various input combinations
2. Verify error handling by intentionally causing exceptions
3. Check log files for appropriate information capture
4. Validate JSON output schema consistency

### User Training

Provide users with:

1. Basic operation guide
2. List of required information to have ready before running
3. Contact information for support
4. Examples of valid inputs for each prompt
