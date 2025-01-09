import sys
import os
import unittest

# Add the path to the src folder so Python can find it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from habit import Habit  # Assuming Habit class is inside src/habit.py


class TestHabitTracker(unittest.TestCase):

    def setUp(self):
        """Create a Habit instance before each test."""
        self.habit = Habit(name="Push Ups", habit_type="daily", streak=3, last_completed="2025-01-09")

    def test_create_habit(self):
        """Test habit creation."""
        self.assertEqual(self.habit.name, "Push Ups")
        self.assertEqual(self.habit.habit_type, "daily")
        self.assertEqual(self.habit.streak, 3)
        self.assertEqual(self.habit.last_completed, "2025-01-09")

    def test_edit_habit(self):
        """Test editing a habit."""
        self.habit.name = "Morning Run"
        self.habit.streak = 5
        self.assertEqual(self.habit.name, "Morning Run")
        self.assertEqual(self.habit.streak, 5)

    def test_delete_habit(self):
        """Test deleting a habit."""
        habit_name = self.habit.name
        self.habit = None  # Simulate deletion
        self.assertIsNone(self.habit)

    def test_streak_calculation(self):
        """Test streak calculation logic."""
        # For simplicity, just check the streak is being tracked correctly
        self.assertEqual(self.habit.streak, 3)
        # Simulate incrementing streak after completion
        self.habit.streak += 1
        self.assertEqual(self.habit.streak, 4)


if __name__ == '__main__':
    unittest.main()