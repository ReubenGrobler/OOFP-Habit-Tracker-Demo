# Habit Tracker v 1.0.0
## Developed by Reuben Grobler

Ever needed a lightweight, yet easy to use habit tracking application? This application allows you to dynamically track your habits via an intuitive check-off system, all via the use of a command-line input!

*This is a demo application developed for the __Object Oriented and Functional Programming with Python__ course for __IU University of Applied Sciences.__*

## How to Install the Application

To install this application, it is first necessary to install Python version 3.12 or higher. Additionally, Pip needs to be installed as well, however this is usually automatically done if you installed Python from [python.org](https://www.python.org/).
If necessary, a guide to install Pip can be found [here](https://pip.pypa.io/en/stable/installation/).

- First, install the latest version of the Questionary library (any version not older than 2.1.0 should work). This can be done by opening your terminal/command line and typing in the following:

```pip install questionary```

- Afterwards, make sure to install the latest version of Pytest as well (any version not older than 8.3.5 should work). This can be done in a similar manner to installing Questionary by opening up your terminal/command line and typing in:

```pip install -U pytest```

**NOTE:** Although installing Questionary isn't strictly necessary due to it being included with the application, installing the library yourself prevents any issues from possibly occurring. As such, it is highly recommended to install Questionary yourself via these instructions.

- Once you have installed these dependencies, type in the following to verify your installation within your terminal/command line:

```pip list```

- You should see *Questionary* and *Pytest* amongst your list. If you do, congratulations! You have installed everything correctly.

- Lastly, copy the contents of the *HabitTrackerApp* directory to any directory on your computer. Make sure that all files and directories are within the same directory.

Once this has all be done, you are ready to run the program!

## How to Run the Application

1. Open your terminal/command line
2. Navigate to the file path that you have stored the application directory at. An example of a file path could be something like:

```C:\Users\JohnDoe\HabitTrackerApp\```

3. Type in the following:

```python main.py```

4. Assuming your path looks something like `C:\Users\JohnDoe\HabitTrackingApp> python main.py`, press Enter.

The application should now start and prompt you with various selections!

## How to Use the Application

Within the program, there is a **Help** section entirely dedicated to explaining what each option does. While the names in and of themselves should be relatively self-explanatory, the **Help** section provides more than enough insight to use the program.

## How to Test the Application

To run a simple test on the application via Pytest, follow the run instructions up until step 3.
- Instead of entering ```python main.py```, enter ```pytest . -s```. Press enter.
- You will be prompted with a few inputs as the test goes on, namely:
    - The test to replace habit data with custom values
    - A test to check-off a test habit specifically created for this test
    - An input asking for start and end dates to search for all check-offs for a habit between those two dates
- You are free to insert whatever values you wish during these tests.
- Upon completion, you will be notified of the test passing and are free to run the application if you so desire. 