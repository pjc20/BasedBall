import csv
import json
import os
from datetime import datetime

data = {}

def initJSON():
    os.system('cls')
    with open('schedule2024.csv', newline='') as schedFile:
        schedReader = csv.reader(schedFile, delimiter=' ', quotechar='|')
        for row in schedReader:
            list = row[0].split(",")
            date = datetime.strptime(list[0], "%Y-%m-%d")
            for match in list[1:]:
                if match[3] == "2":
                    id = (datetime.strftime(date, "%m%d")+match[4:])[1:]+"1"
                    addEntry(match, id, list[0])
                    id = (datetime.strftime(date, "%m%d")+match[4:])[1:]+"2"
                    addEntry(match, id, list[0])
                else:
                    id = (datetime.strftime(date, "%m%d")+match[4:])[1:]
                    addEntry(match, id, list[0])


    with open("games2024.json", "w") as outfile:
        json.dump(data, outfile, indent = 4)
    input("JSON itialization sucessful. Press enter to continue:")

def addEntry(match, id, date):
    data.update({id: {"id": id,
                      "date": date,
                      "complete": False,
                      "home": match[4:],
                      "away": match[:3]}})
    return