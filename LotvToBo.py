import json
from difflib import get_close_matches
import sys

def isSpace(char):
    return char == " " or char == "\t" or char == "\f" or char == "\v" or char == ":"

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
        dictkey[name] = [value["name"], value["race"], value["type"]]
    return rl, dictkey

def parsePureData(data):
    results = []

    for l in data:
        if len(l) < 4:
            continue

        commands = ("".join(l[3:])).split(",")

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
                results.append([l[0], l[1], l[2], command])
            if add_chrono:
                results.append([l[0], l[1], l[2], "ChronoBoost"])



    return results

def execute_code(code):
    l               = parsePureData(newparserLotz(code))
    words, dictkey  = getlist_data()

    for d in l:
        close_matches = get_close_matches(d[3], words)

        #print(d)
        if len(close_matches) == 0:
            print("Error, can't understand what's mean :", d[2])
        else:
            d[3] = dictkey[close_matches[0]]

    return l

# Function to get the content of the InputBox and InputLine and call the execute_code function
#def execute():
#    code = input_box.get("1.0", "end-1c")  # Get the content of the InputBox
#    filename = input_line.get()             # Get the content of the InputLine
#    execute_code(code, filename)            # Call the execute_code function with the data
