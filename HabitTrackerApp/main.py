import questionary
import json
from datetime import datetime, timezone
from habits import Habits
from analytics import Analytics


def cli():
    """This function is responsible for creating a command-line interface (CLI)
    for the user to interact with. It provides the user with several choices, with
    each choice executing a specific piece of functionality as defined within either
    the Habits class or the Analytics class.
    """
    
    exited_program = False
    while (exited_program == False):
        
        # Prompts the user with a welcome message and a choice of actions within the CLI.
        choice = questionary.select("Welcome to the habit tracker! What would you like to do?",
            choices=["Create a habit", "Check-off a habit", "View a habit", "Edit a habit",
                    "Delete a habit", "Archive/Unarchive a habit", "View analytics", "Help", "Exit"]).ask()
        
        
        if choice == "Create a habit":
            
            # Prompts the user for the details of the habit they want to create, namely
            # the name, description, and periodicity (daily or weekly) of the habit.
            # Other essential data, such as archived status and date and time of creation are
            # set automatically.
            while True:
                habit_name = questionary.text("Enter the name of the habit. To exit here, type \"Exit\" (with double quotation marks).").ask()
                
                # Makes sure that an empty habit name and whitespace "names" are not accepted.
                if (habit_name) and (habit_name.strip()):
                    break
                            
                else:
                    print("This field cannot be left empty. Please enter the name of a habit.")
                             
            # Exits the current choice if the user types "Exit" with double quotation marks.
            if habit_name == "\"Exit\"":
                continue
            
            habit_description = questionary.text("Enter a description for the habit. To exit here, type \"Exit\" (with double quotation marks).").ask()
            if habit_description == "\"Exit\"":
                continue
            
            habit_periodicity = (questionary.select("How often do you want to perform this habit?",
                                                choices=["Daily", "Weekly", "Exit selection"]).ask()).lower()
            if habit_name == "Exit selection":
                continue
            
            habit_archived = False
            habit_checked_off_today = False
            
            # The creation date and time of the habit is set to the current date and time in UTC,
            # then formatted without any microseconds and with a "Z" suffix to indicate UTC time.
            habit_creation_time = datetime.now(timezone.utc)
            habit_creation_time = habit_creation_time.replace(microsecond=0)
            json_habit_creation_time = habit_creation_time.isoformat().replace("+00:00", "Z")
            
            habit_checkoff_history = []
            
            # The habit data is stored in a dictionary, which is then passed to the Habits class
            # to create a new habit file in JSON.
            habit_data = {
                "name": habit_name,
                "description": habit_description,
                "periodicity": habit_periodicity,
                "archived": habit_archived,
                "has_checked_off_today": habit_checked_off_today,
                "creation_date_time": json_habit_creation_time,
                "check_off_history": habit_checkoff_history
            }
                
            create_habit = Habits(habit_data = habit_data, habit_name = habit_name)
            
            # The create_habit_file method of the Habits class is called to create the habit file.
            # If the file is created successfully, a success message is printed.
            if (create_habit.create_habit_file() == True):
                print("\nThe habit has been created successfully!\n")
            else:
                print("\nThere was an error creating the habit. This is likely because a habit with that name already exists. Please try another name.\n")
            
        
        elif choice == "Check-off a habit":
            
            # Retrieves the name of the habit that the user wants to check-off.
            habit_name = questionary.text("Please enter the name of the habit you want to check-off. To exit here, type \"Exit\" (with double quotation marks).").ask()
            
            # Exits the current choice if the user types "Exit" with double quotation marks.
            if habit_name == "\"Exit\"":
                continue
            
            # Creates an instance of the Habits class with the habit name, then calls the checkoff_habit method
            # to check-off the habit. If the habit is checked off successfully, a success message is printed.
            print("\n")
            checkoff_habit = Habits(habit_name = habit_name)
            checkoff_habit.checkoff_habit()
            print("\n")
        
        
        elif choice == "View a habit":
            
            # Retrieves the name of the habit that the user wants to view.
            habit_name = questionary.text("Please enter the name of the habit you want to view. To exit here, type \"Exit\" (with double quotation marks).").ask()
            
            # Exits the current choice if the user types "Exit" with double quotation marks.
            if habit_name == "\"Exit\"":
                continue
            
            # Creates an instance of the Habits class with the habit name, then calls the load_habit_file method
            # to load the habit data. If the habit data is found, it is printed in a formatted JSON style.
            view_habit = Habits(habit_name = habit_name)
            habit_data = view_habit.load_habit_file()
            if habit_data:
                print("\nThe habit \"" + habit_name + "\" was found!\n\n"+ json.dumps(habit_data, indent=4))
                print("\n")
            else:
                return None
        
        
        elif choice == "Edit a habit":
            
            # Retrieves the name of the habit that the user wants to edit.
            habit_name = questionary.text("Enter the name of the habit you wish to change. To exit here, type \"Exit\" (with double quotation marks).").ask()
            
            # Exits the current choice if the user types "Exit" with double quotation marks.
            if habit_name == "\"Exit\"":
                continue
            
            # Creates an instance of the Habits class with the habit name, then calls the edit_habit_file method
            # to edit the habit data by prompting input fields within the function and not via Questionary.
            print("\n")
            edit_habit = Habits(habit_name = habit_name)
            edit_habit.edit_habit_file()
            print("\n")
            
            
        elif choice == "Delete a habit":
            
            # Retrieves the name of the habit that the user wants to delete.
            habit_name = questionary.text("Please enter the name of the habit you want to delete. To exit here, type \"Exit\" (with double quotation marks).").ask()
            
            # Exits the current choice if the user types "Exit" with double quotation marks.
            if habit_name == "\"Exit\"":
                continue
            
            # Prompts the user for confirmation before deleting the habit.
            # If the user confirms, the habit is deleted; otherwise, the deletion is cancelled.
            confirmation = questionary.confirm("Are you sure you want to delete the habit \"" + habit_name + "\"? This action cannot be undone.").ask()
            if not confirmation:
                print("\nHabit deletion cancelled.\n")
                return None
            
            # Creates an instance of the Habits class with the habit name, then calls the delete_habit method
            # to delete the habit. If the habit is deleted successfully, a success message is printed.
            print("\n")
            delete_habit = Habits(habit_name = habit_name)
            delete_habit.delete_habit_file()
            print("\n")
        
        
        elif choice == "Archive/Unarchive a habit":
            
            exit_archive_selection = False
            
            # A loop is created so that the selection between "Archive a habit" and "Unarchive a habit"
            # will exit once the "Exit" option has been selected.
            while exit_archive_selection == False:
                
                # Prompts the user to choose whether they want to archive or unarchive a habit, then
                # stores the user's choice.
                archive_choice = questionary.select("Would you like to archive or unarchive a habit?",
                                        choices=["Archive a habit", "Unarchive a habit", "Exit"]).ask()
                
                
                # Depending on the user's choice, the user is prompted to enter the name of the habit they wish to
                # either archive or unarchive.
                if archive_choice == "Archive a habit":
                    habit_name = questionary.text("Please enter the name of the habit you want to archive. To exit here, type \"Exit\" (with double quotation marks).").ask()
                    
                    # Exits the current choice if the user types "Exit" with double quotation marks.
                    if habit_name == "\"Exit\"":
                        continue
                    
                    # The user is prompted for confirmation before archiving the habit. If the user does not confirm,
                    # the archiving is cancelled and a message is printed.
                    confirmation = questionary.confirm("Are you sure you want to archive the habit \"" + habit_name + "\"?").ask()
                    if not confirmation:
                        print("\nThe habit was not archived. No changes were made.\n")
                        return None
                    
                    # Creates an instance of the Habits class with the habit name, then calls the archive_habit method
                    # to archive the habit. If the habit is archived successfully, a success message is printed.
                    print("\n")
                    archive_habit = Habits(habit_name = habit_name)
                    archive_habit.archive_habit()
                    print("\n")
                
                elif archive_choice == "Unarchive a habit":
                    habit_name = questionary.text("Please enter the name of the habit you want to unarchive. To exit here, type \"Exit\" (with double quotation marks).").ask()
                    
                    # Exits the current choice if the user types "Exit" with double quotation marks.
                    if habit_name == "\"Exit\"":
                        continue
                    
                    confirmation = questionary.confirm("Are you sure you want to unarchive the habit \"" + habit_name + "\"?").ask()
                    if not confirmation:
                        print("\nThe habit was not unarchived. No changes were made.\n")
                        return None

                    # Creates an instance of the Habits class with the habit name, then calls the unarchive_habit method
                    # to unarchive the habit. If the habit is unarchived successfully, a success message is printed.
                    print("\n")
                    unarchive_habit = Habits(habit_name=habit_name)
                    unarchive_habit.unarchive_habit()
                    print("\n")
                    
                else:
                    exit_archive_selection = True
                    print("\nExiting selection...\n")
        
        
        elif choice == "View analytics":
            
            # Prompts the user several options as to which analytics they would like to select.
            # The section is in a loop so that the selection will only stop once the loop is ended
            # via the "Exit habit selection" option.
            analytics_exit = False
            while analytics_exit == False:
                analytics_choice = questionary.select("Which analytic do you wish to perform?", choices=["Show all habits", "Show the longest streak for a single habit",
                                                                                                     "Show the longest streak across all habits", "Show the habit with the most check-offs",
                                                                                                     "Show the habit with the least check-offs", "Show the habits with the same periodicity",
                                                                                                     "Show all the check-offs of a habit within a range of time", "Show all archived habits",
                                                                                                     "Exit habit selection"]).ask()
                
                if analytics_choice == "Show all habits":
                    
                    # A message is printed before calling the show_all_habits method of the
                    # Analytics class. The method in question searches through all JSON files,
                    # retrieves the names of the habits, and outputs them.
                    print("\nHere is a list of all your habits, both archived and unarchived:\n")
                    show_all_habits = Analytics()
                    show_all_habits.show_all_habits()
                    print("\nAll habits shown!\n")
                    
                    
                elif analytics_choice == "Show the longest streak for a single habit":
                    
                    # The user is prompted to enter the name of the habit that they wish to view the longest streak of.
                    habit_name = questionary.text("Please enter the name of the habit you want to view the longest streak of. To exit here, type \"Exit\" (with double quotation marks).").ask()
                    
                    # Exits the current choice if the user types "Exit" with double quotation marks.
                    if habit_name == "\"Exit\"":
                        continue
                    
                    # An instace of the Analytics class is created with the "get_longest_streak_single_habit"
                    # method being called. The method searches the check-off history for the habit and
                    # outputs the longest consecutive streak.
                    print("\n")
                    longest_streak_single_habit = Analytics(habit_name = habit_name)
                    longest_streak_single_habit.get_longest_streak_single_habit()
                    print("\n")
                                            
                
                elif analytics_choice == "Show the longest streak across all habits":
                    
                    # An instace of the Analytics class is created with the "get_longest_streak_all_habits"
                    # method being called. The method searches the check-off history for all habits and
                    # outputs the longest consecutive streak amongst all habits.
                    print("\nHere is all the longest streaks for all your habits:\n")
                    longest_streak_all_habits = Analytics()
                    longest_streak_all_habits.get_longest_streak_all_habits()
                    
                    
                elif analytics_choice == "Show the habit with the most check-offs":
                    
                    # An instance of the Analytics class is created, then the "get_most_checkoff_history"
                    # method from within the class searches all habits to determine which one has
                    # the most entries for habit checkoffs. This is then displayed to the user.
                    print("\n")
                    most_checkoffs = Analytics()
                    most_checkoffs.get_most_checkoff_history()
                    print("\nHabit(s) shown!\n")
                    
                    
                elif analytics_choice == "Show the habit with the least check-offs":
                    
                    # An instance of the Analytics class is created, then the "get_least_checkoff_history"
                    # method from within the class searches all habits to determine which one has
                    # the least entries for habit checkoffs. This is then displayed to the user.
                    print("\n")
                    least_checkoffs = Analytics()
                    least_checkoffs.get_least_checkoff_history()
                    print("\nHabit(s) shown!\n")
                    
                    
                elif analytics_choice == "Show the habits with the same periodicity":
                    
                    # An instance of the Analytics class is created, from which the
                    # "get_habits_with_same_periodicity" method originates. The function
                    # searches through all habits which has the same periodicity that the user
                    # specifies, then outputs them to the user.
                    
                    habit_periodicity = (questionary.select("Which habit periodicity do you wish to search for?",
                                                           choices=["Daily", "Weekly", "Exit selection"]).ask()).lower()
                    
                    if habit_periodicity == "Exit selection":
                        continue
                    
                    print("\n")
                    same_periodicity = Analytics()
                    same_periodicity.get_habits_with_same_periodicity(wanted_periodicity = habit_periodicity)
                    print("\n")
                    
                    
                elif analytics_choice == "Show all the check-offs of a habit within a range of time":
                    
                    # An instance of the Analytics class is created, from which the
                    # "get_history_of_checkoffs_time_range" method originates. The function
                    # searches for the habit that the user inputted, then prompts the user with
                    # a start and end date. All checkoffs between those dates are then found and printed.
                    while True:
                        habit_name = questionary.text("Please enter the name of the habit you would like to use. To exit here, type \"Exit\" (with double quotation marks).").ask()
                        
                        # Makes sure that an empty habit name and whitespace "names" are not accepted.
                        if (habit_name) and (habit_name.strip()):
                            break
                        
                        else:
                            print("This field cannot be left empty. Please enter the name of a habit.")
                    
                    # Exits the current choice if the user types "Exit" with double quotation marks.
                    if habit_name == "\"Exit\"":
                        continue
                        
                    print("\n")
                    range_of_habit_checkoffs = Analytics(habit_name = habit_name)
                    range_of_habit_checkoffs.get_history_of_checkoffs_time_range()
                    print("\n")
                 
                    
                elif analytics_choice == "Show all archived habits":
                    
                    # An instance of the Analytics class is created, from which the "get_archived_habits"
                    # method originates. The function loops through all existing habits and check whether
                    # they have been marked as archived. If so, the names of those habits are outputted
                    # to the user.
                    print("\n")
                    all_archived_habits = Analytics()
                    all_archived_habits.get_archived_habits()
                    print("\n")
                    
                    
                elif analytics_choice == "Exit habit selection":
                    print("Exiting the analytics selection...")
                    analytics_exit = True
                    
                else:
                    print("An error has occurred. Somehow, an unavailable selection was made. Please inform the developer of this software to correct this issue.")
                    analytics_exit = True
                    exited_program = True
        
        
        elif choice == "Help":
            
            help_exit = False
            while help_exit == False:
                help_selection = questionary.select("Here is a guide of what each option does. Please select a function to learn more: ",
                    choices=["Create a habit", "Check-off a habit", "View a habit", "Edit a habit",
                        "Delete a habit", "Archive/Unarchive a habit", "View analytics", "Exit help"]).ask()
                
                if help_selection == "Create a habit":
                    questionary.press_any_key_to_continue("The option 'Create a habit' allows you to create a new habit of your choice.").ask()
                    questionary.press_any_key_to_continue("It gives you the opportunity to input a name for your habit, a description, and a daily/weekly periodicity for when you can check-off your habit.").ask()
                    questionary.press_any_key_to_continue("By default, a newly created habit is not archived and is not checked-off, meaning you will need to do so manually.").ask()
                    
                elif help_selection == "Check-off a habit":
                    questionary.press_any_key_to_continue("The option 'Check-off a habit' allows you to confirm that you have completed a habit for the periodicity that you have specified, i.e., \"Checked-off.\"").ask()
                    questionary.press_any_key_to_continue("It should be noted that you cannot check a habit off if you have already checked it off today/this week and will get a message stating this upon attempting to do so.").ask()
                    questionary.press_any_key_to_continue("This also applies to archived habits.").ask()
                    
                elif help_selection == "View a habit":
                    questionary.press_any_key_to_continue("The option 'View a habit' allows you to see all the data associated with the habit name you inputted, from the time of creation to the check-off history.").ask()
                    questionary.press_any_key_to_continue("The data shown to you will be in JSON format, meaning that the data attribute will be shown on the left, and the relevant data shown on the right.").ask()
                    
                elif help_selection == "Edit a habit":
                    questionary.press_any_key_to_continue("The option 'Edit a habit' allows you to edit any habit that you enter the name for.").ask()
                    questionary.press_any_key_to_continue("This allows you to edit the name, description, and periodicity of the habit if you so desire.").ask()
                    questionary.press_any_key_to_continue("Archived habits cannot be edited, and as such need to be unarchived first.").ask()
                    
                elif help_selection == "Delete a habit":
                    questionary.press_any_key_to_continue("The option 'Delete a habit' allows you to delete any habit by inputting the habit's name. Both archived and unarchived habits can be deleted.").ask()
                    questionary.press_any_key_to_continue("Deleted habits cannot be recovered, however. As such, care needs to be taken when deleting habits.").ask()
                    
                elif help_selection == "Archive/Unarchive a habit":
                    questionary.press_any_key_to_continue("The option 'Archive/Unarchive a habit' allows you to either archive or unarchive a habit. Once archived, a habit cannot be checked-off, loaded, or edited.").ask()
                    questionary.press_any_key_to_continue("Similarly, you can unarchive a habit by inputting the name of an archived habit to make it available for loading, editing, or checking off.").ask()
                    
                elif help_selection == "View analytics":
                    
                    analytics_help_exit = False
                    while analytics_help_exit == False:
                        analytics_help_selection = questionary.select("Select to learn more:", choices=["Show all habits", "Show the longest streak for a single habit",
                                                                                                     "Show the longest streak across all habits", "Show the habit with the most check-offs",
                                                                                                     "Show the habit with the least check-offs", "Show the habits with the same periodicity",
                                                                                                     "Show all the check-offs of a habit within a range of time", "Show all archived habits",
                                                                                                     "Exit analytics help"]).ask()
                    
                        if analytics_help_selection == "Show all habits":
                            questionary.press_any_key_to_continue("The option 'Show all habits' lists all the habits that you have created, including both archived and unarchived ones.").ask()
                            questionary.press_any_key_to_continue("Naturally, the only habits excluded are those that have been deleted.").ask()
                        
                        elif analytics_help_selection == "Show the longest streak for a single habit":
                            questionary.press_any_key_to_continue("The option 'Show the longest streak for a single habit' shows the longest consecutive streak of check-offs for a specific habit that you have selected.").ask()
                            questionary.press_any_key_to_continue("Archived habits will not work and instead show a message that they must be unarchived first.").ask()
                        
                        elif analytics_help_selection == "Show the longest streak across all habits":
                            questionary.press_any_key_to_continue("The option 'Show the longest streak across all habits' displays the longest streak amongst all your habits, thereby saving time from individually looking at the streaks for all habits.").ask()
                            questionary.press_any_key_to_continue("It should be noted that archived habits will naturally be skipped when determining the longest streak.").ask()
                        
                        elif analytics_help_selection == "Show the habit with the most check-offs":
                            questionary.press_any_key_to_continue("The option 'Show the habit with the most check-offs' identifies the habit you have checked off the most amount of times.").ask()
                        
                        elif analytics_help_selection == "Show the habit with the least check-offs":
                            questionary.press_any_key_to_continue("The option 'Show the habit with the least check-offs' identifies the habit you have checked off the least amount of times.").ask()
                        
                        elif analytics_help_selection == "Show the habits with the same periodicity":
                            questionary.press_any_key_to_continue("The option 'Show the habits with the same periodicity' lists all habits that share the same periodicity (daily or weekly).").ask()
                            questionary.press_any_key_to_continue("Before any output is made, however, you first need to select whether you wish to view habits with a daily or a weekly periodicity.").ask()
                        
                        elif analytics_help_selection == "Show all the check-offs of a habit within a range of time":
                            questionary.press_any_key_to_continue("The option 'Show all the check-offs of a habit within a range of time' allows you to view all check-offs for a specific habit within a date range you provide.").ask()
                            questionary.press_any_key_to_continue("The date you insert should be in the following format: YYYY-MM-DD. Additionally, archived habits cannot be used.").ask()
                        
                        elif analytics_help_selection == "Show all archived habits":
                            questionary.press_any_key_to_continue("The option 'Show all archived habits' lists all habits that are currently archived.").ask()
                            questionary.press_any_key_to_continue("It is the only way to view the names of archived habits, meaning that if you wish to unarchive a habit but forgot its name, you will need to use this functionality.")
                    
                        elif analytics_help_selection == "Exit analytics help":
                            analytics_help_exit = True
                        
                        else:
                            print("An error has occurred. Somehow, an unavailable selection was made. Please inform the developer of this software to correct this issue.")
                            analytics_help_exit = True
                            exited_program = True
                            
                    
                elif help_selection == "Exit help":
                    print("Exiting the help section...")
                    help_exit = True
                    
                else:
                    print("An error has occurred. Somehow, an unavailable selection was made. Please inform the developer of this software to correct this issue.")
                    help_exit = True
                    exited_program = True


        elif choice == "Exit":
            print("Exiting the habit tracker. Goodbye!")
            exited_program = True
        
        else:
            print("An error has occurred. Somehow, an unavailable selection was made. Please inform the developer of this software to correct this issue.")
            exited_program = True
        

if __name__ == "__main__":
    bootup_habit_functions = Habits()
    bootup_habit_functions.create_predefined_habits()
    bootup_habit_functions.setcheckoff_to_false()
    
    cli()
