from datetime import datetime, timedelta


class Habit:
    # Represents a single habit with its properties and behaviors.
    # Changed habit_type to periodicity for consistency
    def __init__(self, name, periodicity, streak=0, last_completed=None):
        """
        Initializes a new Habit instance.

        Args:
            name (str): The name of the habit.
            periodicity (str): The frequency of the habit ('daily', 'weekly').
            streak (int, optional): The current streak count. Defaults to 0.
            last_completed (datetime, optional): The last date the habit was completed. Defaults to None.
        """
        self.name = name
        # Use periodicity consistently
        self.periodicity = periodicity
        self.current_streak = streak # Renamed for clarity
        self.last_completed_date = last_completed # Renamed for clarity

        # Define XP values directly within the class
        self.xp_values = {
            'daily': 10,
            'weekly': 30 # Example: weekly gives more XP
        }


    def mark_complete(self, completed_at=None):
        """
        Marks the habit as completed, updates the streak based on validation,
        and returns the XP gained.

        Args:
            completed_at (datetime, optional): The timestamp when the habit was completed.
                                             Defaults to datetime.now().

        Returns:
            tuple: (bool, str, int) indicating (was_completed, message, xp_gained)
                   - was_completed: True if the habit could be marked complete for the period, False otherwise.
                   - message: A status message.
                   - xp_gained: XP awarded (0 if not completed).
        """
        if completed_at is None:
            completed_at = datetime.now()

        # Normalize completed_at to date for comparisons
        completed_date = completed_at.date()

        # Prevent marking complete multiple times in the same period
        if self.last_completed_date:
            last_completed_date_only = self.last_completed_date.date()
            if self.periodicity == 'daily' and completed_date == last_completed_date_only:
                return False, "Already completed today.", 0
            if self.periodicity == 'weekly':
                 # Check if it's the same week (assuming week starts on Monday)
                 start_of_last_week = last_completed_date_only - timedelta(days=last_completed_date_only.weekday())
                 start_of_current_week = completed_date - timedelta(days=completed_date.weekday())
                 if start_of_current_week == start_of_last_week:
                     return False, "Already completed this week.", 0

        # Validate and update streak *before* setting last_completed
        if self.last_completed_date:
            if self.is_streak_valid(completed_at):
                self.current_streak += 1
                message = f"Streak continued! Current streak: {self.current_streak}."
            else:
                self.current_streak = 1 # Reset streak to 1 if broken
                message = "Streak broken. New streak started!"
        else:
            self.current_streak = 1 # First time completing
            message = "First completion! Streak started."

        self.last_completed_date = completed_at
        xp_gained = self.calculate_xp()
        return True, message, xp_gained


    def is_streak_valid(self, completed_at):
        """
        Checks if completing the habit now continues the current streak.

        Args:
            completed_at (datetime): The timestamp when the habit is being completed.

        Returns:
            bool: True if the streak is continued, False otherwise.
        """
        if not self.last_completed_date:
            return False # Cannot continue a streak if never completed

        last_completed_date_only = self.last_completed_date.date()
        completed_date_only = completed_at.date()

        if self.periodicity == 'daily':
            # Valid if completed on the very next day
            return (completed_date_only - last_completed_date_only).days == 1
        elif self.periodicity == 'weekly':
            # Valid if completed within the week following the last completion week
            days_since_last = (completed_date_only - last_completed_date_only).days
            # Must be completed between 1 and 14 days after the last one,
            # AND must fall into the next calendar week.
            # (e.g., last Mon, this Sun is valid; last Sun, this Mon is valid)
            last_completion_week_start = last_completed_date_only - timedelta(days=last_completed_date_only.weekday())
            current_completion_week_start = completed_date_only - timedelta(days=completed_date_only.weekday())
            # Check if it's exactly one week apart
            return current_completion_week_start == last_completion_week_start + timedelta(weeks=1)
            # Simpler check: return 1 <= days_since_last <= 14 # Allows skipping a week but maintaining streak if done within 7 days of *next* period start
        # Add monthly logic if needed later
        return False

    # Removed static xp_values dict

    def calculate_xp(self):
        """
        Calculates the experience points earned for completing the habit.
        Applies a bonus for longer streaks.

        Returns:
            int: The XP value based on the habit periodicity and streak length.
        """
        base_xp = self.xp_values.get(self.periodicity, 0)
        # Add a small streak bonus (e.g., +1 XP for every 5 streak days/weeks)
        streak_bonus = self.current_streak // 5
        return base_xp + streak_bonus

    def to_dict(self):
        """Converts the Habit object to a dictionary for JSON serialization."""
        return {
            'name': self.name,
            'periodicity': self.periodicity, # Use periodicity
            'streak': self.current_streak,
            'last_completed': self.last_completed_date.strftime('%Y-%m-%d %H:%M:%S') if self.last_completed_date else None
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Habit object from a dictionary (e.g., loaded from JSON)."""
        last_completed = None
        if data.get('last_completed'):
            try:
                # Try parsing with time first
                last_completed = datetime.strptime(data['last_completed'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                 # Fallback to parsing date only if time is missing (for backward compatibility)
                 try:
                     last_completed = datetime.strptime(data['last_completed'], '%Y-%m-%d')
                 except ValueError:
                     print(f"Warning: Could not parse last_completed date '{data['last_completed']}' for habit '{data.get('name')}'. Setting to None.")
                     last_completed = None # Or handle error differently

        # Handle potential missing keys or old format ('habit_type')
        periodicity = data.get('periodicity') or data.get('habit_type', 'daily') # Default to daily if missing

        return cls(
            name=data.get('name', 'Unnamed Habit'),
            periodicity=periodicity,
            streak=data.get('streak', 0),
            last_completed=last_completed
        )