import json
from datetime import datetime
from habit import Habit
from habit_tracker import HabitTracker
import tkinter as tk
from gui import HabitTrackerGUI # Import the GUI class
# from habit_tracker import HabitTracker # Keep CLI imports if needed later or for args
# import os # Keep if needed for CLI path logic

def run_cli():
    # This function now contains the original CLI logic
    # (You would move the original content of main() here)
    print("Starting Habit Tracker (CLI Mode)...")
    # tracker = HabitTracker()
    # script_dir = os.path.dirname(__file__)
    # json_path = os.path.join(script_dir, 'habits_dataset.json')
    # tracker.load_from_json(json_path)
    # tracker.run() # Assuming run() contains the main CLI loop
    # tracker.save_to_json(json_path) # Save on exit
    print("CLI Mode not fully implemented here yet.")


def run_gui():
    root = tk.Tk()
    app = HabitTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    # For now, default to GUI. Could add argparse later to choose.
    # Example:
    # import argparse
    # parser = argparse.ArgumentParser(description="Habit Tracker")
    # parser.add_argument('--cli', action='store_true', help='Run in command-line interface mode')
    # args = parser.parse_args()
    # if args.cli:
    #    run_cli()
    # else:
    #    run_gui()

    run_gui() # Default to GUI