#!/usr/bin/env python3
import os
import csv
import time
import datetime
import platform
import threading
import logging
import json
import tempfile
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, font
from pynput import keyboard

# Configure logging
log_dir = os.path.join(str(Path.home()), ".session_recorder_logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"session_recorder_{datetime.datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SessionRecorder")

class SessionRecorder:
    """
    A class that records timestamps and notes during a session,
    triggered by keyboard events (Enter or 'e' key).
    """
    
    def __init__(self):
        # Initialize variables
        self.recording = False
        self.timestamps = []
        self.participant_id = None
        self.start_date = None
        self.start_time = None
        self.root = None
        self.listener = None
        self.status_window = None
        self.status_label = None
        self.time_label = None
        self.count_label = None
        self.last_timestamp_label = None
        self.platform_info = self._get_platform_info()
        self.timer_thread = None
        self.timer_running = False
        self.notes_dialog_active = False  # Flag to track when notes dialog is active
        
        # Get system info for logging
        logger.info(f"Session Recorder initialized on {self.platform_info}")
        
        # Setup the tkinter windows
        self.setup_tkinter()
        
    def _get_platform_info(self):
        """Get detailed platform information for diagnostics."""
        info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        }
        return info
        
    def setup_tkinter(self):
        """Set up the tkinter root window and status window."""
        try:
            # Main root window (hidden)
            self.root = tk.Tk()
            self.root.withdraw()  # Hide the main window
            self.root.title("Session Recorder")
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            
            # Configure the application to stay on top
            self.root.attributes("-topmost", True)
            
            # Create a custom theme for better appearance
            self.style = ttk.Style()
            self.style.theme_use('clam')  # Use the 'clam' theme as base
            
            # Create status window
            self.create_status_window()
            
            # Position the windows
            self.center_window(self.root)
            
            logger.debug("Tkinter UI setup complete")
        except Exception as e:
            logger.error(f"Error setting up tkinter: {e}", exc_info=True)
            raise
            
    def create_status_window(self):
        """Create a small status window that shows the current recording status."""
        self.status_window = tk.Toplevel(self.root)
        self.status_window.title("Session Recorder Status")
        self.status_window.attributes("-topmost", True)
        self.status_window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Make it non-resizable
        self.status_window.resizable(False, False)
        
        # Add padding
        frame = ttk.Frame(self.status_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Status indicator
        status_frame = ttk.Frame(frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        self.status_label = ttk.Label(status_frame, text="Ready", foreground="blue")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Clock/Timer
        time_frame = ttk.Frame(frame)
        time_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(time_frame, text="Session Time:").pack(side=tk.LEFT)
        self.time_label = ttk.Label(time_frame, text="00:00:00", font=font.Font(size=12, weight='bold'))
        self.time_label.pack(side=tk.LEFT, padx=5)
        
        # Timestamps counter
        count_frame = ttk.Frame(frame)
        count_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(count_frame, text="Timestamps:").pack(side=tk.LEFT)
        self.count_label = ttk.Label(count_frame, text="0")
        self.count_label.pack(side=tk.LEFT, padx=5)
        
        # Last timestamp
        last_ts_frame = ttk.Frame(frame)
        last_ts_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(last_ts_frame, text="Last Timestamp:").pack(side=tk.LEFT)
        self.last_timestamp_label = ttk.Label(last_ts_frame, text="None")
        self.last_timestamp_label.pack(side=tk.LEFT, padx=5)
        
        # Key commands reminder
        help_frame = ttk.LabelFrame(frame, text="Commands")
        help_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(help_frame, text="Enter/E: Record timestamp").pack(anchor=tk.W)
        ttk.Label(help_frame, text="R: End session and save").pack(anchor=tk.W)
        
        # Center the status window
        self.center_window(self.status_window)
        
        logger.debug("Status window created")
        
    def center_window(self, window):
        """Center a window on the screen."""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        if width == 1 and height == 1:  # If window size not yet determined
            width = 300
            height = 250
            
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
        logger.debug(f"Window centered at position {x},{y} with size {width}x{height}")
        
    def update_timer(self):
        """Update the session timer display."""
        if not self.timer_running:
            return
            
        if self.start_time:
            elapsed = datetime.datetime.now() - self.start_time
            hours, remainder = divmod(elapsed.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            self.time_label.config(text=time_str)
            
        # Schedule the next update
        self.root.after(1000, self.update_timer)
        
    def on_key_press(self, key):
        """Handle key presses."""
        try:
            # Check if Enter or 'e' key was pressed
            if (key == keyboard.Key.enter or 
                (hasattr(key, 'char') and key.char and key.char.lower() == 'e')):
                
                logger.info(f"Timestamp triggered by key: {key}")
                self.record_timestamp()
                
            # Check if 'r' key was pressed to end the session, but only if notes dialog is not active
            elif (hasattr(key, 'char') and key.char and key.char.lower() == 'r' and 
                  not self.notes_dialog_active):
                logger.info("Session end triggered by 'r' key")
                self.end_session()
                return False  # Stop listener
                
        except Exception as e:
            logger.error(f"Error processing key press: {e}", exc_info=True)
            messagebox.showerror("Error", f"An error occurred while processing key press: {e}")
            
    def record_timestamp(self):
        """Record a timestamp with the current time."""
        if not self.recording:
            logger.warning("Attempted to record timestamp but recording is not active")
            return
            
        # Get the current time
        current_time = datetime.datetime.now()
        logger.debug(f"Recording timestamp at {current_time.isoformat()}")
        
        # If this is the first timestamp, get the participant ID
        if not self.participant_id:
            logger.info("First timestamp - requesting participant ID")
            participant_id = simpledialog.askstring("Participant ID", 
                                                  "Enter participant ID number:",
                                                  parent=self.root)
            if participant_id:
                self.participant_id = participant_id
                self.start_date = current_time.strftime("%Y-%m-%d")
                logger.info(f"Participant ID set to: {participant_id}")
                
                # Update status window title with participant ID
                self.status_window.title(f"Session Recorder - Participant {participant_id}")
            else:
                logger.warning("No participant ID provided")
                messagebox.showwarning("Warning", "Participant ID is required to start recording.")
                return
        
        # Format the timestamp components
        timestamp_data = {
            'timestamp_id': len(self.timestamps) + 1,
            'date': current_time.strftime("%Y-%m-%d"),
            'hour': current_time.hour,
            'minute': current_time.minute,
            'second': current_time.second,
            'millisecond': current_time.microsecond // 1000,  # Convert microseconds to milliseconds
            'iso_timestamp': current_time.isoformat(),
            'notes': ''
        }
        
        # Visual feedback - flash the status window
        self.flash_status()
        
        # Ask for additional notes
        self.root.after(100, lambda: self.get_notes(timestamp_data))
    
    def flash_status(self):
        """Provide visual feedback by briefly changing the status label color."""
        original_color = self.status_label.cget("foreground")
        self.status_label.config(foreground="green")
        self.root.after(500, lambda: self.status_label.config(foreground=original_color))
    
    def get_notes(self, timestamp_data):
        """Prompt the user for additional notes."""
        logger.debug(f"Requesting notes for timestamp #{timestamp_data['timestamp_id']}")
        
        # Set flag to indicate notes dialog is active
        self.notes_dialog_active = True
        
        # Use a custom dialog that will update our flag when closed
        notes = self.custom_notes_dialog("Additional Notes", 
                                        f"Add notes for timestamp #{timestamp_data['timestamp_id']} (optional):",
                                        parent=self.root)
        
        # Reset flag since dialog is now closed
        self.notes_dialog_active = False
        
        if notes:
            timestamp_data['notes'] = notes
            logger.debug(f"Notes added: {notes}")
            
        self.timestamps.append(timestamp_data)
        
        # Update the status window
        self.count_label.config(text=str(len(self.timestamps)))
        time_str = timestamp_data['iso_timestamp'].split('T')[1]
        self.last_timestamp_label.config(text=time_str)
        
        # Create auto-backup of data
        self.auto_backup_data()
        
        # Show confirmation message
        timestamp_id = timestamp_data['timestamp_id']
        messagebox.showinfo("Timestamp Recorded", 
                           f"Timestamp #{timestamp_id} recorded at {time_str}")
        logger.info(f"Timestamp #{timestamp_id} recorded at {time_str}")
    
    def custom_notes_dialog(self, title, prompt, parent=None):
        """
        Custom dialog for getting notes that properly handles the notes_dialog_active flag.
        This replaces the standard simpledialog.askstring to properly track when the dialog is active.
        """
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.transient(parent)
        dialog.resizable(False, False)
        
        # Make dialog modal
        dialog.grab_set()
        
        # Create dialog contents
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Prompt label
        ttk.Label(frame, text=prompt).pack(anchor=tk.W, pady=(0, 5))
        
        # Text entry
        entry = ttk.Entry(frame, width=50)
        entry.pack(fill=tk.X, pady=5)
        entry.focus_set()
        
        # Result variable
        result = [None]  # Use list to store result (allows modification in nested function)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def on_ok():
            result[0] = entry.get()
            dialog.destroy()
            
        def on_cancel():
            dialog.destroy()
            
        ok_button = ttk.Button(button_frame, text="OK", command=on_ok, width=10)
        ok_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel, width=10)
        cancel_button.pack(side=tk.RIGHT)
        
        # Set up key bindings
        dialog.bind("<Return>", lambda event: on_ok())
        dialog.bind("<Escape>", lambda event: on_cancel())
        
        # Center the dialog
        self.center_window(dialog)
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result[0]
    
    def auto_backup_data(self):
        """Create an automatic backup of the recorded data."""
        try:
            if not self.timestamps or not self.participant_id:
                return
                
            # Use temp directory for backup
            temp_dir = tempfile.gettempdir()
            backup_file = os.path.join(temp_dir, f"session_backup_{self.participant_id}.json")
            
            with open(backup_file, 'w') as f:
                json.dump({
                    'participant_id': self.participant_id,
                    'start_date': self.start_date,
                    'timestamps': self.timestamps,
                    'backup_time': datetime.datetime.now().isoformat()
                }, f, indent=2)
                
            logger.debug(f"Auto-backup created at {backup_file}")
        except Exception as e:
            logger.error(f"Failed to create auto-backup: {e}", exc_info=True)
    
    def start_session(self):
        """Start recording session and keyboard listener."""
        if self.recording:
            logger.warning("Attempted to start session but it's already running")
            messagebox.showinfo("Info", "Session already in progress.")
            return
            
        logger.info("Starting recording session")
        self.recording = True
        self.timestamps = []
        self.participant_id = None
        self.start_date = None
        self.start_time = datetime.datetime.now()
        self.notes_dialog_active = False
        
        # Update status window
        self.status_label.config(text="Recording", foreground="green")
        self.count_label.config(text="0")
        self.last_timestamp_label.config(text="None")
        
        # Start the timer
        self.timer_running = True
        self.update_timer()
        
        # Start the keyboard listener in a separate thread
        try:
            self.listener = keyboard.Listener(on_press=self.on_key_press)
            self.listener.start()
            logger.debug("Keyboard listener started")
        except Exception as e:
            logger.error(f"Failed to start keyboard listener: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to start keyboard listener: {e}")
            self.recording = False
            return
        
        messagebox.showinfo("Session Started", 
                           "Recording session started!\n\n" +
                           "Press Enter or 'e' to record a timestamp.\n" +
                           "Press 'r' to end the session and save data.")
                           
        # Make status window visible
        self.status_window.deiconify()
                           
        # Keep application running
        self.root.mainloop()
        
    def end_session(self):
        """End the recording session and export the data."""
        if not self.recording:
            logger.warning("Attempted to end session but no session is active")
            return
            
        logger.info("Ending recording session")
        self.recording = False
        self.timer_running = False
        
        # Update status window
        self.status_label.config(text="Session Ended", foreground="blue")
        
        # Only export if we have timestamps and participant ID
        if self.timestamps and self.participant_id:
            success = self.export_data()
            if success:
                messagebox.showinfo("Session Ended", 
                                   f"Session for Participant {self.participant_id} ended.\n" +
                                   f"Data saved to Downloads folder.")
                logger.info(f"Session data saved for participant {self.participant_id}")
            else:
                # If export failed, keep the auto-backup
                backup_path = os.path.join(tempfile.gettempdir(), f"session_backup_{self.participant_id}.json")
                messagebox.showinfo("Session Ended", 
                                   f"Session ended but data export failed.\n" +
                                   f"Backup data available at: {backup_path}")
                logger.warning(f"Session export failed, using backup at {backup_path}")
        else:
            messagebox.showinfo("Session Ended", "Session ended. No data to save.")
            logger.info("Session ended with no data to save")
            
        # Close the tkinter window
        self.root.quit()
        
    def export_data(self):
        """Export the recorded timestamps to a CSV file."""
        try:
            # Create the filename with participant ID and date
            date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"session_recording_{self.participant_id}_{date_str}.csv"
            
            # Get the downloads folder path
            downloads_path = str(Path.home() / "Downloads")
            filepath = os.path.join(downloads_path, filename)
            
            logger.debug(f"Exporting data to {filepath}")
            
            # Define CSV headers
            fieldnames = ['timestamp_id', 'date', 'hour', 'minute', 'second', 
                         'millisecond', 'iso_timestamp', 'notes']
            
            # Write the data to CSV
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                # Add metadata as a comment
                csvfile.write(f"# Session Recording for Participant: {self.participant_id}\n")
                csvfile.write(f"# Date: {self.start_date}\n")
                csvfile.write(f"# Total Timestamps: {len(self.timestamps)}\n")
                csvfile.write(f"# System Info: {json.dumps(self.platform_info)}\n")
                
                # Write all timestamps
                for timestamp in self.timestamps:
                    writer.writerow(timestamp)
                    
            logger.info(f"Successfully exported {len(self.timestamps)} timestamps to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export data: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to export data: {e}")
            return False
    
    def on_close(self):
        """Handle window close event."""
        if self.recording:
            if messagebox.askyesno("End Session", 
                                  "A recording session is in progress.\n" +
                                  "Do you want to end the session and save data?"):
                self.end_session()
            else:
                # User canceled, don't close
                return
        
        # No recording in progress, just close
        logger.info("Application closed by user")
        self.root.quit()


def check_environment():
    """Check if the environment is properly set up."""
    issues = []
    
    # Check if tkinter is working
    try:
        root = tk.Tk()
        root.destroy()
    except:
        issues.append("Tkinter is not working properly. Make sure Python is installed with Tkinter support.")
    
    # Check if pynput is installed
    try:
        import pynput
    except ImportError:
        issues.append("The pynput package is not installed. Install it with: pip install pynput")
    
    # Check for write permissions in Downloads folder
    downloads_path = str(Path.home() / "Downloads")
    if not os.access(downloads_path, os.W_OK):
        issues.append(f"No write permission in Downloads folder: {downloads_path}")
    
    return issues


def main():
    """Main function to start the application."""
    print("Session Recorder")
    print("================")
    print(f"Log file: {log_file}")
    print("This application will record timestamps when you press Enter or 'e'.")
    print("Press 'r' to end the session and save the data to a CSV file.")
    
    # Check environment before starting
    issues = check_environment()
    if issues:
        print("\nEnvironment Issues Detected:")
        for issue in issues:
            print(f"- {issue}")
        print("\nPlease resolve these issues before running the application.")
        
        if 'pynput' in str(issues):
            print("\nTo install pynput, run: pip install pynput")
        
        # Also show an error dialog if possible
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Environment Issues", 
                               "The following issues were detected:\n\n" + 
                               "\n".join([f"• {issue}" for issue in issues]))
            root.destroy()
        except:
            # If tkinter doesn't work, we've already reported this in the console
            pass
            
        return
    
    print("\nStarting recording session...\n")
    
    # Create and start the recorder
    try:
        recorder = SessionRecorder()
        recorder.start_session()
    except Exception as e:
        logger.critical(f"Failed to start application: {e}", exc_info=True)
        print(f"\nCritical error: {e}")
        print(f"See log file for details: {log_file}")


if __name__ == "__main__":
    main() 