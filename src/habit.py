from datetime import datetime, timedelta


class Habit:
    # Represents a single habit with its properties and behaviors.
    def __init__(self, name, habit_type, streak=0, last_completed=None):
        """
        Initializes a new Habit instance.

        Args:
            name (str): The name of the habit.
            habit_type (str): The type of the habit ('daily', 'weekly', 'monthly').
            streak (int, optional): The current streak count. Defaults to 0.
            last_completed (datetime, optional): The last date the habit was completed. Defaults to None.
        """
        self.name = name
        self.habit_type = habit_type
        self.streak = streak
        self.last_completed = last_completed

    def mark_complete(self, completed_at):
        """
        Marks the habit as completed and updates the streak.

        Args:
            completed_at (datetime): The timestamp when the habit was completed.
        """
        if self.last_completed:
            # Check if the streak is valid based on the habit type
            if not self.is_streak_valid(completed_at):
                self.streak = 1  # Reset streak if the periodicity is broken
        else:
            self.streak = 1  # First time completing the habit

        self.last_completed = completed_at
        self.streak += 1  # Increment streak

    def is_streak_valid(self, completed_at):
        """
        Checks if the streak is still valid based on the habit's periodicity.

        Args:
            completed_at (datetime): The timestamp when the habit was completed.

        Returns:
            bool: True if the streak is valid, False if it's broken.
        """
        if self.habit_type == 'daily':
            return (completed_at - self.last_completed).days == 1
        elif self.habit_type == 'weekly':
            return (completed_at - self.last_completed).days <= 7
        elif self.habit_type == 'monthly':
            return completed_at.month == self.last_completed.month and completed_at.year == self.last_completed.year
        return False

    xp_values = {
        'daily': 10,
        'weekly': 20,
        'monthly': 30
    }

    def calculate_xp(self):
        """
        Calculates the experience points earned for completing the habit.

        Returns:
            int: The XP value based on the habit type.
        """
        return self.xp_values.get(self.habit_type, 0)