# Import necessary modules
import csv
import json
from datetime import datetime

# Define a class MLBSchedule that manages MLB schedules

class MLBSchedule:

    def __init__(self, scheduleFile):
        ''' 
            scheduleFile: Takes in an official csv file containing MLB schedule data; 
            Official Source: https://www.mlbschedulegrid.com/downloads
            Reformated to include away/home data
        '''

        self.scheduleFile = scheduleFile
        self.data = {}


    def importSchedule(self):
        ''' 
            Takes in scheduleFile, imports, and returns JSON equivalent 
        '''
        
        with open(self.scheduleFile, newline='') as schedFile:
            # Opens csv file, stores in schedReader
            schedReader = csv.reader(schedFile, delimiter=' ', quotechar='|')

            # Defines game ID based on scheduled date (for example, 501NYY = 
            # Yankees game on May 1); all games, even postponed, are referred to by schedule date
            # For scheduled double header, adds unique game id number to game 2 (501NYY2)
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

        # Output results in json file
        with open("games2024.json", "w") as outfile:
            json.dump(data, outfile, indent = 4)

MLB_schedule_2024 = MLBSchedule('schedule2024.csv')
