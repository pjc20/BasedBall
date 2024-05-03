# Import necessary modules
import json

# Define class ManageTeams to manage and msnipulate team data
# I will include a function to modify team names and cities cause lol Oakland

class ManageTeams:

    def __init__(self):
        # Constructor

        # Dictionary of all teams by devision. Used for sorting standings and playoff races.
        teamList = {"ALE":["BAL","BOS","NYY","TBR","TOR"],
            "ALC":["CLE","CHW","DET","KCR","MIN"],
            "ALW":["HOU","LAA","OAK","SEA","TEX"],
            "NLE":["ATL","MIA","NYM","PHI","WSH"],
            "NLC":["CHC","CIN","MIL","PIT","STL"],
            "NLW":["ARI","COL","LAD","SDP","SFG"]}
        
    def updateStandings(self):