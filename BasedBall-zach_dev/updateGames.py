import json
import os
import simulate
from datetime import datetime, timedelta
from updateTeams import updateTeams

def updateGames():
    while (True):
        os.system('cls')
        with open("games2024.json",'r+') as gamesFile:
            data = json.load(gamesFile)
            print('Enter date [MDD] or game ID to update, all to show incomplete to date, s to run simulation, x to exit:')
            cmd = input()
            date = "2024-0"+cmd[:1]+"-"+cmd[1:3]

            if cmd == "all":
                today = datetime.today()-timedelta(hours=6)
                for match in data:
                    if datetime.strptime(data[match]["date"], "%Y-%m-%d") <= today and not data[match]["complete"]:
                        print(data[match]["id"])
                input("Press enter to continue")
            elif cmd == "s":
                iterations = int(input("Enter number of iterations: "))
                simulate.simulate(iterations)
                input("Simulation complete. Press enter to continue")
            elif len(cmd) == 3:
                for match in data:
                    if data[match]["complete"] or not data[match]["date"] == date:
                        continue
                    [a, h] = getScore(data[match])
                    if a == "-1":
                        continue
                    elif a == "-2":
                        data[match]["date"] = h
                    else:
                        data[match] = update(data[match], a, h)
            elif 6 <= len(cmd) <= 7:
                [a, h] = getScore(data[cmd])
                if a == "-2":
                        data[cmd]["date"] = h
                elif not a == "-1":
                    data[cmd] = update(data[cmd], a, h)
            elif cmd == "x":
                break

            gamesFile.seek(0)
            json.dump(data, gamesFile, indent = 4)

        updateTeams()
        print("Update successful.")

def update(match, a, h):
    win = int(h) > int(a)
    match.update({"home_score": h,
                  "away_score": a,
                  "home_win": win})
    match["complete"] = True
    return match

def simUpdate(match, a, h):
    win = int(h) > int(a)
    match.update({"home_score": h,
                  "away_score": a,
                  "home_win": win})
    return match

def getScore(match):
    os.system('cls')
    print("Game ID: "+match["id"])
    print("Enter game score or type x to cancel, p to postpone:")
    aScore = input(match["away"]+": ")
    if aScore == "x": return ["-1","-1"]
    elif aScore == "p":
        newDate = input("Input new game date:")
        return ["-2",newDate]
    hScore = input(match["home"]+": ")
    if hScore == "x": return ["-1","-1"]
    return [aScore,hScore]

if __name__ == '__main__':
    updateGames()