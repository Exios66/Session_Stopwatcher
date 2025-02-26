#!/usr/bin/env python3
"""
Session Stopwatcher Launcher
----------------------------
A script to launch any component of the Session Stopwatcher system.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Display the main menu."""
    clear_screen()
    print("=" * 50)
    print("         SESSION STOPWATCHER LAUNCHER         ")
    print("=" * 50)
    print("\nChoose a component to launch:\n")
    print("1. Web-based Stopwatch Application")
    print("2. Manifest Generator")
    print("3. Recording Session")
    print("4. Exit")
    print("\n" + "=" * 50)

def launch_stopwatch():
    """Launch the web-based stopwatch application."""
    try:
        html_path = Path("index.html").absolute()
        webbrowser.open(f'file://{html_path}')
        print(f"\nLaunched Stopwatch Application in your default browser.")
        input("\nPress Enter to return to the menu...")
    except Exception as e:
        print(f"\nError launching Stopwatch Application: {e}")
        input("\nPress Enter to return to the menu...")

def launch_manifest_generator():
    """Launch the manifest generator."""
    try:
        script_path = Path("Manifest-Generator/manifest.py").absolute()
        
        # Check if we're on Windows
        if os.name == 'nt':
            subprocess.run(["python", script_path], check=True)
        else:
            subprocess.run(["python3", script_path], check=True)
            
        print(f"\nManifest Generator completed.")
        input("\nPress Enter to return to the menu...")
    except Exception as e:
        print(f"\nError launching Manifest Generator: {e}")
        input("\nPress Enter to return to the menu...")

def launch_recording_session():
    """Launch the recording session application."""
    try:
        script_path = Path("Recording_Session/session_recorder.py").absolute()
        
        # Check if we're on Windows
        if os.name == 'nt':
            subprocess.run(["python", script_path], check=True)
        else:
            subprocess.run(["python3", script_path], check=True)
            
        print(f"\nRecording Session completed.")
        input("\nPress Enter to return to the menu...")
    except Exception as e:
        print(f"\nError launching Recording Session: {e}")
        input("\nPress Enter to return to the menu...")

def main():
    """Main function to run the launcher."""
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            launch_stopwatch()
        elif choice == '2':
            launch_manifest_generator()
        elif choice == '3':
            launch_recording_session()
        elif choice == '4':
            print("\nExiting Session Stopwatcher Launcher. Goodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 