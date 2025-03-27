#Name: Joshua Kyle Finlayson
#Student Number: 1069148

# Import the necessary module(s).
import tkinter, tkinter.messagebox, json
import tkinter.ttk

#Global constant
DATA_FILE_PATH = "data.txt"


class ProgramGUI:
    def __init__(self, file_path):
        # This is the constructor of the class.
        # It is responsible for loading the data from the text file and creating the user interface.
        #Create root TK window
        self.root = tkinter.Tk()
        self.root.title("Game Browser")


        #Get file Data
        self.file_path = file_path
        try:
            with open(self.file_path, "r") as file:
                #If the file is empty
                self.data = json.load(file)
                file.close()
        except FileNotFoundError:
            #If the file does not exist
            self.warning_box(f"The storage file {self.file_path} does not exist.")
        except json.decoder.JSONDecodeError:
            #If the file is empty
            self.warning_box(f"The JSON code in {self.file_path} was invalid")
        except NotADirectoryError:
            self.error_box(f"the directory for {self.file_path} is invalid")
            return
        except PermissionError:
           self.error_box(f"The program does not have the proper permissions to access {self.file_path}")
           return
        except EOFError:
            self.error_box(f"{self.file_path} ends early likely due to incorrect JSON syntax")
            return
        
        if self.data == []:
            self.warning_box(f"The file {self.file_path} was empty")


        #Create the rest of the TK window stuff
        #Title
        self.title_label = tkinter.Label(self.root, 
                                         text="Boardgame Search", 
                                         fg="blue",
                                         font = ('Aptos', 16, 'bold'),
                                         anchor="n")
        self.title_label.pack(side="top", anchor="center")

        #Number of players frame
        self.num_players_frame = tkinter.ttk.Frame(self.root)
        self.num_players_frame.pack()
        self.num_of_players_label = tkinter.Label(self.num_players_frame, text = "Number of players: ", justify="right", width=18)
        self.num_of_players_label.pack(side="left")
        self.num_players_entry = tkinter.Entry(self.num_players_frame, width=4)
        self.num_players_entry.pack(side="right", padx=5)

        #Time available frame
        self.time_available_frame = tkinter.ttk.Frame(self.root)
        self.time_available_frame.pack()
        self.time_available_label = tkinter.Label(self.time_available_frame, text="Time available (mins):", justify="right", width=18)
        self.time_available_label.pack(side="left")
        self.time_available_entry = tkinter.Entry(self.time_available_frame, width=4)
        self.time_available_entry.pack(side="right", padx=5)

        #Youngest player frame
        self.youngest_player_frame = tkinter.ttk.Frame(self.root)
        self.youngest_player_frame.pack()
        self.youngest_player_label = tkinter.Label(self.youngest_player_frame, text="Age of youngest player:", justify="right", width=18)
        self.youngest_player_label.pack(side="left")
        self.youngest_player_entry = tkinter.Entry(self.youngest_player_frame, width=4)
        self.youngest_player_entry.pack(side="right", padx=5)

        #Button
        self.search_button = tkinter.Button(self.root, text="Search", command=self.search, width=10)
        self.search_button.pack(side="top")

        #Search Results frame
        self.search_results_title = tkinter.Label(self.root, text="Search Results", fg="blue", font=('Aptos', 16, 'bold'))
        self.search_results_title.pack(side="top", pady=(20, 0))

        #Inner search reuslts frame for buttons
        self.search_results_frame = tkinter.ttk.Frame(self.root)
        self.search_results_frame.pack(fill="both", expand=True)
        temp_label = tkinter.Label(self.search_results_frame, text="Form not submitted.", state='disabled')
        temp_label.pack(side="top")

        self.root.mainloop()
    
    def error_box(self, error_message : str):
        tkinter.messagebox.showerror("Error", "ERROR: " + error_message)
    
    def warning_box(self, warning_message : str):
        tkinter.messagebox.showwarning("Warning", "WARNING: " + warning_message)

    def search(self):
        # This method displays buttons containing the names of boardgames that meet the criteria specified in the form.
        num_players = self.num_players_entry.get()
        time_available = self.time_available_entry.get()
        youngest = self.youngest_player_entry.get()

        #error checking
        if num_players == "":
            try:
                if int(num_players) != float(num_players): raise TypeError
                num_players = int(num_players)
                if num_players <= 0: raise ValueError
            except:
                self.error_box(f"The number of players playing need to be a whole number greater than zero")
                return
        
        if time_available == "":
            try:
                if int(time_available) != float(time_available): raise TypeError
                time_available = int(time_available)
                if time_available <= 0: raise ValueError
            except:
                self.error_box(f"The time avilable needs to be a whole number greater than zero")
                return
        
        if youngest == "":
            try:
                if int(youngest) != float(youngest): raise TypeError
                youngest = int(youngest)
                if youngest < 0: raise ValueError
            except:
                self.error_box(f"The youngest player's age needs to be a whole positive number")
                return
        
        #Now do search stuff
        self.search_results = []
        for i, game in enumerate(self.data):
            if ((num_players != "" and game['players'][0] <= num_players <= game['players'][1]) and
                (time_available != "" and game['playtime'][0] <= time_available <= game['playtime'][1]) and
                (youngest != "" and game['min_age'] <= youngest)):
                self.search_results += [i]
        
        #remove current buttons
        for widget in self.search_results_frame.winfo_children():
            widget.destroy()

        #Display search results
        if not self.search_results:
            temp = tkinter.Label(self.search_results_frame, text="No results found", status='disabled')
            temp.pack(side="top")
            return
        
        temp = tkinter.Label(self.search_results_frame, text=f"{len(self.search_results)} out of {len(self.data)} matches", status='disabled')
        temp.pack(side="top")

        for i in self.search_results:
            temp = tkinter.Button(self.search_results_frame, text=self.data[i]['name'], command=lambda x=i: self.show_details(x), width=40)
            temp.pack(side="top")

    def show_details(self, index):
        # This method for displays all of the details of the boardgame in a messagebox.
        game = self.data[index]
        out = ""
        out += f"{game['name']} ({game['year']})\n"
        out += f"{game['desc']}\n\n"
        out += f"Players: {game['players'][0]}-{game['players'][1]}\n"
        out += f"Playtime: {game['playtime'][0]}-{game['playtime'][1]} minutes\n"
        out += f"Minimum age: {game['min_age']}+\n"
        out += f"Complexity: {game['complexity']}/5"

        if not out:
            self.error_box(f"Could not find game data for index {index}")
            return
        tkinter.messagebox.showinfo(game['name'], out)


#Code to run in Sequence

# Create an object of the ProgramGUI class to begin the program.
ProgramGUI(DATA_FILE_PATH)

# If you have been paid to write this program, please delete this comment.