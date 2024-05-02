# BasedBall

This is a (likely overcomplicated) set of scripts to simulate the remaining games in a MLB season and calculate the odds of the teams reaching the postseason. The main .py file is updateGames.py which has a CLI to add game results and run the simulation.


## File Descriptions
- MLB Tracker.xlsx: this is the main way to visualize the simulation output. It has two tabs, one with standing tables and magic number grid, the other with graphs of postseason odds over time. It automatically updates through query blackmagic that even I don't fully understand yet. There are hidden tabs where the query data ends up, don't worry about them. The .xlsx file needs to be in the same directory as the .csv files. It also pulls from mlb.com/standings to let you know if the simulation is out of date or a team's run differential is incorrect. "Error" next to a teams row in the standings indicate a game is missing or has an incorrect score. Click on "Refresh All" in excel's data tab to update queries.
- updateGames.py is how you add game results to the database (games202x.json) you type the game ID (month, day, home team) such as "501TOR" or you can just type the date "501" to do them all sequentially (you can type x instead of the score to skip a game or type p to change the date in case of a rain out)
- updateTeams.py: updates the standings database (teams202x.json). It runs automatically whenever you input a game result through updateGames.py
- simulate.py is the "turn my computer into a space heater" function. Running it outputs the csv files that are read by the excel file. It is multithreaded which is something I have only just now learned how to do so you might want to tweak the max_workers parameter for your system.
- multiSim.py runs the simulation for every day in the past to calculate historical odds for the graphs. You don't need to run it nor do I recommend it as it can take hours to run. simulate.py automatically will keep it updated as long as you run it at least once with a completed day's worth of games.
- games202x.json: saves game information including: home and away teams, score, and date
- teams202x.json: saves team win/loss record including intradivision, interdivision, h2h, avg, etc.
- simOutput.csv: The csv required to fill out the standings tab in the excel sheet.
- multiSimOutput.csv: The csv required to populate the graphs in the excel file.
- initJSON.py will read from schedule202x.csv file and initialize games202x.json for a fresh season. (Warning, this will erase the entire season's game results if run!)
- schedule202x: this is just a nicely formatted csv file with the schedule for the MLB season. Modified from: https://www.mlbschedulegrid.com/downloads
