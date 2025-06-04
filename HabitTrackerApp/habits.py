import json
import os
from datetime import datetime, timezone, date, time, timedelta


class Habits:

    def __init__(self, habit_data: dict = None, habit_name: str = None):
        """This is the constructor for the Habits class.

        Args:
            habit_data (dict, optional): This parameter is used to parse JSON for processing. Defaults to None.
            habit_name (str, optional): This is the name of the habit that the user wishes to interact with. Defaults to None.
        """
        self.habit_data = habit_data
        self.habit_name = habit_name


    def create_habit_file(self):
        """This method creates a JSON file (if it does not
        already exist) for any JSON data inputted into the
        parameters of the class under "habit_data." A folder
        called "Habits" is created (if it doesn't exist), and
        all JSON files are stored within it. Additionally, the
        name of the habit is sanitised in order to use it for the file name.
        """

        # Sanitises the habit name to create a valid filename by replacing any spaces with underscores
        # and converting the name to lowercase
        cleaned_name = self.habit_data["name"].lower().replace(" ", "_")
        
        # Creates the "Habits" directory if it doesn't exist
        # and sets the cleansed habit name to be saved in that directory
        # as its file name, as well as enforcing the file to have the ".json" extension
        os.makedirs("Habits", exist_ok=True)
        filename = os.path.join("Habits", (cleaned_name + ".json"))

        # If the file does not already exist, create it and write the habit data to it
        if not os.path.exists(filename):
            with open(filename, mode="w", encoding="utf-8") as write_file:
                json.dump(self.habit_data, write_file, indent=4)
            return True

        else:
            return None


    def load_habit_file(self):
        """This method loads a JSON file from the folder
        called "Habits" where all habits are stored. The method
        verifies whether the folder exists, and if so, proceeds
        to loop through all the files in the folder. If a JSON file
        is found, the path of the file is saved to access the file.
        The JSON attribute "name" is used to verify whether the user-inputted
        "habit_name" from the class constructor matches the name of the
        habit in the JSON file. If so, the contents of the JSON file is displayed.
        It should be noted that "habit_name" is used to sarch for in all JSON files. The
        attribute is also sanitised to match the format of the JSON file.
        
        Returns:
            loaded_habit (dict): The contents of the JSON file that matches habit_name.
        """
        
        # Checks whether the "Habits" directory exists and exits the method if it doesn't
        if not os.path.exists("Habits"):
            print("No \"Habits\" folder found. Please create a habit first or check the file path.")
            return None
        
        # Loops through all the files in the "Habits" directory and checks
        # if a file is a JSON file. If so, it loads the file and checks if the "name" attribute
        # within the JSON data matches the "habit_name" parameter from the class constructor.
        # If so, the contents of the JSON file are returned.
        for file_in_folder in os.listdir("Habits"):
            if file_in_folder.endswith(".json") == True:
                path_of_file = os.path.join("Habits", file_in_folder)
                with open(path_of_file, mode="r", encoding="utf-8") as read_file:
                    loaded_habit = json.load(read_file)
            
                    if loaded_habit.get("name", "").lower().replace("_", " ") == self.habit_name.lower().replace("_", " "):
                        return loaded_habit

            # If the file is not a JSON file, print an error message and exit the method.
            else:
                print("The file \"" + file_in_folder + "\" is not a JSON file. Please check the file format in the \"Habits\" directory.")
                return None
        
        

        # If no matching habit is found, print an error message and exits the method.
        print("The habit \"" + self.habit_name + "\" was not found. Try searching for another habit or check possible typos.")
            
        return False


    def edit_habit_file(self):
        """This method loads a JSON file by calling the "load_habit_file()" method.
        If the file is found, the user is prompted to enter new data for the habit,
        namely the name, description, periodicity, and archived status. It should be noted
        that, for periodicity, the input will loop until a valid input ("daily"/"weekly") is
        entered. The user is also prompted to confirm whether they want to save the changes.
        If the user accepts,the new data is saved to the JSON file. If the user does not accept,
        no changes are made and the method ends.
        """
        
        # Checks whether the "Habits" directory exists and exits the method if it doesn't
        if not os.path.exists("Habits"):
            print("No \"Habits\" folder found. Please create a habit first or check the file path.")
            return None

        
        # Loads the habit file using the "load_habit_file()" method and checks whether the file
        # was found. If not, an error message is printed and the method ends.
        loaded_habit = self.load_habit_file()
        if loaded_habit is None:
            print("No habit was found to edit. Please check the habit name for typos or create a new habit.")
            return None
        
        else:
            
            # Checks whether the habit is archived. If it is, an error message is printed
            # and the method ends. This is to prevent editing archived habits.
            if loaded_habit.get("archived", False):
                print("The habit \"" + self.habit_name + "\" is archived and cannot be edited. Please unarchive the habit first.")
                return None
            
            # If the habit file was found, the user is prompted to enter new data for the habit. This consists of
            # a new name, description, periodicity, and archived status. The user is also able to press Enter to
            # keep the existing data.
            print("Please enter the new data for the habit. If you want to keep the same data, just press Enter.")
            
            new_name = input("New name: ")
            new_description = input("New description: ")
            
            # Loops until the user enters a valid periodicity ("daily" or "weekly") or presses Enter to keep the same data.
            # If the user enters an invalid input, an error message is printed and the loop continues.
            while True:
                new_periodicity = input("New periodicity (daily/weekly): ").strip().lower()
                if new_periodicity in ("", "daily", "weekly"):
                    break
                print("Invalid input. Please enter \"daily\" or \"weekly,\" or press Enter to keep the same data.")

            # If the user inputted "yes," "y," "true," or "1," the input is stored as True and the value
            # isAccepted is changed to True.
            isAccepted = False
            confirmation = input("Are you sure you want to save your changes to the habit? This cannot be reversed (yes/no): ").strip().lower()
            isAccepted = confirmation in ("yes", "y", "true", "1")
            
            # If isAccepted is True, the new data overwrites the pre-existing data in the JSON file.
            if isAccepted:
            
                if new_name:
                    loaded_habit["name"] = new_name
                if new_description:
                    loaded_habit["description"] = new_description
                if new_periodicity:
                    loaded_habit["periodicity"] = new_periodicity


                # The JSON file is then saved with the new data, and a success message is printed.
                with open(os.path.join("Habits", (self.habit_name.lower().replace(" ", "_") + ".json")), mode="w", encoding="utf-8") as write_file:
                    json.dump(loaded_habit, write_file, indent=4)
                
                print("The habit \"" + self.habit_name + "\" was successfully edited and saved.")
                return None
            
            # If the user does not accept the changes, the user is informed that no changes were made and the method ends.
            else:
                print("The habit \"" + self.habit_name + "\" was not edited. No changes were made.")
                return None
        

    def delete_habit_file(self):
        """This method deletes a JSON file from the "Habits" directory.
        It receives the "habit_name" parameter from the user via the
        class constructor, then loops through all the contents of all JSON
        files in the directory. If the "name" property within a JSON file
        matches "habit_name," that file is deleted.
        """
        # All files within the "Habits" directory are looped through.
        # Should the file be a JSON file, the path of the file is saved,
        # then opened. The JSON data is loaded and the "name" attribute is checked to see if
        # it matches the "habit_name" parameter from the class constructor (after being
        # sanitised to match JSON formatting). If so, the file is deleted.
        for file_in_folder in os.listdir("Habits"):
            if file_in_folder.endswith(".json") == True:
                path_of_file = os.path.join("Habits", file_in_folder)
                with open(path_of_file, mode="r", encoding="utf-8") as read_file:
                    loaded_habit = json.load(read_file)
                if loaded_habit.get("name", "").lower().replace("_", " ") == self.habit_name.lower().replace("_", " "):
                    os.remove(path_of_file)
                    print("The habit \"" + self.habit_name + "\" was successfully deleted.")
                    return None
        
        # If the habit was not found, an error message is printed and the method ends.
        print("The habit \"" + self.habit_name + "\" was not found. Try searching for another habit or check possible typos.")
        return None


    def create_predefined_habits(self):
        """This method creates a set of predefined habits
        via JSON. Five predetermined habits are made with at least
        4 weeks of tracking data each. Once the habits are defined,
        the method "create_habit_file(habit_data)" is called to
        create the JSON files for each habit (if they do not already
        exist).
        """

        # Here, a predefined habit is created with the following attributes:
        # name, description, periodicity, archived status, has_checked-off_today status,
        # creation_date_and_time, and check_off_history. The check-off history
        # contains a minimum of 4 weeks of data, with each date being a string.
        # The attributes are stored within a dictionary to be later converted to JSON.
        # 5 predefined habits are created in total.
        habit1 = {
            "name": "Message a friend",
            "description": "Send a message to any friend in order to see how they are doing.",
            "periodicity": "daily",
            "archived": False,
            "has_checked_off_today": False,
            "creation_date_time": "2025-03-30T15:23:11Z",
            "check_off_history": [
                "2025-03-30T15:24:42Z",
                "2025-04-01T12:54:39Z",
                "2025-04-02T09:12:11Z",
                "2025-04-03T18:45:46Z",
                "2025-04-05T08:00:29Z",
                "2025-04-06T16:30:11Z",
                "2025-04-07T11:15:43Z",
                "2025-04-09T14:20:28Z",
                "2025-04-11T10:05:19Z",
                "2025-04-13T17:45:50Z",
                "2025-04-14T13:30:10Z",
                "2025-04-15T09:55:33Z",
                "2025-04-17T12:40:22Z",
                "2025-04-18T08:15:11Z",
                "2025-04-20T14:25:38Z",
                "2025-04-21T10:50:47Z",
                "2025-04-22T16:05:29Z",
                "2025-04-24T11:30:18Z",
                "2025-04-25T09:45:37Z",
                "2025-04-27T15:55:11Z",
                "2025-04-28T13:20:45Z",
                "2025-04-30T10:10:22Z",
                "2025-05-01T12:30:11Z",
                "2025-05-06T14:40:55Z",
                "2025-05-07T16:50:33Z",
                "2025-05-09T08:20:11Z",
                "2025-05-11T10:30:22Z",
                "2025-05-15T12:40:11Z",
                "2025-05-18T14:50:55Z",
            ],
        }

        habit2 = {
            "name": "Go to the gym",
            "description": "Go to the gym for at least 45 minutes.",
            "periodicity": "daily",
            "archived": False,
            "has_checked_off_today": False,
            "creation_date_time": "2025-04-12T11:57:03Z",
            "check_off_history": [
                "2025-04-12T12:01:44Z",
                "2025-04-13T11:46:49Z",
                "2025-04-14T10:10:10Z",
                "2025-04-15T09:06:32Z",
                "2025-04-16T12:34:27Z",
                "2025-04-17T16:29:59Z",
                "2025-04-18T08:37:18Z",
                "2025-04-19T12:32:20Z",
                "2025-04-20T11:58:07Z",
                "2025-04-21T09:28:14Z",
                "2025-04-22T14:45:36Z",
                "2025-04-23T10:15:22Z",
                "2025-04-24T12:54:11Z",
                "2025-04-25T16:03:41Z",
                "2025-04-26T08:21:32Z",
                "2025-04-27T10:40:19Z",
                "2025-04-28T12:50:27Z",
                "2025-04-29T14:55:28Z",
                "2025-04-30T11:05:40Z",
                "2025-05-05T13:19:10Z",
                "2025-05-06T15:21:56Z",
                "2025-05-07T08:47:32Z",
                "2025-05-11T10:55:33Z",
                "2025-05-12T12:05:18Z",
                "2025-05-13T14:33:41Z",
                "2025-05-16T16:57:19Z",
                "2025-05-17T09:39:40Z",
                "2025-05-19T11:28:32Z",
            ],
        }

        habit3 = {
            "name": "Do the laundry",
            "description": "Wash the laundry, iron all the clothes, and put the clothes away.",
            "periodicity": "weekly",
            "archived": False,
            "has_checked_off_today": False,
            "creation_date_time": "2025-01-18T17:12:06Z",
            "check_off_history": [
                "2025-01-19T18:23:17Z",
                "2025-01-26T15:48:38Z",
                "2025-02-02T12:10:51Z",
                "2025-02-09T14:50:33Z",
                "2025-02-16T19:31:47Z",
                "2025-02-23T16:29:38Z",
                "2025-03-02T12:40:11Z",
                "2025-03-09T14:39:55Z",
                "2025-03-16T16:22:49Z",
                "2025-03-23T19:28:10Z",
                "2025-03-30T17:02:24Z",
                "2025-04-06T15:03:06Z",
                "2025-04-13T18:45:50Z",
                "2025-04-20T14:30:01Z",
                "2025-04-27T17:15:43Z",
                "2025-05-05T20:00:29Z",
                "2025-05-16T13:55:41Z",
            ],
        }

        habit4 = {
            "name": "Clean the house",
            "description": "Clean the house, including dusting, vacuuming, and mopping.",
            "periodicity": "weekly",
            "archived": False,
            "has_checked_off_today": False,
            "creation_date_time": "2025-02-11T07:21:03Z",
            "check_off_history": [
                "2025-02-12T16:30:16Z",
                "2025-02-19T19:47:27Z",
                "2025-02-26T21:51:31Z",
                "2025-03-05T13:05:29Z",
                "2025-03-12T14:19:41Z",
                "2025-03-19T16:45:30Z",
                "2025-03-26T18:28:17Z",
                "2025-04-02T13:49:28Z",
                "2025-04-09T17:50:39Z",
                "2025-04-16T16:01:46Z",
                "2025-04-23T11:13:16Z",
                "2025-04-30T14:07:35Z",
                "2025-05-07T12:40:09Z",
                "2025-05-14T13:53:28Z",
            ],
        }

        habit5 = {
            "name": "Writing in a journal",
            "description": "Write in a journal about your day for at least 15 minutes.",
            "periodicity": "daily",
            "archived": False,
            "has_checked_off_today": False,
            "creation_date_time": "2025-04-07T21:59:13Z",
            "check_off_history": [
                "2025-04-08T22:10:23Z",
                "2025-04-09T21:28:46Z",
                "2025-04-10T23:41:11Z",
                "2025-04-14T21:17:30Z",
                "2025-04-17T20:39:58Z",
                "2025-04-18T22:30:43Z",
                "2025-04-19T23:40:19Z",
                "2025-04-22T23:50:55Z",
                "2025-04-23T21:57:28Z",
                "2025-04-25T22:39:00Z",
                "2025-04-26T21:45:12Z",
                "2025-04-27T23:10:17Z",
                "2025-04-29T22:21:13Z",
                "2025-05-01T20:55:45Z",
                "2025-05-03T23:29:20Z",
                "2025-05-04T22:19:10Z",
                "2025-05-05T21:15:33Z",
                "2025-05-08T20:39:16Z",
                "2025-05-09T19:33:59Z",
                "2025-05-10T22:11:01Z",
                "2025-05-12T21:50:09Z",
                "2025-05-13T20:35:37Z",
                "2025-05-14T19:49:27Z",
                "2025-05-15T22:27:24Z",
                "2025-05-16T21:46:36Z",
                "2025-05-17T20:31:15Z",
                "2025-05-18T19:27:29Z",
                "2025-05-19T22:20:02Z",
            ],
        }

        # Here, several instances of the "Habits" class are created
        # to parse the habit data and to create JSON files for each
        # respective habit.
        Habits(habit_data=habit1).create_habit_file()
        Habits(habit_data=habit2).create_habit_file()
        Habits(habit_data=habit3).create_habit_file()
        Habits(habit_data=habit4).create_habit_file()
        Habits(habit_data=habit5).create_habit_file()

    
    def checkoff_habit(self):
        """This method checks off a habit by loading the JSON file
        using the "load_habit_file()" method. If the file is found,
        the user is prompted to confirm whether they want to check-off
        the habit. If the user accepts, the current date and time are
        fetched and then formatted to match the format within the JSON file
        (namely, ISO 8601) without any microseconds. The habit is then checked-off
        for today and the current formatted date and time is appended to the
        "check_off_history" attribute within the JSON file. The file is then saved
        and the user is informed thereof. If the user does not accept, no changes are made
        and the method ends with a notification message.
        """
        # Checks whether the "Habits" directory exists and exits the method if it doesn't
        if not os.path.exists("Habits"):
            print("No \"Habits\" folder found. Please create a habit first or check the file path.")
            return None

        # Loads the habit file using the "load_habit_file()" method and checks whether the file
        # was found. If not, an error message is printed from the "load_habit_file()" method
        # and this method ends.
        loaded_habit = self.load_habit_file()
        if loaded_habit is None:
            return None
        else:
            
            # Checks whether the habit is archived. If it is, an error message is printed
            # and the method ends. This is to prevent checking off archived habits.
            if loaded_habit.get("archived", False):
                print("The habit \"" + self.habit_name + "\" is archived and cannot be checked-off. Please unarchive the habit first.")
                return None
            
            # If the habit file was found, the user is asked whether they would like
            # to check-off the habit for today.
            isCheckedOff = False 
            confirmation = input("Would you like to check-off the habit \"" + self.habit_name + "\" (yes/no)? ")
            isCheckedOff = confirmation in ("yes", "y", "true", "1")
            
            # The current date and time are fetched and formatted to show the time within
            # the UTC timezone by setting it to "Z". The microseconds are removed and the
            # date and time are formatted to match the ISO 8601 format.
            current_datetime = datetime.now(timezone.utc)
            current_datetime = current_datetime.replace(microsecond=0)
            json_datetime_format = current_datetime.isoformat().replace("+00:00", "Z")
            
            # If the user wishes to check-off the habit, the current date and time
            # are appended to the "check_off_history" attribute within the JSON file.
            # If the habit was not checked-off today, the "has_checked-off_today" attribute
            # is set to True and the file is saved. The user is informed with a message
            # that the habit was successfully checked-off. If the habit was already
            # checked-off today, the user is informed accordingly and the method ends.
            if isCheckedOff:

                loaded_habit["check_off_history"].append(json_datetime_format)
                if loaded_habit["has_checked_off_today"] == False:
                    loaded_habit["has_checked_off_today"] = True

                    with open(os.path.join("Habits", (self.habit_name.lower().replace(" ", "_") + ".json")), mode="w", encoding="utf-8") as write_file:
                        json.dump(loaded_habit, write_file, indent=4)
                
                    print("The habit \"" + self.habit_name + "\" was successfully checked-off!")
                    return None
                else:
                    print("You already checked-off the habit \"" + self.habit_name + "\" recently. Please check again tomorrow.")
                    return None
            
            # If the user does not wish to check-off the habit, the user is informed
            # that no changes were made and the method ends.
            else:
                print("The habit \"" + self.habit_name + "\" was not checked-off. No changes were made.")
                return None
        
       
    def setcheckoff_to_false(self):
        """This method loops through all the JSON files in the "Habits" directory
        and checks whether the "has_checked_off_today" attribute is set to "true"
        within all JSON files. If so, the method checks the periodicity of the habit
        and calculates whether the last check-off date is before today for daily habits
        and this week for weekly habits. If the last check-off date is before today or this week,
        the "has_checked_off_today" attribute is set to "false" and the file is saved.
        """
        
        # Checks whether the "Habits" directory exists and exits the method if it doesn't.
        if not os.path.exists("Habits"):
            print("No \"Habits\" folder found. Please create a habit first or check the file path.")
            return None

        # Gets the current date and time in UTC and sets the time to midnight for the given timezone (UTC).
        # This is done to ensure that the last habit check-off date is compared to the start of the day.
        today_midnight = datetime.combine(date.today(), time.min).replace(tzinfo=timezone.utc)
        
        # Gets the start of the week by subtracting the number of days since the last Monday from today.
        start_of_week = today_midnight - timedelta(days=today_midnight.weekday())
        
        # Loops through all the files in the "Habits" directory and checks
        # if a file is a JSON file. If so, it loads the file and grabs the
        # last value in the "check_off_history" list, then formats the value
        # into a datetime object.
        for file_in_folder in os.listdir("Habits"):
            if file_in_folder.endswith(".json") == True:
                path_of_file = os.path.join("Habits", file_in_folder)
                with open(path_of_file, mode="r", encoding="utf-8") as read_file:
                    loaded_habit = json.load(read_file)
                    all_checkoffs = loaded_habit.get("check_off_history", [])
                    if all_checkoffs:
                        last_checkoff = all_checkoffs[-1]
                        last_checkoff = datetime.strptime(last_checkoff, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                        
                        # If the periodicity of the habit is "daily," the method
                        # compares the last check-off date to today via the "today_midnight" variable.
                        # If the last check-off date is before today, the "has_checked_off_today" attribute
                        # is set to "False" and the file is saved.
                        if loaded_habit.get("periodicity", "").lower() == "daily":
                            
                            if last_checkoff < today_midnight:
                                loaded_habit["has_checked_off_today"] = False
                                with open(path_of_file, mode="w", encoding="utf-8") as write_file:
                                    json.dump(loaded_habit, write_file, indent=4)
                        
                        # If the periodicity of the habit is "weekly," the method
                        # compares the last check-off date to today via the "start_of_week" variable.
                        # If the last check-off date is before the previous week, the "has_checked_off_today" attribute
                        # is set to "False" and the file is saved.
                        else:
                            
                            if last_checkoff < start_of_week:
                                loaded_habit["has_checked_off_today"] = False
                                with open(path_of_file, mode="w", encoding="utf-8") as write_file:
                                    json.dump(loaded_habit, write_file, indent=4)
        return None
    
    
    def archive_habit(self):
        """This method archives a habit by loading the JSON file
        using the "load_habit_file()" method. If the file is found,
        the "archived" attribute within the JSON file is set to True and the file is saved.
        The user is informed that the habit was successfully archived. In the event that
        the habit is already archived, an error message is printed and the method ends.
        """
        
        # Checks whether the "Habits" directory exists and exits the method if it doesn't
        if not os.path.exists("Habits"):
            print("No \"Habits\" folder found. Please create a habit first or check the file path.")
            return None

        # Loads the habit file using the "load_habit_file()" method and checks whether the file
        # was found. If not, an error message is printed and the method ends.
        loaded_habit = self.load_habit_file()
        if loaded_habit is None:
            print("No habit was found to archive. Please check the habit name for typos or create a new habit.")
            return None
        
        # If the habit is already archived, an error message is printed and the method ends.
        elif loaded_habit.get("archived") == True:
            print("The habit \"" + self.habit_name + "\" is already archived. No changes were made.")
            return None
        
        else:
            # If the user wishes to archive the habit, the "archived" attribute within
            # the JSON file is set to True and the file is saved. The user is informed with a message
            # that the habit was successfully archived.
            loaded_habit["archived"] = True
            with open(os.path.join("Habits", (self.habit_name.lower().replace(" ", "_") + ".json")), mode="w", encoding="utf-8") as write_file:
                json.dump(loaded_habit, write_file, indent=4)
            print("The habit \"" + self.habit_name + "\" was successfully archived.")
            return None
            
    
    def unarchive_habit(self):
        """This method unarchives a habit by loading the JSON file
        using the "load_habit_file()" method. If the file is found,
        the "archived" attribute within the JSON file is set to False
        and the file is saved. The user is informed that the habit was
        successfully unarchived. In the event that the habit is not archived,
        an error message is printed and the method ends.
        """
        
        # Checks whether the "Habits" directory exists and exits the method if it doesn't.
        if not os.path.exists("Habits"):
            print("No \"Habits\" folder found. Please create a habit first or check the file path.")
            return None

        # Loads the habit file using the "load_habit_file()" method and checks whether the file
        # was found. If not, an error message is printed and the method ends.
        loaded_habit = self.load_habit_file()
        if loaded_habit is None:
            print("No habit was found to unarchive. Please check the habit name for typos or create a new habit.")
            return None
        
        # If the habit is not archived, an error message is printed and the method ends.
        elif loaded_habit.get("archived") == False:
            print("The habit \"" + self.habit_name + "\" is not archived. No changes were made.")
            return None
        
        else:
            # If the user wishes to unarchive the habit, the "archived" attribute within
            # the JSON file is set to False and the file is saved. The user is informed with a message
            # that the habit was successfully unarchived.

            loaded_habit["archived"] = False
            with open(os.path.join("Habits", (self.habit_name.lower().replace(" ", "_") + ".json")), mode="w", encoding="utf-8") as write_file:
                json.dump(loaded_habit, write_file, indent=4)        
            print("The habit \"" + self.habit_name + "\" was successfully unarchived.")
            return None
                
