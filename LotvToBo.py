import json
from difflib import get_close_matches
import sys

def isSpace(char):
    return char == " " or char == "\t" or char == "\f" or char == "\v"

def getNextChar(line, k):
    while k < len(line) and isSpace(line[k]):
        k += 1
    return k

def getNextSpace(line, k):
    while k < len(line) and not isSpace(line[k]):
        k += 1
    return k

def newparserLotz(lotv):
    parser = []
    for line in lotv.split("\n"):
        parser.append([])
        k = 0
        while k < len(line):
            k  = getNextChar(line, k)
            k1 = getNextSpace(line, k)

            parser[-1].append(line[k:k1])

            k = k1
    return parser

def openJson():
    data = {}
    with open("output.json", 'r') as json_file:
        data = json.load(json_file)
    return data

def getlist_data():
    data = openJson()
    dictkey = {}
    rl = []

    for key, value in data.items():
        name = value["name"]
        name = name.replace("_", "")
        rl.append(name)
        dictkey[name] = key
    return rl, dictkey

def parsePureData(data):
    results = []

    for l in data:
        if len(l) < 2:
            continue

        commands = ("".join(l[2:])).split(",")

        for command in commands:
            if len(command) < 2:
                continue

            add_chrono = False
            rep        = 1

            itDeb = command.find("(")
            itEnd = command.find(")")

            if itDeb != -1 and itEnd != -1:
                if len(get_close_matches(command[itDeb + 1:itEnd], ["ChronoBoost"])) > 0:
                    command = command[:itDeb]
                    add_chrono = True

            if len(command) and command[-2] == 'x' and command[-1].isdigit():
                rep = int(command[-1])
                command = command[0:-2]

            for _ in range(rep):
                results.append([l[0], l[1], command])
            if add_chrono:
                results.append([l[0], l[1], "ChronoBoost"])



    return results



import tkinter as tk
from tkinter import scrolledtext

def execute_code(code, filename):
    # Function to be called when the "Execute" button is clicked
    l               = parsePureData(newparserLotz(code))
    words, dictkey  = getlist_data()

    for d in l:
        close_matches = get_close_matches(d[2], words)

        print(d)
        if len(close_matches) == 0:
            print("Error, can't understand what's mean :", d[2])
            sys.exit()

        d[2] = dictkey[close_matches[0]]


    with open(filename + ".csv", "w") as f:
        for d in l:
            print(d)
            f.write(",".join(d) + "\n")

# Function to get the content of the InputBox and InputLine and call the execute_code function
def execute():
    code = input_box.get("1.0", "end-1c")  # Get the content of the InputBox
    filename = input_line.get()             # Get the content of the InputLine
    execute_code(code, filename)            # Call the execute_code function with the data

if __name__ == "__main__":
    # Create the main window
    window = tk.Tk()
    window.title("Graphical Interface")

    input_box_label = tk.Label(window, text="The build order:")
    input_box_label.pack()

    # Create the InputBox (ScrolledText for a text area with scrolling)
    input_box = scrolledtext.ScrolledText(window, wrap=tk.WORD)
    input_box.pack(fill=tk.BOTH, expand=True, pady=10)

    # Create the InputLine (Entry for a simple text field)
    input_line_label = tk.Label(window, text="Filename:")
    input_line_label.pack()
    input_line = tk.Entry(window, width=40)
    input_line.pack(pady=10)

    # Create the "Execute" button
    execute_button = tk.Button(window, text="Execute", command=execute)
    execute_button.pack()

    # Start the main loop
    window.mainloop()
