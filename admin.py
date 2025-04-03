#Name: Joshua Kyle Finlayson
#Student Number: 1069148

#Source: all the boardgame data was sourced from:
# (n.d.). BoardGameGeek. https://boardgamegeek.com

# Import the necessary module(s).
#This is an inbuilt module in python that allows python to parse and create JSON data 
# which is a type of organising data based on javascript objects
import json
#This is an inbuilt python module that allows the program 
# to do calculations with regards to time and date
from datetime import datetime

#Global constant
DATA_FILE_PATH = "data.txt"

# This function repeatedly prompts for input until something other than whitespace is entered.
def input_something(prompt : str):
    if prompt.strip() == prompt:
        prompt += "\n> "
    while True:
        inp = input(prompt).strip()
        if not inp:
            print("Sorry, you didn't seem to input anything there. Please try again")
        return inp




# This function repeatedly prompts for input until a float with a minimum of 0 is entered.
def input_int(prompt : str, min_value : int = None, max_value : int = None):
    if min_value and max_value:
        if min_value > max_value:
            raise ValueError(f"max_value must be larger thanor equal to min_value\nmax_value: {max_value} \nmin_value: {min_value}")
    while True:
        inp = input_something(prompt)
        try: 
            if int(inp) != float(inp):
                raise ValueError
            inp = int(inp)
        except ValueError:
            print(f"{inp} is not an integer (a whole number)")
            continue
        if min_value != None and inp < min_value:
            print(f"The input cannot be less than {min_value}")
            continue
        if max_value != None and inp > max_value:
            print(f"The input cannot be more than {max_value}")
            continue
        return inp




# This function repeatedly prompts for input until the user enters two integers with a dash between them.
def input_range(prompt : str):
    if prompt.strip() == prompt:
        prompt += "\n> "
    while True:
        inp = input(prompt).strip()
        if "-" not in inp:
            print("You need to input a range separated with a '-'")
            continue
        if inp.count("-") != 1:
            print("You can only have one '-', so no negative numbers")
            continue
        [num1, num2] = inp.split("-")
        try:
            if int(num1) != float(num1) or int(num2) != float(num2):
                raise ValueError
            num1 = int(num1)
            num2 = int(num2)
        except ValueError:
            print("You must input two integers on either side of the '-'")
            continue
        if num1 <= 0 or num2 <= 0:
            print("You must input positive numbers greater than zero")
            continue
        if num2 < num1:
            print("The second number cannot be smaller than the first number")
            continue
        return [num1, num2]




# This function opens "data.txt" in write mode and writes the data to it in JSON format.
def save_data(data : list, file_path):
    with open(file_path, "w+") as file:
        json.dump(data, file, indent = 1)
        file.close()


# Here is where you attempt to open data.txt and read the data into a "data" variable.
# If the file does not exist or does not contain JSON data, set "data" to an empty list instead.
data : list = []
try:
    with open(DATA_FILE_PATH, "r") as file:
        #If the file is empty
        data = json.load(file)
        file.close()
except FileNotFoundError:
    #If the file does not exist
    print(f"WARNING: The storage file {DATA_FILE_PATH} does not exist.")
except json.decoder.JSONDecodeError:
    #If the file is empty
    print(f"WARNING: The JSON code in {DATA_FILE_PATH} is invalid")
except NotADirectoryError:
    print(f"ERROR: the directory for {DATA_FILE_PATH} is invalid")
    raise NotADirectoryError
except PermissionError:
    print(f"ERROR: The program does not have the proper permissions to access {DATA_FILE_PATH}")
    raise PermissionError
except EOFError:
    print(f"ERROR: {DATA_FILE_PATH} ends early likely due to incorrect JSON syntax")
    raise EOFError
if data == []:
    print(f"WARNING: The file {DATA_FILE_PATH} was empty")


# Print welcome message, then enter the endless loop which prompts the user for a choice.
print("Welcome to Joshua's Boardgame Catalogue Admin Program.")

while True:
    print("\nChoose [a]dd, [l]ist, [s]earch, [v]iew, [d]elete or [q]uit.")
    print("For (s)earch, (v)iew, and (d)elete if you type the specifier after the letter the command runs.\n"
          "(e.g. 's Hello' searches for the 'Hello' term)")
    inp = input('> ').lower().strip()
        
    match inp.split()[0]:
        case 'a':
            #Add new Boardgame
            new_data = {}
            new_data['name'] = input_something("Enter boardgame name: ")
            #The datetime.now().year gets the current year
            #This is becuase a baordgame can't be created in the future
            #but in order to future proof the program the number '2025' cant just be written there
            #and the number '0' is there under the assumption that all games will be from A.D./C.E.
            new_data['year'] = input_int("Enter relase year: ", 0, datetime.now().year)
            new_data['desc'] = input_something("Enter a short description: ")
            new_data['players'] = input_range("Enter number of players as a range e.g. 1-4: ")
            new_data['playtime'] = input_range("Enter playtime in minutes as a range e.g. 15-30: ")
            new_data['min_age'] = input_int("Enter the minimum recommended playing age: ", 0)
            new_data['complexity'] = input_int("Enter complexity(1-5): ", 1, 5)

            data += [new_data]
            print(f"{new_data['name']} added")
            save_data(data, DATA_FILE_PATH)

        case 'l':
            #List all Boardgames
            if not data:
                print("No boardgames saved")
                continue
            print("List of Boardgames")
            for i in range(len(data)):
                print(f"{i +1}) {data[i]['name']} ({data[i]['year']})")

        case 's':
            #Serch for Boardgames through name and description 
            #In the case there is no data
            if not data:
                print("No boardgames saved")
                continue

            #Get search term
            if len(inp.split()) > 1:
                search_term = "".join(inp.split()[1:])
            else:
                search_term = input_something("Enter a search term: ")
            search_term = search_term.lower()

            #Actually search
            search_results : list = []
            for i in range(len(data)):
                if search_term in data[i]['name'].lower() or search_term in data[i]['desc'].lower():
                    search_results.append([i, data[i]])

            #Display results
            if not search_results:
                print("No results found")
                continue

            print("Search results: ")
            for i in range(len(search_results)):
                print(f"{search_results[i][0] + 1}) {search_results[i][1]['name']} ({search_results[i][1]['year']})")

        case 'v':
            #View a specific Boardgame
            #in case there is no data
            if not data:
                print("No boardgames saved")
                continue
            
            #Get num
            num = -1
            if len(inp.split()) > 1:
                str_num = "".join(inp.split()[1:])
                try:
                    num = int(str_num)
                    #Checks if the number was a float
                    if num != float(str_num):
                        #Throw error
                        raise ValueError
                    #check it is in the correct range
                    if len(data) >= num >= 1:
                        num = num - 1
                    else: raise IndexError
                except ValueError:
                    print(f"{str_num} is not an integer. Please try again")
                    num = -1
                except IndexError:
                    print(f"{str_num} is not within the correct range ({1}-{9})")
                    num = -1
            if num == -1:
                num = input("Boardgame number to view: ") - 1
            
            #Display results
            print(f"{data[num]['name']} ({data[num]['year']})")
            print(data[num]['desc'])
            print(f"Players: {data[num]['players'][0]}-{data[num]['players'][1]}")
            print(f"Playtime: {data[num]['playtime'][0]}-{data[num]['playtime'][1]} minutes")
            print(f"Age: {data[num]['min_age']}+")
            print(f"Complexity: {data[num]['complexity']}/5")

        case 'd':
            #Delete a specific Boardgame
            if not data:
                print("No boardgames saved")
                continue

            #Get num
            num = -1
            if len(inp.split()) > 1:
                str_num = "".join(inp.split()[1:])
                try:
                    num = int(str_num)
                    #Checks if the number was a float
                    if num != float(str_num):
                        #Throw error
                        raise ValueError
                    #check it is in the correct range
                    if len(data) >= num >= 1:
                        num = num - 1
                    else: raise IndexError
                except ValueError:
                    print(f"{str_num} is not an integer. Please try again")
                    num = -1
                except IndexError:
                    print(f"{str_num} is not within the correct range ({1}-{9})")
                    num = -1
            if num == -1:
                num = input("Boardgame number to delete: ") - 1
            
            del data[num]
            print("Deleted boardgame")

            save_data(data, DATA_FILE_PATH)

        case 'q':
            #Quit the program
            print("Goodbye")
            input("Press enter to close the program")
            break
        case _: 
            #Else display an error message
            print("Invalid Choice. \nPlease try again.")




# If you have been paid to write this program, please delete this comment