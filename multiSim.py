import csv
from datetime import datetime
import itertools
from tqdm.contrib.concurrent import process_map
import json
import simulate as sim
import updateTeams

def prune(data,sel):
    day = datetime.strptime(sel, "%Y-%m-%d")
    for match in data:
        if datetime.strptime(data[match]["date"], "%Y-%m-%d") > day:
            data[match]["complete"] = False
    print(sel)
    return data

def daySim(day,iterations):
    count = sim.initCount()
    with open("games2024.json",'r+') as gamesFile:
        gameData = prune(json.load(gamesFile),day)
    teamData = updateTeams.initTeams()
    for id in gameData:
        match = gameData[id]
        if not match["complete"]:
            continue
        [teamData[match["home"]], teamData[match["away"]]] = updateTeams.update(match)
                
    psteams = process_map(sim.simulateSeason, itertools.repeat(teamData), itertools.repeat(gameData), range(iterations), max_workers=16, chunksize=25, total=iterations)
    
    for i in psteams:
        for team in i:
            count[team] = count[team] + 1/iterations
    return count

def init_dateList():
    list = []
    with open("games2024.json",'r+') as gamesFile:
        gameData = json.load(gamesFile)
    for match in gameData:
        if not gameData[match]["date"] in list and gameData[match]["complete"]:
            list.append(gameData[match]["date"])
    return list

def multiSim():
    dateList=init_dateList()
    counts = {}
    for date in dateList:
        counts.update({date:daySim(date,250000)})
    with open('multiSimOutput.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([""]+list(counts[dateList[0]]))
        for i in counts:
            writer.writerow([i]+list(counts[i].values()))
    return

if __name__ == '__main__':
    multiSim()