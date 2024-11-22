import json
from datetime import datetime


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
        self.last_completed = completed_at
        self.streak += 1

    XP_VALUES = {
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
        return self.XP_VALUES.get(self.habit_type, 0)


class HabitTracker:
    # Manages a collection of habits, tracks experience points, and rewards.
    REWARD_COSTS = {
        'easy': 50,
        'medium': 100,
        'hard': 150
    }

    def __init__(self):
        """
        Initializes the HabitTracker instance with default values.
        Loads data from JSON file at initialization.
        """
        self.habits = []
        self.total_xp = 0
        self.rewards = []
        self.level = 1
        self.current_hp = 10  # Starting HP
        self.coins = 0
        self.exp_needed = 100  # Example starting experience needed to level up

        self.load_from_json()  # Load data at initialization

    def get_default_data(self):
        """
        Provides default data for the habit tracker.

        Returns:
            dict: A dictionary containing default values for the tracker.
        """
        return {
            'habits': [],
            'total_xp': 0,
            'rewards': [],
            'level': 1,
            'current_hp': 10,
            'coins': 0,
            'exp_needed': 100
        }

    def load_data(self, filename):
        """
        Loads data from a JSON file.

        Args:
            filename (str): The name of the JSON file to load data from.

        Returns:
            dict: The data loaded from the file, or default data if the file doesn't exist or is invalid.
        """
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"{filename} not found or has invalid JSON. Starting with default settings.")
            return self.get_default_data()

    def save_data(self, data, filename):
        """
        Saves data to a JSON file.

        Args:
            data (dict): The data to save.
            filename (str): The name of the file to save the data to.
        """
        with open(filename, 'w') as file:
            json.dump(data, file)

    def load_from_json(self):
        """
        Loads habit tracker data from a JSON file and initializes the tracker state.
        """

        data = self.load_data('habits.json')
        if data:
            self.total_xp = data['total_xp']
            self.rewards = data['rewards']
            self.level = data['level']
            self.current_hp = data['current_hp']
            self.coins = data['coins']
            self.exp_needed = data['exp_needed']
            self.habits = [
                Habit(
                    habit_data['name'],
                    habit_data['habit_type'],
                    habit_data['streak'],
                    datetime.strptime(habit_data['last_completed'], '%Y-%m-%d') if habit_data[
                        'last_completed'] else None
                )
                for habit_data in data['habits']
            ]

    def save_to_json(self):
        """
        Saves the current state of the habit tracker to a JSON file.
        """
        data_to_save = {
            'habits': [
                {
                    'name': habit.name,
                    'habit_type': habit.habit_type,
                    'streak': habit.streak,
                    'last_completed': habit.last_completed.strftime('%Y-%m-%d') if habit.last_completed else None
                }
                for habit in self.habits
            ],
            'total_xp': self.total_xp,
            'rewards': self.rewards,
            'level': self.level,
            'current_hp': self.current_hp,
            'coins': self.coins,
            'exp_needed': self.exp_needed
        }
        self.save_data(data_to_save, 'habits.json')

    def add_habit(self, name, habit_type):
        """
        Adds a new habit to the tracker if it does not already exist.

        Args:
            name (str): The name of the habit.
            habit_type (str): The type of the habit.

        Returns:
            None
        """
        if any(habit.name == name for habit in self.habits):
            print("Error: A habit with that name already exists.")
            return

        new_habit = Habit(name, habit_type)
        self.habits.append(new_habit)
        self.save_to_json()
        print("Habit created successfully!")  # Move the success message here

    def delete_habit(self, name):
        """
        Deletes a habit by its name after user confirmation.

        Args:
            name (str): The name of the habit to delete.

        Returns:
            None
        """
        confirm = input(f"Are you sure you want to delete the habit '{name}'? (yes/no): ").strip().lower()
        if confirm == 'yes':
            self.habits = [habit for habit in self.habits if habit.name != name]
            self.save_to_json()
            print(f"Habit '{name}' deleted successfully!")
        else:
            print("Habit deletion canceled.")

    def mark_habit(self, name):
        """
        Marks a specified habit as complete, updates XP and coin counts, and checks for level up.

        Args:
            name (str): The name of the habit to mark as complete.

        Returns:
            None
        """
        now = datetime.now()  # Store now once
        for habit in self.habits:
            if habit.name == name:
                habit.mark_complete(now)
                xp_gained = habit.calculate_xp()
                self.total_xp += xp_gained
                self.coins += 10  # Example coin gain
                print(f'You gained {xp_gained} XP and 10 coins!')
                self.check_level_up()
                break
        else:
            print("Habit not found!")
        self.save_to_json()

    def check_level_up(self):
        """
        Checks if the tracker has enough XP to level up. If so, increments the level and updates HP and XP needed.

        Returns:
            None
        """
        if self.total_xp >= self.exp_needed:
            self.level += 1
            self.total_xp = 0  # Reset XP
            self.current_hp += 5  # Increase HP on level up
            self.exp_needed += 50  # Increase XP needed for next level
            print(f'Congratulations! You leveled up to Level {self.level}. Your HP is now {self.current_hp}!')

    def view_statistics(self):
        """
        Displays the statistics of the habits, including total XP, level, longest streak, average streak length, and success rate.

        Returns:
            None
        """
        print("\n--- Statistics ---")
        if not self.habits:
            print("No habits to show statistics for.")
            return

        longest_streak = 0
        total_streak = 0
        completed_count = 0

        for habit in self.habits:
            total_streak += habit.streak
            longest_streak = max(longest_streak, habit.streak)
            if habit.last_completed:
                completed_count += 1

        average_streak_length = total_streak / len(self.habits) if self.habits else 0
        success_rate = (completed_count / len(self.habits)) * 100 if self.habits else 0

        print(f"Total XP: {self.total_xp} / {self.exp_needed} needed for next level")
        print(f"Level: {self.level}")
        print(f"Longest Streak: {longest_streak}")
        print(f"Average Streak Length: {average_streak_length:.2f}")
        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Current HP: {self.current_hp}")
        print(f"Coins: {self.coins}")
        print("------------------")

    def create_reward(self, name, difficulty):
        """
        Creates a new reward if it does not already exist.

        Args:
            name (str): The name of the reward.
            difficulty (str): The difficulty level of the reward.

        Returns:
            None
        """
        if any(reward['name'] == name for reward in self.rewards):
            print("Error: A reward with that name already exists.")
            return

        reward = {
            'name': name,
            'difficulty': difficulty,
            'last_exchanged': None  # Initialize the last exchanged time as None
        }
        self.rewards.append(reward)
        self.save_to_json()

    def delete_reward(self, name):
        self.rewards = [reward for reward in self.rewards if reward['name'] != name]
        self.save_to_json()

    def exchange_reward(self, name):
        """
        Exchanges a reward if enough coins are available.

        Args:
            name (str): The name of the reward to exchange.

        Returns:
            None
        """
        for reward in self.rewards:
            if reward['name'] == name:
                cost = self.REWARD_COSTS.get(reward['difficulty'], 0)
                if self.total_xp >= cost:
                    self.total_xp -= cost
                    reward['last_exchanged'] = datetime.now().strftime(
                        '%Y-%m-%d %H:%M:%S')  # Update the last exchanged time
                    print(f'You exchanged {cost} XP for {name}!')
                else:
                    print("Not enough XP to exchange for this reward.")
                break
        else:
            print("Reward not found!")
        self.save_to_json()

    def view_rewards(self):
        """
        Displays the list of rewards to the user.

        Returns:
            None
        """
        if not self.rewards:
            print("No rewards available.")
            return

        print("--- Your Rewards ---")
        for reward in self.rewards:
            last_exchanged = reward['last_exchanged'] if reward['last_exchanged'] else "Never"
            print(f"Reward: {reward['name']}, Difficulty: {reward['difficulty']}, Last Exchanged: {last_exchanged}")

    def show_menu(self):
        """
        Displays the main menu and handles user choices.

        Returns:
            None
        """
        while True:
            print("\n--- Habit Tracker Menu ---")
            print("1. Habits Management")
            print("2. Statistics")
            print("3. Rewards")
            print("4. Exit")

            choice = input(
                "Choose an option number or type 'Habits', 'Statistics', 'Rewards', or 'Exit' directly: ").strip().lower()

            # Determine the user's choice
            if choice == '1' or choice == 'habits':
                self.habits_management()
            elif choice == '2' or choice == 'statistics':
                self.view_statistics()
            elif choice == '3' or choice == 'rewards':
                self.rewards_management()
            elif choice == '4' or choice == 'exit':
                print("Goodbye!")
                break
            else:
                print("Invalid option, please try again.")

    def habits_management(self):
        """
        Manages user habits, allowing creation, deletion, marking, and viewing habits.

        Returns:
            None
        """
        while True:
            print("\n--- Habits Management ---")
            print("1. Create Habit")
            print("2. Delete Habit")
            print("3. Mark Habit as completed")
            print("4. View Habits")
            print("5. Back to Main Menu")

            choice = input(
                "Choose an option from 1-5 or type 'Create', 'Delete', 'Mark', 'View', or 'Back' directly.: ").strip().lower()

            # Determine the user's choice
            if choice == '1' or choice == 'create':
                name = input("Enter habit name: ")
                habit_type = self.select_habit_type()  # Use a separate method to select habit type
                self.add_habit(name, habit_type)
            elif choice == '2' or choice == 'delete':
                name = input("Enter habit name to delete: ")
                self.delete_habit(name)
                print("Habit deleted successfully!")
            elif choice == '3' or choice == 'mark':
                name = input("Enter habit name to mark as complete: ")
                self.mark_habit(name)
            elif choice == '4' or choice == 'view':
                self.view_habits()  # New method to view habits
            elif choice == '5' or choice == 'back':
                break
            else:
                print("Invalid option, please try again.")

    def select_habit_type(self):
        """
        Allows the user to select the type of habit (daily, weekly, or monthly).

        Returns:
            str: The selected habit type.
        """
        print("Select habit type:")
        print("1. Daily")
        print("2. Weekly")
        print("3. Monthly")
        choice = input("Choose an option (1-3): ")
        if choice == '1':
            return 'daily'
        elif choice == '2':
            return 'weekly'
        elif choice == '3':
            return 'monthly'
        else:
            print("Invalid option, defaulting to daily.")
            return 'daily'

    def view_habits(self):
        """
        Displays the list of habits to the user.

        Returns:
            None
        """
        if not self.habits:
            print("No habits available.")
            return

        print("--- Your Habits ---")
        for habit in self.habits:
            last_completed_str = habit.last_completed.strftime(
                '%Y-%m-%d') if habit.last_completed else "Not completed yet"
            print(
                f"Habit: {habit.name}, Type: {habit.habit_type}, Streak: {habit.streak}, Last Completed: {last_completed_str}")
        print("------------------")

    def rewards_management(self):
        """
         Manages user rewards, allowing creation, deletion, exchange, and viewing rewards.

         Returns:
             None
         """
        while True:
            print("\n--- Rewards Management ---")
            print("1. Create Reward")
            print("2. Delete Reward")
            print("3. Exchange Reward")
            print("4. View Rewards")
            print("5. Back to Main Menu")

            choice = input(
                "Choose an option from 1-5 or type 'Create', 'Delete', 'Exchange', 'View', or 'Back' directly.: ").strip().lower()

            # Determine the user's choice
            if choice == '1' or choice == 'create':
                name = input("Enter reward name: ")
                difficulty = input("Enter reward difficulty (easy, medium, hard): ").strip().lower()
                if difficulty in self.REWARD_COSTS:
                    self.create_reward(name, difficulty)
                    print("Reward created successfully!")
                else:
                    print("Invalid difficulty level. Please try again.")
            elif choice == '2' or choice == 'delete':
                name = input("Enter reward name to delete: ")
                self.delete_reward(name)
                print("Reward deleted successfully!")
            elif choice == '3' or choice == 'exchange':
                name = input("Enter reward name to exchange: ")
                self.exchange_reward(name)
            elif choice == '4' or choice == 'view':
                self.view_rewards()
            elif choice == '5' or choice == 'back':
                break
            else:
                print("Invalid option, please try again.")

# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    # Create an instance of the HabitTracker class, initializing the habit tracking system
    habit_tracker = HabitTracker()

    # Load existing data from a JSON file to restore previous habits and rewards
    habit_tracker.load_from_json()

    # Display the main menu, allowing the user to interact with the habit tracker
    habit_tracker.show_menu()