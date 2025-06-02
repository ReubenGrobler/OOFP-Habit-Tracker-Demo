from habits import Habits
from analytics import Analytics
import os


class TestProject:
    
    def setup_method(self):
        """This method runs before any testing is performed. Here, methods create predefined test
        data and set their checkoffs to false if the user has not checked-off a habit today, similarly
        to how the habit tracking app operates at startup.
        """
        
        # Before testing, all predefined habits will be created (if the files don't already exist)
        # and any daily checkoffs that were made will be set to false (in the event that they weren't
        # checked-off today).
        bootup_tests = Habits()
        bootup_tests.create_predefined_habits()
        bootup_tests.setcheckoff_to_false()
    
    
    def test_habit(self):
        """This method tests all functions used by the Habits class to determine
        whether they are functional with the use of a combination of test data
        and predefined habit files.
        """
        
        
        # Before testing, JSON data is created for the sake of the "create_habit_file"
        # method, which will naturally need data first before creating a file.
        test_data = {
            "name": "Testing data",
            "description": "Lorem ipsum dolor sit amet",
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
                "2025-04-06T16:30:15Z",
                "2025-04-07T11:15:43Z",
                "2025-04-09T14:20:28Z",
                "2025-04-11T10:05:19Z",
                "2025-04-13T17:31:59Z",
                "2025-04-14T13:36:16Z",
                "2025-04-15T12:11:22Z",
                "2025-04-16T11:49:27Z",
                "2025-04-18T18:59:07Z",
                "2025-04-20T09:26:03Z",
                "2025-04-22T20:37:26Z",
                "2025-04-25T13:33:40Z",
                "2025-04-29T19:08:38Z",
                "2025-04-30T16:04:56Z",
                "2025-05-03T15:01:14Z"
            ]
        }
        
        test_habit = Habits(habit_data = test_data, habit_name = "Testing data")
        
        test_habit.create_habit_file()
        
        # Here, the method is verified to determine whether any output has been made.
        # The test ends if no output has been returned by the method, indicating that
        # the file has not been loaded. 
        loaded_output = test_habit.load_habit_file()
        assert (loaded_output != None)
        
        test_habit.edit_habit_file()
        
        test_habit.checkoff_habit()
        
        test_habit.archive_habit()
        
        test_habit.unarchive_habit()
        
        test_habit.delete_habit_file()
        
        
    def test_analytics(self):
        """This method tests all functions used by the Analytics class to determine
        whether they are functional with the use of a combination of test data
        and predefined habit files.
        """
        
        # Here, an instance of the Analytics class is created while using one
        # of the predefined habits made when starting the testing procedure.
        test_analytics = Analytics(habit_name = "Go to the gym")
        
        test_analytics.show_all_habits()
        
        # This method not only determines what the longest streak of the habit
        # "Go to the gym" is, but also verifies that it is a streak of 19 days;
        # the expected streak length.
        longest_gym_streak = test_analytics.get_longest_streak_single_habit()
        assert (longest_gym_streak == 19)
        
        test_analytics.get_longest_streak_all_habits()
        
        # This method checks which habit has the most checkoffs. It is then
        # verified whether the answer correlates to the expected outcome,
        # "Message a friend"
        most_checkoff_history = test_analytics.get_most_checkoff_history()
        assert (most_checkoff_history == "Message a friend")
        
        # This method checks which habit has the least checkoffs. It is then
        # verified whether the answer correlates to the expected outcome,
        # "Clean the house"
        least_checkoff_history = test_analytics.get_least_checkoff_history()
        assert(least_checkoff_history == "Clean the house")
        
        test_analytics.get_habits_with_same_periodicity("daily")
        
        test_analytics.get_history_of_checkoffs_time_range()

        test_analytics.get_archived_habits()
        
        
    def teardown_method(self):
        """This method runs after the main testing has concluded.
        All files that had been created upon startup are removed, creating
        a completely clean slate.
        """
        
        os.remove("Habits/clean_the_house.json")
        os.remove("Habits/do_the_laundry.json")
        os.remove("Habits/go_to_the_gym.json")
        os.remove("Habits/message_a_friend.json")
        os.remove("Habits/writing_in_a_journal.json")