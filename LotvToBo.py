import json
from difflib import get_close_matches
import sys


lotv2 = """
  14	  0:18	  Supply Depot x2 (Chrono Boost)	
  15	  0:41	  Barracks
  19	  1:28	  Reaper, Orbital Command
  23	  2:21	  Command Center
  24	  2:28	  Hellion
  26	  2:32	  Supply Depot
  26	  2:35	  Reaper
  28	  2:47	  Starport
  29	  2:53	  Hellion
  32	  3:07	  Barracks Reactor, Refinery
  33	  3:14	  Factory Tech Lab
  33	  3:24	  Starport Tech Lab
  34	  3:35	  Cyclone
  38	  3:43	  Marine x2
  40	  3:49	  Raven
  46	  4:08	  Siege Tank
  52	  4:19	  Supply Depot, Marine x2
  59	  4:45	  Siege Tank
"""

import re

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
            #print(line, getNextChar(line, k))

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
        print(commands)

        for command in commands:
            add_chrono = False
            rep        = 1

            itDeb = command.find("(")
            itEnd = command.find(")")

            if itDeb != -1 and itEnd != -1:
                print(command[itDeb + 1:itEnd], get_close_matches(command[itDeb + 1:itEnd], ["ChronoBoost"])) 
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

l               = parsePureData(newparserLotz(lotv2))
words, dictkey  = getlist_data()

for d in l:
    close_matches = get_close_matches(d[2], words)

    if len(close_matches) == 0:
        print("Error, can't understand what's mean :", d[2])
        sys.exit()

    d[2] = dictkey[close_matches[0]]


filename = input("file name : ")

with open(filename + ".csv", "w") as f:
    for d in l:
        print(d)
        f.write(",".join(d) + "\n")
