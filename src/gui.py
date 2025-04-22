import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from habit_tracker import HabitTracker
from habit import Habit
import os

class HabitTrackerGUI:
    def __init__(self, root):
        self.tracker = HabitTracker()
        # Construct the path to the JSON file relative to this script's directory
        script_dir = os.path.dirname(__file__) 
        self.json_path = os.path.join(script_dir, 'habits_dataset.json')
        self.tracker.load_from_json(self.json_path)

        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("600x400") # Adjusted size

        # --- Main Frame ---
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Habit List ---
        list_frame = ttk.LabelFrame(main_frame, text="Habits")
        list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.habit_listbox = tk.Listbox(list_frame, height=10)
        self.habit_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.habit_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.habit_listbox.config(yscrollcommand=scrollbar.set)

        self.refresh_habit_list() # Populate the list initially

        # --- Buttons ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        add_button = ttk.Button(button_frame, text="Add Habit", command=self.add_habit_gui)
        add_button.pack(side=tk.LEFT, padx=5)

        mark_button = ttk.Button(button_frame, text="Mark Complete", command=self.mark_complete_gui)
        mark_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(button_frame, text="Delete Habit", command=self.delete_habit_gui)
        delete_button.pack(side=tk.LEFT, padx=5)

        stats_button = ttk.Button(button_frame, text="View Stats", command=self.view_stats_gui)
        stats_button.pack(side=tk.LEFT, padx=5)

        # --- Status Bar ---
        self.status_bar = ttk.Label(root, text="Level: 1 | XP: 0/100", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_status_bar() # Update initially

        # --- Save on Close ---
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


    def refresh_habit_list(self):
        self.habit_listbox.delete(0, tk.END) # Clear existing items
        habits = self.tracker.get_all_habits()
        if not habits:
            self.habit_listbox.insert(tk.END, "No habits yet. Add one!")
        else:
            for habit in habits:
                 # Display format: Name (Periodicity) - Streak: X
                 display_text = f"{habit.name} ({habit.periodicity}) - Streak: {habit.current_streak}"
                 self.habit_listbox.insert(tk.END, display_text)


    def update_status_bar(self):
         level, current_exp, exp_needed = self.tracker.get_level_and_exp()
         self.status_bar.config(text=f"Level: {level} | XP: {current_exp}/{exp_needed}")


    def add_habit_gui(self):
        # Simple dialog for now, could be a custom window later
        name = simpledialog.askstring("Add Habit", "Enter habit name:")
        if not name:
            return

        periodicity = simpledialog.askstring("Add Habit", "Enter periodicity (daily/weekly):",
                                             initialvalue="daily")
        if periodicity not in ["daily", "weekly"]:
             messagebox.showerror("Error", "Invalid periodicity. Use 'daily' or 'weekly'.")
             return

        if name and periodicity:
            self.tracker.add_habit(name, periodicity)
            self.refresh_habit_list()
            self.update_status_bar() # XP might change if level up happens indirectly? (Review logic)
            messagebox.showinfo("Success", f"Habit '{name}' added.")


    def mark_complete_gui(self):
        selected_index = self.habit_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select a habit to mark complete.")
            return

        # Extract habit name from the listbox text
        selected_text = self.habit_listbox.get(selected_index[0])
        habit_name = selected_text.split(" (")[0] # Get the part before " ("

        habit = self.tracker.get_habit_by_name(habit_name)
        if habit:
            completed, message = self.tracker.mark_habit(habit_name)
            if completed:
                self.refresh_habit_list()
                self.update_status_bar()
                messagebox.showinfo("Habit Marked", message)
            else:
                messagebox.showinfo("Habit Not Marked", message) # Show reason if not completed (e.g., already done)
        else:
             messagebox.showerror("Error", f"Could not find habit '{habit_name}' internally.")


    def delete_habit_gui(self):
        selected_index = self.habit_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select a habit to delete.")
            return

        selected_text = self.habit_listbox.get(selected_index[0])
        habit_name = selected_text.split(" (")[0]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the habit '{habit_name}'?"):
            if self.tracker.delete_habit(habit_name):
                self.refresh_habit_list()
                self.update_status_bar() # In case deletion affects something? Unlikely but good practice.
                messagebox.showinfo("Success", f"Habit '{habit_name}' deleted.")
            else:
                 messagebox.showerror("Error", f"Could not delete habit '{habit_name}'.")


    def view_stats_gui(self):
        # Simple stats display for now
        stats_text = self.tracker.view_statistics() # Get stats string from tracker
        level, current_exp, exp_needed = self.tracker.get_level_and_exp()
        # Added the missing closing quote to the f-string
        full_stats = f"Current Level: {level}\r\nCurrent XP: {current_exp}/{exp_needed}\r\n\r\n{stats_text}"
        messagebox.showinfo("Statistics", full_stats)


    def on_closing(self):
        # Save data before closing
        if messagebox.askokcancel("Quit", "Do you want to save changes and quit?"):
            self.tracker.save_to_json(self.json_path)
            self.root.destroy()

# This part is usually in main.py, but for simplicity now:
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = HabitTrackerGUI(root)
#     root.mainloop()
