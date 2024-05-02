from copy import deepcopy
from tqdm.contrib.concurrent import process_map
#from tiebreakers import tiebreakers
import csv
import itertools
import json
import random
import updateTeams
import updateGames

#TODO: Implement tiebreakers

def initCount():
    count = {}
    teamList = updateTeams.teamList
    for div in teamList:
        for team in teamList[div]:
            count.update({team:0})
    return count

def teamUpdate(match, data):
    home = data[match["home"]]
    away = data[match["away"]]
    home_win = match["home_win"]
    [home, away] = updateTeams.update_record("ovr_W/L", home, away, home_win)
    #[home, away] = updateTeams.update_intdiv(home, away, home_win)
    #[home, away] = updateTeams.update_h2h(home, away, home_win)
    [home, away] = updateTeams.update_GP(home, away)
    [home, away] = updateTeams.update_avg(home, away)
    return [home, away]

def fillSlots(avg, slots, data):
    for i in avg:
        if slots[0] == "" and data[i]["division"][1:] == "LE":
            slots[0] = i
        elif slots[1] == "" and data[i]["division"][1:] == "LC":
            slots[1] = i
        elif slots[2] == "" and data[i]["division"][1:] == "LW":
            slots[2] = i
        elif slots[3] == "":
            slots[3] = i
        elif slots[4] == "":
            slots[4] = i
        elif slots[5] == "":
            slots[5] = i
    return slots

def lazytiebreakers(avg):
    flipped = {}
    for key, value in avg.items():
        if value not in flipped:
            flipped[value] = [key]
        else:
            flipped[value].append(key)
    for value in flipped:
        if len(flipped[value]) >= 1:
            for team in flipped[value]:
                avg[team] = avg[team] + (random.random()/163)
    return avg

def postseason(data):
    ALslots = ["","","","","",""] #ALE,ALC,ALW,WC1,WC2,WC3
    NLslots = ["","","","","",""] #NLE,NLC,NLW,WC1,WC2,WC3
    ALavg = {}
    NLavg = {}
    for team in data:
        if data[team]["division"][0] == "A":
            ALavg.update({team:data[team]["avg"]})
        else:
            NLavg.update({team:data[team]["avg"]})
    ALavg = lazytiebreakers(ALavg)
    NLavg = lazytiebreakers(NLavg)
    ALavg = dict(sorted(ALavg.items(), reverse=True, key=lambda item: item[1]))
    NLavg = dict(sorted(NLavg.items(), reverse=True, key=lambda item: item[1]))
    return fillSlots(ALavg,ALslots,data)+fillSlots(NLavg,NLslots,data)

def simulateSeason(teamData,igameData, i):
    iteamData = deepcopy(teamData)
    random.seed(i)
    for gameID in igameData:
        game = igameData[gameID]
        if not game["complete"]:
            odds = (iteamData[game["home"]]["Pavg"] + (1-iteamData[game["away"]]["Pavg"]))/2
            if random.random() < odds:
                gameResult = updateGames.simUpdate(game,0,1)
            else:
                gameResult = updateGames.simUpdate(game,1,0)
            [iteamData[game["home"]], iteamData[game["away"]]] = teamUpdate(gameResult,iteamData)
    return postseason(iteamData)

def simulate(iterations):
    count = initCount()
    with open("games2024.json",'r+') as gamesFile:
        gameData = json.load(gamesFile)
    with open("teams2024.json",'r+') as teamFile:
        teamData = json.load(teamFile)
        for team in teamData:
            del teamData[team]["h2h"]
            del teamData[team]["intradiv_W/L"]
            del teamData[team]["interdiv_W/L"]

    psteams = process_map(simulateSeason, itertools.repeat(teamData), itertools.repeat(gameData), range(iterations), max_workers=8, chunksize=25, total=iterations)
    
    for i in psteams:
        for team in i:
            count[team] = count[team] + 1/iterations
    
    for team in count:
        x = count[team]*100
        print(team+": "+"{:.2f}".format(x)+"%")
    with open('simOutput.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for i in count:
            rdiff = teamData[i]["RS/RA"]
            writer.writerow([i,teamData[i]["ovr_W/L"][0],teamData[i]["ovr_W/L"][1],count[i],rdiff[0]-rdiff[1]])
    updateMulti(gameData, count)
    return

def updateMulti(gameData, count):
    dlist = []
    for match in gameData:
        if not gameData[match]["date"] in dlist and gameData[match]["complete"]:
            dlist.append(gameData[match]["date"])
    with open("multiSimOutput.csv", "r", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            date = row[0]
            if date in dlist:
                dlist.remove(date)
        for match in gameData:
            if gameData[match]["date"] in dlist and not gameData[match]["complete"]:
                dlist.remove(gameData[match]["date"])
    if len(dlist) == 1:
        with open('multiSimOutput.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([dlist[0]]+list(count.values()))
        print("multiSimOutput.csv successfully updated.")
    elif not len(dlist) == 0:
        print("More than one day has passed since last multiSim update. Please run full multiSim.")
    return

if __name__ == '__main__':
    simulate(250000)