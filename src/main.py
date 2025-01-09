import json
from datetime import datetime
from habit import Habit
from habit_tracker import HabitTracker


# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":

    # Create an instance of the HabitTracker class, initializing the habit tracking system
    habit_tracker = HabitTracker()

    # Load existing data from a JSON file to restore previous habits and rewards
    habit_tracker.load_from_json()

    # Display the main menu, allowing the user to interact with the habit tracker
    habit_tracker.show_menu()