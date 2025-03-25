import csv
import random
from tqdm import tqdm

pyth = {
    "NYY": 0.598158942914082,
    "BAL": 0.558385461999626,
    "KCR": 0.565703730309405,
    "CLE": 0.565183418742706,
    "HOU": 0.565234759253964,
    "DET": 0.530183930476651,
    "LAD": 0.601041066160263,
    "SDP": 0.563423696375496,
    "ATL": 0.573586477869142,
    "PHI": 0.577197606904705,
    "MIL": 0.595035530893644,
    "NYM": 0.548350599135579
}

count = {
    "NYY": 0,
    "BAL": 0,
    "KCR": 0,
    "CLE": 0,
    "HOU": 0,
    "DET": 0,
    "LAD": 0,
    "SDP": 0,
    "ATL": 0,
    "PHI": 0,
    "MIL": 0,
    "NYM": 0
}

def simulateSeries(series):
    t1Wins = series[2]
    t2Wins = series[3]
    pMatchup = (pyth[series[0]]+(1-pyth[series[1]]))/2
    while(True):
        rand = random.random()
        if rand < pMatchup:
            t1Wins += 1
        else:
            t2Wins += 1
        if t1Wins >= series[-1]:
            return series[0]
        elif t2Wins >= series[-1]:
            return series[1]

def simulatePostseason():
    WS = ["NYY","LAD",0,2,5]
    return simulateSeries(WS)

iterations = 1000000
for i in tqdm(range(iterations)):
    champion = simulatePostseason()
    count[champion] = count[champion] + 1/iterations

with open('simPostseason.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for key, value in count.items():
        writer.writerow([key, value])

print(count)
