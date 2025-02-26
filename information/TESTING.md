# Testing Guide for Manifest Generator

This document outlines procedures for testing the Manifest Generator to ensure it functions correctly in various scenarios.

## Prerequisites

- Python 3.x installed
- Access to the manifest.py script
- Basic understanding of terminal/command prompt

## Basic Functionality Tests

### Test 1: Normal Operation

**Procedure:**

1. Run the script: `python manifest.py`
2. Complete all prompts with valid inputs
3. Verify that a JSON file was created in the Downloads folder
4. Open the JSON file and check that all entered data is correctly stored

**Expected Result:**

- The script runs without errors
- A JSON file is created with a name following the pattern `participant_{ID}_{timestamp}.json`
- The JSON file contains all the data entered during the prompts

### Test 2: Input Validation

**Procedure:**

1. Run the script: `python manifest.py`
2. For numeric inputs, test the following:
   - Enter a number outside the allowed range
   - Enter alphabetical text instead of a number
   - Press enter without entering anything
3. For yes/no questions, test:
   - Enter values other than yes/no/y/n
   - Press enter without entering anything
4. For date/time inputs, test:
   - Enter incorrectly formatted dates/times
   - Enter invalid dates (e.g., February 30)

**Expected Result:**

- The script should provide informative error messages
- The script should prompt again for valid input
- The script should not crash on invalid input

### Test 3: Keyboard Interruption

**Procedure:**

1. Run the script: `python manifest.py`
2. While answering a prompt, press Ctrl+C to interrupt execution

**Expected Result:**

- The script should catch the interruption and exit gracefully
- An appropriate message should be displayed
- The script should log the interruption

## Error Handling Tests

### Test 4: File System Errors

**Procedure:**

1. Modify the script to save to a non-existent or protected directory
2. Run the modified script
3. Complete all prompts

**Expected Result:**

- The script should catch the file system error
- A backup file should be created in the current directory
- An appropriate error message should be displayed
- The error should be logged

### Test 5: Unexpected Exception

**Procedure:**

1. Modify the script to intentionally throw an exception during execution
   (e.g., add `raise Exception("Test exception")` in the main function)
2. Run the modified script
3. Complete prompts until the exception is triggered

**Expected Result:**

- The exception should be caught
- A backup file containing the data collected before the exception should be created
- An appropriate error message should be displayed
- The error should be logged with traceback information

## Integration Tests

### Test 6: JSON Data Structure

**Procedure:**

1. Run the script with various combinations of inputs
2. Use a JSON validator (e.g., jsonlint.com) to validate the structure
3. Parse the JSON file with another program or script

**Expected Result:**

- The JSON files should be well-formed and valid
- The structure should be consistent across all test runs
- All required fields should be present

### Test 7: Logging System

**Procedure:**

1. Run the script several times with different inputs
2. Check the manifest_generator.log file

**Expected Result:**

- The log file should contain entries for each run
- Appropriate log levels should be used for different events
- Errors and warnings should be clearly recorded
- The log format should follow the configured pattern

## Performance Tests

### Test 8: Large Input Data

**Procedure:**

1. Run the script and enter large amounts of data for text inputs
2. Try especially long inputs for free-text fields like additional_notes

**Expected Result:**

- The script should handle large inputs without issues
- The JSON file should correctly store the large data values

## Compatibility Tests

### Test 9: Cross-Platform Testing

**Procedure:**

1. Run the script on different operating systems:
   - Windows
   - macOS
   - Linux

**Expected Result:**

- The script should function identically on all platforms
- File paths should be correctly handled on each system
- No platform-specific errors should occur

### Test 10: Python Version Compatibility

**Procedure:**

1. Run the script with different Python versions:
   - Python 3.6
   - Python 3.7
   - Python 3.8
   - Python 3.9
   - Python 3.10+

**Expected Result:**

- The script should work on all tested Python versions
- No version-specific errors should occur
- Any differences in behavior should be documented

## Security Tests

### Test 11: File Permissions

**Procedure:**

1. Run the script with different user permissions
2. Verify the permissions on the generated files

**Expected Result:**

- The script should fail gracefully if it lacks required permissions
- Generated files should have appropriate permissions

## Reporting Test Results

For each test, document:

1. Test date and environment
2. Pass/fail status
3. Any unexpected behavior
4. Screenshots or terminal output where relevant
5. Suggested improvements or bug fixes
