# Habit Tracker

A simple and comprehensive habit tracker application to help users monitor their habits, track streaks, earn rewards, and improve their productivity.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Modules and Functionality](#modules-and-functionality)
- [Unit Testing](#unit-testing)
- [License](#license)

## Introduction

The Habit Tracker application is designed to help you build and maintain positive habits by allowing you to:

- Create and manage daily or weekly habits.
- Track habit completion and streaks.
- View analytics related to your habits.
- Earn rewards as you progress and level up.

This project uses Python and stores user data in a JSON file. It's lightweight and can be run from your local machine with no additional dependencies.

## Installation

To install the project, follow these steps:

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/pablogonz12/Habit-Tracker.git
    cd habit-tracker
    ```
2. Set up a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    ```
3. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

**Dependencies:**
No external dependencies are needed

**Structure:**

Ensure your project directory has the following structure:
```
habit_tracker_project/
├── src/
│   ├── habit.py
│   └── habit_tracker.py
│   └── main.py
│   └── habits_dataset.json  <-- Rename this to habits.json for testing purposes
├── tests/
│   └── test_habits.py
├── README.md
```

**Prepare the dataset (optional):**

The app expects a `habits.json` file to store habit data. For testing purposes, an extensive dataset has been provided. Simply rename `habits_dataset.json` (provided in the repository) to `habits.json` to use this dataset. If you value your existing data on this program, please make sure to back up your existing `habits.json` file before renaming the dataset for testing purposes.

## Running the Application

To run the app:

1. Navigate to the `src/` directory:
    ```bash
    cd src/
    ```
2. Run the main application:
    ```bash
    python main.py
    ```
This will start the program and you can interact with the habit tracker in your terminal or command line interface.

## Modules and Functionality

#### 1. `habit.py`

The `Habit` class encapsulates the properties and behaviors of a single habit, providing functionality for tracking its progress, managing streaks, and calculating experience points (XP). This class is a cornerstone of the habit-tracking system, ensuring that each habit operates independently and adheres to its designated type.

---

##### Key Features

1. **Initialization**
    
    - **Attributes**:
        
        - `name` (str): The name of the habit.
        - `habit_type` (str): Specifies the type of habit (`daily`, `weekly`, `monthly`).
        - `streak` (int): Tracks the current streak of consecutive completions. Defaults to 0.
        - `last_completed` (datetime): Stores the date and time when the habit was last completed. Defaults to `None`.
        
    - **Constructor**:
        
        - The `__init__` method initializes a habit with its name, type, streak, and last completion date.
        
1. **Marking a Habit as Complete**
    
    - **Method**: `mark_complete(completed_at)`
        - Updates the habit's `last_completed` timestamp and increments its streak.
        - **Behaviour**:
            - If the habit has never been completed (`last_completed` is `None`), the streak starts at 1.
            - If a completion breaks the periodicity (e.g., missing a day for a `daily` habit), the streak resets to 1.
            - Otherwise, the streak increments by 1 upon valid completion.
            
1. **Streak Validation**
    
    - **Method**: `is_streak_valid(completed_at)`
        - Ensures that the current streak remains valid based on the habit type and completion frequency.
        
        - **Validation Rules**:
            - `daily`: The habit must be completed exactly one day after the last completion.
            - `weekly`: The habit must be completed within 7 days of the last completion.
            - `monthly`: The completion must fall within the same month and year as the last completion.
        
1. **Experience Points Calculation**
    
    - **Method**: `calculate_xp()`
        - Determines the XP awarded for completing the habit, based on its type.
        - **XP Values**:
            - `daily`: 10 XP
            - `weekly`: 20 XP
            - `monthly`: 30 XP
            - Defaults to 0 XP for undefined habit types.

#### 2. `habit_tracker.py`

The `habit_tracker.py` module provides tools for managing and tracking the progress of habits, including calculating streaks, experience points (XP), rewards, and overall performance. It serves as the core functionality for maintaining user engagement and habit-building by offering the following key features:

##### Key Features

1. **Habit Management**
    
    - Allows adding, deleting, and updating habits with relevant attributes like streaks and completion status.
    - Supports categorizing habits based on difficulty levels (`easy`, `medium`, `hard`).
    
1. **Streak Tracking**
    
    - **`calculate_streak(habit_name)`**: Dynamically calculates the current streak for a given habit by analyzing the completion dates. Streaks encourage consistency by rewarding users for maintaining their habits.
    
1. **Experience Points and Leveling System**
    
    - Tracks user XP and provides progression through levels.
    - XP is gained by completing habits, with more challenging habits yielding greater rewards.
    - **`check_level_up()`**: Automatically checks if the user’s XP has reached the threshold to level up, providing bonuses like increased HP.
    
1. **Reward System**
    
    - Users can create rewards and exchange earned XP for these rewards.
    - **Reward Cost Scaling**: Rewards are categorized by difficulty, with costs (`easy`, `medium`, `hard`) scaled for balance.
    
1. **Analytics and Reporting**
    
    - **`view_statistics()`**: Displays critical metrics like total XP, longest streak, average streak length, and habit success rate. These insights help users identify strengths and areas for improvement.
    - **`generate_report()`**: Produces a comprehensive report summarizing habit performance, streaks, XP, and rewards.
    
1. **Persistent Data Management**
    
    - Automatically saves and loads user data (habits, XP, rewards, etc.) via JSON files.
    - **`load_from_json()`** and **`save_to_json()`** ensure users can pick up where they left off without losing progress.
    
1. **Interactive User Interface**
    
    - A menu-driven system enables easy navigation through various functionalities, such as habit management, statistics, and rewards.

---

##### Example Workflow

1. **Adding a Habit**:  
    Users can create a new habit by specifying its name and type (e.g., `daily`, `weekly`). The system ensures no duplicate habits exist.
    
2. **Tracking Progress**:  
    After completing a habit, users mark it as done. This updates the habit’s last completed date, increases its streak, and awards XP and coins.
    
3. **Leveling Up**:  
    Once sufficient XP is earned, users level up, unlocking new challenges and bonuses like additional HP.
    
4. **Claiming Rewards**:  
    Users can exchange XP for rewards such as relaxation time or special treats, incentivizing consistent progress.
    
5. **Monitoring Progress**:  
    Users access detailed statistics and reports to visualize their performance, motivating them to maintain their habits and improve.

**Analytics Methods:**

- `calculate_streak(habit_name)`: Calculates the streak of a given habit.
- `generate_report()`: Generates a report showing streaks, habit completion, and rewards.

#### 3. `main.py`

The main entry point to the application. It loads the habits from `habits.json`, provides an interface for interacting with the habits, and displays analytics.

---
##### Key Features

1. **Module Imports**
    
    - **`json`**: Facilitates reading and writing data to and from JSON files, allowing for persistent habit tracking.
    - **`datetime`**: Handles date and time operations, such as tracking when habits are completed.
    - **`Habit`** and **`HabitTracker`**: Imported from separate modules, they define the structure and functionality of individual habits and the overall tracking system.
2. **Main Script Execution**
    
    - The script includes a conditional block to ensure it runs only when executed directly (not imported as a module):

```python
`if __name__ == "__main__":`
```

3. **Habit Tracking System Initialization**
    
    - **Instance Creation**:
        - An instance of the `HabitTracker` class is created to manage all habits and their associated behaviors.

```python
`habit_tracker = HabitTracker()`
```

4. **Data Restoration**
    
    - **Method**: `habit_tracker.load_from_json()`
        - Loads previously saved habits and their states from a JSON file, ensuring continuity across sessions.
5. **User Interaction**
    
    - **Method**: `habit_tracker.show_menu()`
        - Displays an interactive menu that allows users to perform actions like:
            - Adding new habits.
            - Marking habits as complete.
            - Viewing progress and streaks.
            - Saving data to the JSON file.



## Unit Testing

The `test_habits.py` is a unit test for the `Habit` class, specifically testing its creation, modification, deletion, and streak calculation. Unit tests are used to verify that the methods and properties of a class behave as expected. The script uses the `unittest` framework to run automated tests on the `Habit` class to ensure it functions properly.

---
##### Key Features

1. **Module Imports**
    
    - **`sys`**: Allows manipulation of the Python runtime environment. It’s used here to add the path to the `src` directory so that the script can access modules from there.
    - **`os`**: Provides a way to interact with the operating system, especially useful for manipulating file paths.
    - **`unittest`**: Python's built-in testing framework for writing and running tests.
2. **Path Setup**
    
    - The following line adds the `src` directory to the system path, allowing the script to import the `Habit` class from `src/habit.py`:

```python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
```
 
3. **Test Class: `TestHabitTracker`**
    
    - The `TestHabitTracker` class extends `unittest.TestCase`, which provides the methods required to run unit tests. Each test method within this class will be executed independently to validate specific functionality.
4. **Test Setup: `setUp()`**
    
    - The `setUp()` method is automatically called before each individual test method. It prepares a fresh `Habit` instance, which can then be used in the subsequent tests.

```python
self.habit = Habit(name="Push Ups", habit_type="daily", streak=3, last_completed="2025-01-09")
```
---

##### Test Methods

1. **`test_create_habit()`**
    
    - Verifies that the `Habit` instance is correctly initialized.
        
        - Checks that the habit's name, type, streak, and last completion date match the expected values.

```python
self.assertEqual(self.habit.name, "Push Ups") self.assertEqual(self.habit.habit_type, "daily") self.assertEqual(self.habit.streak, 3) self.assertEqual(self.habit.last_completed, "2025-01-09")
```

2. **`test_edit_habit()`**
    
    - Tests modifying the attributes of the `Habit` instance.
        
        - Changes the habit's name to "Morning Run" and updates the streak to 5.
        - Confirms that the changes are successfully applied.

```python
self.habit.name = "Morning Run" self.habit.streak = 5 self.assertEqual(self.habit.name, "Morning Run") self.assertEqual(self.habit.streak, 5)
```

3. **`test_delete_habit()`**
    
    - Simulates the deletion of a habit.
        
        - Sets the `habit` instance to `None`, simulating its removal.
        - Verifies that the habit is no longer present (i.e., it is `None`).
        
4. **`test_streak_calculation()`**
    
    - Tests the streak calculation logic.
        
        - Checks that the initial streak is correctly set to 3.
        - Simulates the completion of the habit and increments the streak by 1.
        - Verifies that the streak is updated correctly.

```python
habit_name = self.habit.name self.habit = None # Simulate deletion self.assertIsNone(self.habit)
```


---

##### Running the Tests

To run the tests, simply execute the script in a Python environment:

```bash
`python test_habit_tracker.py`
```

When executed, `unittest.main()` will automatically discover and run all test methods in the script, outputting the results to the console.


## License

MIT License

Copyright (c) 2025 Pablo González Mínguez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.