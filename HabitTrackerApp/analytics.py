from habits import Habits
import json
import os
from datetime import datetime, timezone

class Analytics(Habits):
    
    def __init__(self, habit_data: dict = None, habit_name: str = None):
        """This is the constructor for the Analytics class.

        Args:
            habit_data (dict, optional): Stores all JSON data from the JSON files and is
            imported from the Habits parent class. Defaults to None.
            habit_name (str, optional): Stores the name of a given habit that a user wishes
            to interact with and is imported from the Habits parent class. Defaults to None.
        """
        super().__init__(habit_data, habit_name)
        
        
    def show_all_habits(self):
        """This method displays the names of all habits stored within the
        "Habits" folder. The method loops through all JSON files and then
        loads the names of the habits from each file. The names are printed before
        the next name is temporarily stored in the "loaded_habit" variable.
        """
        
        # Checks whether the "Habits" directory exists and exits the method if it doesn't
        if not os.path.exists("Habits"):
            print("No \"Habits\" folder found. Please create a habit first or check the file path.")
            return None
        
        for file_in_folder in os.listdir("Habits"):
            if file_in_folder.endswith(".json") == True:
                path_of_file = os.path.join("Habits", file_in_folder)
                with open(path_of_file, mode="r", encoding="utf-8") as read_file:
                    loaded_habit = json.load(read_file)
                    print("- "+ loaded_habit.get("name", ""))
                    
    
    def get_longest_streak_single_habit(self):
        """This method calculates the longest streak of check-offs for a single habit.
        This is done by keeping counters for the current streak and the longest streak.
        The method checks the periodicity of the habit (daily or weekly) and calculates
        the streak accordingly after the entire check-off history has loaded and converted
        from ISO format to a datetime object. A loop is then used to iterate through
        the converted check-off history, checking the difference in days between each
        consecutive check-off. If the difference is 1 day (for daily habits) or 7 days
        (for weekly habits), the streak counter is incremented.
        
        Returns:
            longest_streak (int): The longest streak found for a given habit and its periodicity.
        """
        
        # Counters to keep track of the current and longest streaks
        streak_counter = 1
        longest_streak = 1
        
        # Loads the habit data from the JSON file. This method is inherited from the Habits class.
        self.habit_data = self.load_habit_file()

        # If no habit data was returned from the load_habit_file method, then end the method.
        # Due to the method already including a message for archived habits, no message is outputted here.
        if self.habit_data == None:
            return None
        
        # The check-off history and the periodicity of the habit are stored.
        unconverted_checkoffs = self.habit_data.get("check_off_history", [])
        checkoff_periodicity = self.habit_data.get("periodicity", "")
        
        # A loop runs to convert each entry in the check-off history from a string to a datetime object,
        # then appends these new values into a new list.
        converted_checkoffs = []
        for unconverted_datetime in unconverted_checkoffs:
            converted_datetime = datetime.fromisoformat(unconverted_datetime.replace("Z", "+00:00"))
            converted_checkoffs.append(converted_datetime)

        # A loop runs for each entry in the converted check-off history. The difference in days
        # between each consecutive check-off is calculated and stored a variable.
        for i in range(1, len(converted_checkoffs)):
            difference_in_days = (converted_checkoffs[i].date() - converted_checkoffs[i - 1].date()).days
            
            # If the difference between check-offs is 1 day (for daily habits) or 7 days (for weekly habits),
            # the streak counter is incremented. Otherwise, the streak counter is reset to 1.
            if (checkoff_periodicity == "daily") and (difference_in_days == 1):
                streak_counter += 1
            elif (checkoff_periodicity == "weekly") and (difference_in_days <= 7):
                streak_counter += 1
            else:
                streak_counter = 1
            
            # The longest streak is compared to the current streak counter and updated should the current streak
            # be greater than the longest streak.  
            longest_streak = max(longest_streak, streak_counter)
        
        # The longest streak is outputted to the user, with the value being divided by 7 if the periodicity is weekly.
        if checkoff_periodicity == "daily":
            print("The longest streak for the habit \"" + self.habit_name + "\" is " + str(longest_streak) + " days.")
            return longest_streak
            
        elif checkoff_periodicity == "weekly":
            longest_streak = int(longest_streak / 7)
            print("The longest streak for the habit \"" + self.habit_name + "\" is " + str(longest_streak) + " weeks.")
            return longest_streak
        
        else:
            print("Unforseen error occurred. Please check the periodicity of the habit.")
            return None
    

    def get_longest_streak_all_habits(self):
        """This method calculates the longest streak of check-offs for all habits
        stored in the "Habits" folder. The method loops through each JSON file in the
        folder, loading the habit data and calling the longest_streak_single_habit()
        method for each habit. At the end, the called method outputs the longest streak
        for each individual habit.
        """
        
        # Checks whether the "Habits" directory exists and exits the method if it doesn't.
        if not os.path.exists("Habits"):
            print("No \"Habits\" folder found. Please create a habit first or check the file path.")
            return None
        
        # Loops through each JSON file in the "Habits" folder, then sets
        # the name of the habit and the habit data before calling the
        # longest_streak_single_habit() method. Therefore, with each call
        # of the method, each individual habit's data is loaded and used.
        for file_in_folder in os.listdir("Habits"):
            if file_in_folder.endswith(".json"):
                path_of_file = os.path.join("Habits", file_in_folder)
                with open(path_of_file, mode="r", encoding="utf-8") as read_file:
                    loaded_habit = json.load(read_file)
                    self.habit_name = loaded_habit.get("name", "")
                    self.habit_data = loaded_habit
                    self.get_longest_streak_single_habit()


    def get_most_checkoff_history(self):
        """This method checks through all JSON files in the "Habits" folder and
        determines which habit has the most check-offs. The method keeps track of
        the maximum number of check-offs and the corresponding habit names. If multiple
        habits have the same maximum number of check-offs, all of them are printed.
        
        Returns:
            habit (list): Stores the names of all habits that have the most checkoff history.
        """
        
        # Checks whether the "Habits" directory exists and exits the method if it doesn't.
        if not os.path.exists("Habits"):
            print("No \"Habits\" folder found. Please create a habit first or check the file path.")
            return None
        
        # Counters to keep track of the maximum number of check-offs and the corresponding habit names.
        most_checkoffs = 0
        habits_with_most_checkoffs = []
        
        # A loop runs to check through all JSON files in the "Habits" folder.
        # The method checks whether the file ends with ".json" and then loads the data.
        for file_in_folder in os.listdir("Habits"):
            if file_in_folder.endswith(".json"):
                path_of_file = os.path.join("Habits", file_in_folder)
                with open(path_of_file, mode="r", encoding="utf-8") as read_file:
                    loaded_habit = json.load(read_file)

                    # The number of check-offs for the current habit is compared to the current
                    # holder of the habit with most values. If the current habit has more check-offs,
                    # the highest number of check-offs is updated and the habit name is stored.
                    if len(loaded_habit.get("check_off_history", [])) > most_checkoffs:
                        most_checkoffs = len(loaded_habit.get("check_off_history", []))
                        habits_with_most_checkoffs = [loaded_habit.get("name", "")]
                        
                    # If the current habit has the same number of check-offs as the maximum,
                    # the habit name is added to the list of habits with the most check-offs.
                    elif len(loaded_habit.get("check_off_history", [])) == most_checkoffs:
                        habits_with_most_checkoffs.append(loaded_habit.get("name", ""))
        
        # A loop runs to print the habit(s) with the most check-offs.
        if habits_with_most_checkoffs:
            print("The habit(s) with the most check-offs (" + str(most_checkoffs) + ") are:")
            for habit in habits_with_most_checkoffs:
                print("- " + habit)
                return habit
        return None
        

    def get_least_checkoff_history(self):
        """This method checks through all JSON files in the "Habits" folder and
        determines which habit has the least check-offs. The method keeps track of
        the minimum number of check-offs and the corresponding habit names. If multiple
        habits have the same minimum number of check-offs, all of them are printed.
        
        Returns:
            habit (list): Stores the names of all habits that have the least checkoff history.
        """
        
        # Checks whether the "Habits" directory exists and exits the method if it doesn't.
        if not os.path.exists("Habits"):
            print("No \"Habits\" folder found. Please create a habit first or check the file path.")
            return None
        
        # Counters to keep track of the minimum number of check-offs and the corresponding habit names.
        # It should be noted that the minimum number of check-offs is initially set to infinity so that
        # any initial value during the loop will be less than least_checkoffs.
        least_checkoffs = float("inf")
        habits_with_least_checkoffs = []
        
        # A loop runs to check through all JSON files in the "Habits" folder.
        # The method checks whether the file ends with ".json" and then loads the data.
        for file_in_folder in os.listdir("Habits"):
            if file_in_folder.endswith(".json") == True:
                path_of_file = os.path.join("Habits", file_in_folder)
                with open(path_of_file, mode="r", encoding="utf-8") as read_file:
                    loaded_habit = json.load(read_file)

                    # The number of check-offs for the current habit is compared to the current
                    # holder of the habit with least values. If the current habit has less check-offs,
                    # the lowest number of check-offs is updated and the habit name is stored.
                    if len(loaded_habit.get("check_off_history", [])) < least_checkoffs:
                        least_checkoffs = len(loaded_habit.get("check_off_history", []))
                        habits_with_least_checkoffs = [loaded_habit.get("name", "")]
                        
                    # If the current habit has the same number of check-offs as the minimum,
                    # the habit name is added to the list of habits with the least check-offs.
                    elif len(loaded_habit.get("check_off_history", [])) == least_checkoffs:
                        habits_with_least_checkoffs.append(loaded_habit.get("name", ""))
        
        # A loop runs to print the habit(s) with the least check-offs.
        if habits_with_least_checkoffs:
            print("The habit(s) with the least check-offs (" + str(least_checkoffs) + ") are:")
            for habit in habits_with_least_checkoffs:
                print("- " + habit)
                return habit
        return None

    
    def get_habits_with_same_periodicity(self, wanted_periodicity: str = "daily"):
        """This method checks through the contents of all JSON files in the "Habits" folder
        and determines which habits have the same periodicity as the one specified by the user.
        If a match is found, the habit name is added to a list.

        Args:
            wanted_periodicity (str, optional): This is the periodicity to search
            for that is specified by the user. Defaults to "daily".
        """
        
        # Checks whether the "Habits" directory exists and exits the method if it doesn't.
        if not os.path.exists("Habits"):
            print("No \"Habits\" folder found. Please create a habit first or check the file path.")
            return None
        
        # Used to store all habits with the same periodicity as the one specified by the user.
        all_periodicities = []
        
        # Loops through each JSON file in the "Habits" folder, then checks whether the file ends with ".json".
        # If it does, the file is opened and the periodicity of the habit is checked.
        # If the periodicity matches the one specified by the user, the habit name is added to the list.
        for file_in_folder in os.listdir("Habits"):
            if file_in_folder.endswith(".json"):
                path_of_file = os.path.join("Habits", file_in_folder)
                with open(path_of_file, mode="r", encoding="utf-8") as read_file:
                    loaded_habit = json.load(read_file)
                    periodicity = loaded_habit.get("periodicity", "")
                    
                    if wanted_periodicity == periodicity:
                        all_periodicities.append(loaded_habit.get("name", "")) 

        if all_periodicities:
            print("The following habits have the periodicity of \"" + wanted_periodicity + "\":")
            for habit in all_periodicities:
                print("- " + habit)
                
        else:
            print("No habits were found with that periodicity. Please create a new habit with that periodicity.")
            return None
        
       
    def get_history_of_checkoffs_time_range(self):
        """This method gets the history of check-offs for a specific habit within
        a specified range of dates. The habit is loaded from the JSON file and the user
        is then prompted to enter a start and end date. The method checks if the dates
        are in the correct format (YYYY-MM-DD) and converts them to datetime objects.
        Afterwards, the method filters the check-off history based on the specified date range
        and outputs the filtered check-off history to the user after being sanitised for
        readability.
        """
        
        # Loads the habit data from the JSON file. This method is inherited from the Habits class.
        self.habit_data = self.load_habit_file()
        
        # A loop is made that prompts the user for a start and end date, then checks if they are valid. If they are,
        # the dates are then converted to datetime objects with the UTC timezone and formatted. The loop
        # is then exited. If the dates are not valid, a ValueError is raised and the user is informed
        # that they have entered an incorrect date format. The loop continues until valid dates are entered.

        while True:
            start_date = input("Enter start date (YYYY-MM-DD): ")
            
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                
                end_date = input("Enter end date (YYYY-MM-DD): ")
                end_date = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                break
            
            except ValueError:
                print("You have entered an incorrect date format. Please use YYYY-MM-DD.")
            
        # Retrieves the check-off history from the habit data formats it into datetime objects,
        # then filters the check-offs based on the specified date range. The accepted dates are then
        # appended to a new list called "filtered_checkoffs".
        filtered_checkoffs = []
        for checkoff in self.habit_data.get("check_off_history", []):
            checkoff_date = datetime.fromisoformat(checkoff.replace("Z", "+00:00"))
            if start_date <= checkoff_date <= end_date:
                filtered_checkoffs.append(checkoff)
        
        # The specified start and end dates are formatted to only include the date part.
        start_date = start_date.date()
        end_date = end_date.date()
        
        # All check-offs within the specified date range are printed to the user.
        # If no check-offs are found, the user is informed that no check-offs were found within the date range.
        if filtered_checkoffs:
            print("\nAll check-offs between " + str(start_date) + " and " + str(end_date) + " are:")
            for checkoff in filtered_checkoffs:
                checkoff = datetime.fromisoformat(checkoff.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")
                print("- " + checkoff)
        else:
            print("\nNo check-offs were found between " + str(start_date) + " and " + str(end_date) + ". Please try again with a different date range or check the habit off.")   
       
        
    def get_archived_habits(self):
        """This method loads all archived habits from the "Habits" directory if it exists.
        Each habit's "archive" attribute is then stored in a list, then is checked to see
        whether the habit is archived. If so, the habit name is added to the list and then outputted.
        """
        
        # Checks whether the "Habits" directory exists and exits the method if it doesn't.
        if not os.path.exists("Habits"):
            print("No \"Habits\" folder found. Please create a habit first or check the file path.")
            return None
        
        # Used to store all archived habits.
        archived_habits = []
        
        # Loops through each JSON file in the "Habits" folder, then checks whether the file ends with ".json".
        # If it does, the file is opened and the "archived" key is checked. Should the habit be archived,
        # the habit name is added to the list of archived habits.
        for file_in_folder in os.listdir("Habits"):
            if file_in_folder.endswith(".json"):
                path_of_file = os.path.join("Habits", file_in_folder)
                with open(path_of_file, mode="r", encoding="utf-8") as read_file:
                    loaded_habit = json.load(read_file)
                    if loaded_habit.get("archived", "") == True:
                        archived_habits.append(loaded_habit.get("name", ""))
        
        # A loop runs to print all archived habits from the saved list.
        # If no archived habits are found, the user is informed.
        if archived_habits:
            print("The following habits are archived:")
            for habit in archived_habits:
                print("- " + habit)
        else:
            print("No archived habits found.")
        
        return None
