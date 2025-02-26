# Recording Session

This module provides functionality to record precise timestamps during research sessions or experiments. It acts as a timeclock system that records the exact time when specific events occur, triggered by keyboard input.

## Features

- Start a recording session to capture timestamps
- Record timestamps with millisecond precision using keyboard input (Enter or 'e' key)
- Add optional notes to each recorded timestamp
- Automatic participant ID collection at the beginning of a session
- Export session data as CSV to the Downloads folder
- Simple dialog-based interface that stays on top of other windows

## Requirements

- Python 3.x
- pynput library for keyboard input handling
- tkinter for GUI dialogs (included in standard Python installation)

## Installation

1. Ensure you have Python 3.x installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Navigate to the Recording_Session directory:

```bash
cd Recording_Session
```

2. Run the session recorder:

```bash
python session_recorder.py
```

3. When the application starts:
   - A dialog will appear indicating the session has started
   - Press Enter or 'e' to record a timestamp
   - The first timestamp will prompt you to enter a participant ID
   - After each timestamp, you can add optional notes
   - Press 'r' to end the session and save the CSV file

## Data Format

The recorded data is saved as a CSV file with the following columns:

- `timestamp_id`: Sequential ID for each timestamp
- `date`: Date in YYYY-MM-DD format
- `hour`: Hour (24-hour format)
- `minute`: Minute
- `second`: Second
- `millisecond`: Millisecond
- `iso_timestamp`: Full ISO format timestamp
- `notes`: Optional notes added by the user

## Output Files

CSV files are saved to the user's Downloads folder with the naming format:
`session_recording_[PARTICIPANT_ID]_[TIMESTAMP].csv`

## Integration with Manifest Generator

This module complements the Manifest Generator by providing real-time data collection capability during experimental sessions. Consider using the Manifest Generator to collect participant metadata before starting a recording session.
