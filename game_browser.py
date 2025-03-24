#Name: Joshua Kyle Finlayson
#Student Number: 1069148

# Import the necessary module(s).
import tkinter, tkinter.messagebox, json

#global variables
global DATA_FILE_PATH
DATA_FILE_PATH = "data.txt"



class ProgramGUI:

    def __init__(self):
        # This is the constructor of the class.
        # It is responsible for loading the data from the text file and creating the user interface.
        # See the "Constructor of the GUI Class of game_browser.py" section of the assignment brief.
        pass



    def search(self):
        # This method displays buttons containing the names of boardgames that meet the criteria specified in the form.
        # See Point 1 of the "Methods in the GUI class of game_browser.py" section of the assignment brief.
        pass



    def show_details(self, index):
        # This method for displays all of the details of the boardgame in a messagebox.
        # See Point 2 of the "Methods in the GUI class of game_browser.py" section of the assignment brief.
        pass


#Code to run in Sequence

#copied this over from admin.py
# Here is where you attempt to open data.txt and read the data into a "data" variable.
# If the file does not exist or does not contain JSON data, set "data" to an empty list instead.
data : list = []
try:
    #Create the file if it doesn't exist
    open(DATA_FILE_PATH, "x")
except:
    with open(DATA_FILE_PATH, "r") as file:
        #If the file is not empty
        for i in file.readlines():
            data += [json.loads(i)]
        file.close()

# Create an object of the ProgramGUI class to begin the program.
gui = ProgramGUI()




# If you have been paid to write this program, please delete this comment.
