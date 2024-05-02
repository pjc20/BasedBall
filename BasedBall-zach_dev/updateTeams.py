import json

teamData = {}
teamList = {"ALE":["BAL","BOS","NYY","TBR","TOR"],
            "ALC":["CLE","CHW","DET","KCR","MIN"],
            "ALW":["HOU","LAA","OAK","SEA","TEX"],
            "NLE":["ATL","MIA","NYM","PHI","WSH"],
            "NLC":["CHC","CIN","MIL","PIT","STL"],
            "NLW":["ARI","COL","LAD","SDP","SFG"]}

def updateTeams():
    initTeams()

    with open("games2024.json",'r+') as gamesFile:
        gameData = json.load(gamesFile)

        for id in gameData:
            match = gameData[id]
            if not match["complete"]:
                continue
            [teamData[match["home"]], teamData[match["away"]]] = update(match)

        #magicNumbers()
        
        #for team in teamData:
        #    print(team+": "+str(teamData[team]["Pavg"]))

    with open("teams2024.json", "w") as outfile:
        json.dump(teamData, outfile, indent = 4)

def h2hInit(curTeam):
    h2hDict = {}
    for div in teamList:
        for team in teamList[div]:
            if not team == curTeam:
                h2hDict.update({team:[0,0]})
    return h2hDict


def magicInit(league, curTeam):
    magicDict = {}
    for div in teamList:
        if div[0] == league:
            for team in teamList[div]:
                if not team == curTeam:
                    magicDict.update({team:0})
    return magicDict

def initTeams():
    for div in teamList:
        for team in teamList[div]:
            teamData.update({team: {}})
            teamData[team].update({"team": team,
                                   "division": div,
                                   "ovr_W/L": [0,0],
                                   "intradiv_W/L": [0,0],
                                   "interdiv_W/L": [0,0],
                                   "h2h": h2hInit(team),
                                   "GP/GR": [0,162],
                                   "RS/RA": [0,0],
                                   "avg": float(0),
                                   "Pavg": float(0)#,
                                   #"magic": magicInit(div[0], team)
                                   })
    return teamData

def pythagorean(RS,RA,GP):
    ratio = GP/162
    try:
        Pavg = 1/(1+(RA/RS)**1.83)
    except ZeroDivisionError:
        Pavg = 0
    Pavg = (ratio*Pavg)+((1-ratio)*0.5)
    return float(Pavg)

def update_record(key, home, away, home_win):
    if home_win:
        home[key][0] = home[key][0] + 1
        away[key][1] = away[key][1] + 1
    else:
        home[key][1] = home[key][1] + 1
        away[key][0] = away[key][0] + 1
    return [home, away]

def update_intdiv(home, away, home_win):
    if home["division"] == away["division"]:
        [home, away] = update_record("interdiv_W/L", home, away, home_win)
    else:
        [home, away] = update_record("intradiv_W/L", home, away, home_win)
    return [home, away]

def update_h2h(home, away, home_win):
    if home_win:
        home["h2h"][away["team"]][0] = home["h2h"][away["team"]][0] + 1
        away["h2h"][home["team"]][1] = away["h2h"][home["team"]][1] + 1
    else:
        home["h2h"][away["team"]][1] = home["h2h"][away["team"]][1] + 1
        away["h2h"][home["team"]][0] = away["h2h"][home["team"]][0] + 1
    return [home, away]

def update_GP(home, away):
    home["GP/GR"] = [home["GP/GR"][0]+1,home["GP/GR"][1]-1]
    away["GP/GR"] = [away["GP/GR"][0]+1,away["GP/GR"][1]-1]
    return [home, away]

def update_rdiff(home, away, home_RS, away_RS):
    home["RS/RA"] = [home["RS/RA"][0]+home_RS, home["RS/RA"][1]+away_RS]
    away["RS/RA"] = [away["RS/RA"][0]+away_RS, away["RS/RA"][1]+home_RS]
    return [home, away]

def update_avg(home, away):
    home["avg"] = float(home["ovr_W/L"][0]/home["GP/GR"][0])
    away["avg"] = float(away["ovr_W/L"][0]/away["GP/GR"][0])
    return [home, away]

def update_Pavg(home, away):
    home["Pavg"] = pythagorean(home["RS/RA"][0],home["RS/RA"][1],home["GP/GR"][0])
    away["Pavg"] = pythagorean(away["RS/RA"][0],away["RS/RA"][1],home["GP/GR"][0])
    return [home, away]

def update(match):
    home = teamData[match["home"]]
    away = teamData[match["away"]]
    home_win = match["home_win"]
    [home, away] = update_record("ovr_W/L", home, away, home_win)
    [home, away] = update_intdiv(home, away, home_win)
    [home, away] = update_h2h(home, away, home_win)
    [home, away] = update_GP(home, away)
    [home, away] = update_rdiff(home, away, int(match["home_score"]), int(match["away_score"]))
    [home, away] = update_avg(home, away)
    [home, away] = update_Pavg(home, away)
    return [home, away]

def magicNumbers():
    for teamA in teamData:
        for teamB in teamData[teamA]["magic"]:
            if teamA == teamB:
                continue
            magic = 163 - teamData[teamA]["ovr_W/L"][0] - teamData[teamB]["ovr_W/L"][1]
            teamData[teamA]["magic"][teamB] = magic
    return

if __name__ == '__main__':
    updateTeams()