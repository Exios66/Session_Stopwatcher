#!/usr/bin/env python3
import os
import csv
import time
import datetime
import platform
import threading
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog, messagebox
from pynput import keyboard

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
        self.root = None
        self.listener = None
        
        # Setup the hidden tkinter root window for dialogs
        self.setup_tkinter()
        
    def setup_tkinter(self):
        """Set up the hidden tkinter root window for dialogs."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window
        
        # Set window title and icon
        self.root.title("Session Recorder")
        
        # Configure the application to stay on top
        self.root.attributes("-topmost", True)
        
        # Position the window (centered)
        self.center_window()
        
    def center_window(self):
        """Center the hidden window."""
        self.root.update_idletasks()
        width = 300
        height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def on_key_press(self, key):
        """Handle key presses."""
        try:
            # Check if Enter or 'e' key was pressed
            if (key == keyboard.Key.enter or 
                (hasattr(key, 'char') and key.char and key.char.lower() == 'e')):
                
                self.record_timestamp()
                
            # Check if 'r' key was pressed to end the session
            elif hasattr(key, 'char') and key.char and key.char.lower() == 'r':
                self.end_session()
                return False  # Stop listener
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while processing key press: {e}")
            
    def record_timestamp(self):
        """Record a timestamp with the current time."""
        if not self.recording:
            return
            
        # Get the current time
        current_time = datetime.datetime.now()
        
        # If this is the first timestamp, get the participant ID
        if not self.participant_id:
            participant_id = simpledialog.askstring("Participant ID", 
                                                  "Enter participant ID number:",
                                                  parent=self.root)
            if participant_id:
                self.participant_id = participant_id
                self.start_date = current_time.strftime("%Y-%m-%d")
            else:
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
        
        # Ask for additional notes
        self.root.after(100, lambda: self.get_notes(timestamp_data))
    
    def get_notes(self, timestamp_data):
        """Prompt the user for additional notes."""
        notes = simpledialog.askstring("Additional Notes", 
                                      "Add notes for this timestamp (optional):",
                                      parent=self.root)
        if notes:
            timestamp_data['notes'] = notes
            
        self.timestamps.append(timestamp_data)
        
        # Show confirmation message
        timestamp_id = timestamp_data['timestamp_id']
        time_str = timestamp_data['iso_timestamp'].split('T')[1]
        messagebox.showinfo("Timestamp Recorded", 
                           f"Timestamp #{timestamp_id} recorded at {time_str}")
    
    def start_session(self):
        """Start recording session and keyboard listener."""
        if self.recording:
            messagebox.showinfo("Info", "Session already in progress.")
            return
            
        self.recording = True
        self.timestamps = []
        self.participant_id = None
        self.start_date = None
        
        # Start the keyboard listener in a separate thread
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        
        messagebox.showinfo("Session Started", 
                           "Recording session started!\n\n" +
                           "Press Enter or 'e' to record a timestamp.\n" +
                           "Press 'r' to end the session and save data.")
                           
        # Keep application running
        self.root.mainloop()
        
    def end_session(self):
        """End the recording session and export the data."""
        if not self.recording:
            return
            
        self.recording = False
        
        # Only export if we have timestamps and participant ID
        if self.timestamps and self.participant_id:
            self.export_data()
            messagebox.showinfo("Session Ended", 
                               f"Session for Participant {self.participant_id} ended.\n" +
                               f"Data saved to Downloads folder.")
        else:
            messagebox.showinfo("Session Ended", "Session ended. No data to save.")
            
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
                
                # Write all timestamps
                for timestamp in self.timestamps:
                    writer.writerow(timestamp)
                    
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {e}")
            return False


def main():
    """Main function to start the application."""
    print("Session Recorder")
    print("================")
    print("This application will record timestamps when you press Enter or 'e'.")
    print("Press 'r' to end the session and save the data to a CSV file.")
    print("\nStarting recording session...\n")
    
    # Create and start the recorder
    recorder = SessionRecorder()
    recorder.start_session()


if __name__ == "__main__":
    main() 