import json

def openJson():
    data = None
    with open("output.json", 'r') as json_file:
        data = json.load(json_file)
    return data

def make_data():
    json_data = openJson()

    data = {
            "Terran": {"Buildings": [], "Units": [], "Upgrades": []},
            "Protoss": {"Buildings": [], "Units": [], "Upgrades": []},
            "Zerg": {"Buildings": [], "Units": [], "Upgrades": []},
    }

    for key in json_data.keys():
        name = json_data[key]["name"]

        if json_data[key]["race"] == 'p':
            if json_data[key]["type"] == 'u':
                data["Protoss"]["Units"].append(name)
            elif json_data[key]["type"] == 'b':
                data["Protoss"]["Buildings"].append(name)
            elif json_data[key]["type"] == 'p':
                data["Protoss"]["Upgrades"].append(name)
        elif json_data[key]["race"] == 't':
            if json_data[key]["type"] == 'u':
                data["Terran"]["Units"].append(name)
            elif json_data[key]["type"] == 'b':
                data["Terran"]["Buildings"].append(name)
            elif json_data[key]["type"] == 'p':
                data["Terran"]["Upgrades"].append(name)
        elif json_data[key]["race"] == 'z':
            if json_data[key]["type"] == 'u':
                data["Zerg"]["Units"].append(name)
            elif json_data[key]["type"] == 'b':
                data["Zerg"]["Buildings"].append(name)
            elif json_data[key]["type"] == 'p':
                data["Zerg"]["Upgrades"].append(name)
    return data

