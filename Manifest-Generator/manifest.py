#!/usr/bin/env python3
import json
import os
import logging
import sys
import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("manifest_generator.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("manifest-generator")

def get_valid_int(prompt, min_val, max_val):
    """Prompt until the user enters an integer between min_val and max_val."""
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                logger.warning(f"User entered value outside range: {value}")
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            logger.warning("User entered non-integer value")
            print("Invalid input. Please enter an integer.")
        except KeyboardInterrupt:
            logger.info("User interrupted input")
            print("\nInput interrupted. Exiting program.")
            sys.exit(0)

def get_yes_no_input(prompt):
    """Prompt until the user enters a valid yes/no answer."""
    while True:
        try:
            answer = input(prompt).strip().lower()
            if answer in ['yes', 'y']:
                return True
            elif answer in ['no', 'n']:
                return False
            else:
                logger.warning(f"Invalid yes/no input: {answer}")
                print("Please enter 'yes' or 'no'.")
        except KeyboardInterrupt:
            logger.info("User interrupted input")
            print("\nInput interrupted. Exiting program.")
            sys.exit(0)

def get_valid_option(prompt, options):
    """Prompt until the user enters one of the valid options provided in options list."""
    options_lower = [option.lower() for option in options]
    while True:
        try:
            answer = input(prompt).strip().lower()
            if answer in options_lower:
                return answer
            else:
                logger.warning(f"Invalid option input: {answer}")
                print(f"Invalid input. Please enter one of the following: {', '.join(options)}.")
        except KeyboardInterrupt:
            logger.info("User interrupted input")
            print("\nInput interrupted. Exiting program.")
            sys.exit(0)

def get_two_unique_numbers(prompt1, prompt2, min_val, max_val):
    """Prompt for two distinct integers within a specified range."""
    num1 = get_valid_int(prompt1, min_val, max_val)
    while True:
        num2 = get_valid_int(prompt2, min_val, max_val)
        if num2 == num1:
            logger.warning(f"User entered duplicate values: {num1}")
            print("The second number cannot be the same as the first. Please choose a different number.")
        else:
            return [num1, num2]

def get_date_input(prompt, format="%Y-%m-%d"):
    """Validate and get date input in the specified format."""
    while True:
        try:
            date_str = input(prompt)
            # Validate the date format
            datetime.datetime.strptime(date_str, format)
            return date_str
        except ValueError:
            logger.warning(f"Invalid date format entered: {date_str}")
            print(f"Invalid date format. Please use the format {format}")
        except KeyboardInterrupt:
            logger.info("User interrupted input")
            print("\nInput interrupted. Exiting program.")
            sys.exit(0)

def get_time_input(prompt, format="%H:%M"):
    """Validate and get time input in the specified format."""
    while True:
        try:
            time_str = input(prompt)
            # Validate the time format
            datetime.datetime.strptime(time_str, format)
            return time_str
        except ValueError:
            logger.warning(f"Invalid time format entered: {time_str}")
            print(f"Invalid time format. Please use the format {format}")
        except KeyboardInterrupt:
            logger.info("User interrupted input")
            print("\nInput interrupted. Exiting program.")
            sys.exit(0)

def save_data(data, output_path=None):
    """Save data to a JSON file with error handling."""
    try:
        # Determine the output path if not provided
        if output_path is None:
            downloads_path = Path.home() / "Downloads"
            if not downloads_path.exists():
                logger.warning("Downloads folder not found, using current directory")
                downloads_path = Path.cwd()
            
            # Create a filename with timestamp and participant ID
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            participant_id = data.get("participant_id", "unknown")
            filename = f"participant_{participant_id}_{timestamp}.json"
            output_path = downloads_path / filename
        
        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the data
        with open(output_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        
        logger.info(f"Data successfully saved to {output_path}")
        print(f"\nData successfully saved to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error writing file: {e}", exc_info=True)
        print(f"\nError writing file: {e}")
        return False

def main():
    logger.info("Starting manifest generator")
    print("Please answer the following questions:\n")
    
    try:
        data = {}
        # Basic Participant Information
        data["date"] = get_date_input("Enter today's date (YYYY-MM-DD): ")
        data["current_time"] = get_time_input("Enter the current time (HH:MM): ")
        data["participant_id"] = input("Enter participant ID number: ")
        data["participant_initials"] = input("Enter participant initials: ")
        data["assigned_subject_knowledge"] = input("Enter assigned subject knowledge: ")
        
        # Additional Information
        data["methods_of_analysis"] = get_valid_int("Enter the number of methods of analysis (1-4): ", 1, 4)
        recruitment_completed = get_yes_no_input("Was the recruitment form completed? (yes/no): ")
        data["recruitment_form_completed"] = recruitment_completed
        data["participant_gender"] = input("Enter participant gender: ")
        
        # Subject Knowledge Topics (two unique selections from 1 to 5)
        print("\nSelect two subject knowledge topics (choose two distinct numbers between 1 and 5).")
        data["subject_knowledge_topics"] = get_two_unique_numbers(
            "Enter first subject knowledge topic (1-5): ",
            "Enter second subject knowledge topic (1-5): ",
            1, 5
        )
        
        # Behavioral Profiles (two unique selections from 1 to 5)
        print("\nSelect two behavioral profiles (choose two distinct numbers between 1 and 5).")
        data["behavioral_profiles"] = get_two_unique_numbers(
            "Enter first behavioral profile (1-5): ",
            "Enter second behavioral profile (1-5): ",
            1, 5
        )
        
        # Eye-tracking and Additional Data Analysis Information
        print("\nPlease provide details regarding the eye tracking metrics:")
        data["screen_resolution"] = input("Enter the screen resolution (e.g., 1920x1080): ")
        data["screen_distance"] = input("Enter the approximate distance from the screen (e.g., in cm): ")
        data["sampling_rate"] = input("Enter the sampling rate (Hz): ")
        data["additional_notes"] = input("Enter any additional notes for data analysis: ")
        
        # Audio Recording Option (one stream, two streams, or none)
        audio_options = ["one", "two", "none"]
        data["audio_recording"] = get_valid_option(
            "Is audio being recorded on one stream, two streams, or none? (one/two/none): ",
            audio_options
        )
        
        # Add metadata
        data["generated_at"] = datetime.datetime.now().isoformat()
        data["generator_version"] = "1.1.0"
        
        # Save the data
        output_path = Path.home() / "Downloads" / f"participant_{data['participant_id']}.json"
        save_data(data, output_path)
        
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        print("\nProgram interrupted. Exiting.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\nAn unexpected error occurred: {e}")
        # Try to save any collected data as a backup
        if 'data' in locals() and data:
            backup_path = Path.cwd() / f"backup_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            save_data(data, backup_path)
            print(f"Partial data saved to {backup_path}")
        sys.exit(1)
    finally:
        logger.info("Manifest generator completed")

if __name__ == "__main__":
    main()