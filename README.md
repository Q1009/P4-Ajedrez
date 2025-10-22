# AJEDREZ
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)  

![AJEDREZ Logo](https://user.oc-static.com/upload/2020/09/22/16007793690358_chess%20club-01.png)  
*(Chess Tournament Management Solution)*

This program aims at managing your local chess club and organize round-robin tournaments. Keep track of players, their ELO, the tournaments' state and much more ! Works offline.
## Get started

> [!WARNING]  
> Make sure you have installed Python version 3.13.3, pip version 25.0.1 and git version 2.39.5.  

- Open any terminal and navigate through your desired directory using the `cd 'directory_name'` command line.

### Requirements

- Start by cloning the GitHub repository by typing the following:  
`git clone https://github.com/Q1009/P4-Ajedrez.git`
- Go in the downloaded directory by typing the following:  
`cd P4-Ajedrez`
- Create your virtual environment by typing the following:  
`python3 -m venv env`

### Installation

- Activate your virtual environment by typing the following:  

    - For Linux Based OS Or Mac-OS.  
`source env/bin/activate`  

    - For Windows With CMD.  
`.\env\Scripts\activate.bat` 

    - For Windows With Power shell.  
`.\env\Scripts\activate.ps1`  

    - For Windows With Unix Like Shells For Example Git Bash CLI.  
`source env/Scripts/activate`

- Install the required packages by typing the following:  
`pip install -r requirements.txt`  

## Running

> [!IMPORTANT]
> Make sure your virtual environment is activated before running the application (see Installation).

1. Start the program
   - From the project root (where main.py is located) run:  
   `python main.py`

   The application will open an interactive console menu.

2. What the interactive menu lets you do
   - Manage players
     - Add, modify or remove players.
     - Players are stored in data/players.json with fields such as surname, name, federation_chess_id, elo, coef_k and games_played.
   - Manage tournaments
     - Create tournaments, subscribe players (by their federation IDs), start tournaments and record match results round by round.
     - Tournament data is stored in data/tournaments.json.
   - Update tournaments
     - If the program was stopped mid-tournament you can resume and continue entering match results.
   - Generate reports
     - The report generator produces HTML files (Jinja2 templates) in the reports/ directory (index.html, players.html, tournaments.html and per-tournament pages).
     - After report generation the program prints a link (clickable in many terminals) to reports/index.html.

3. Entering match results
   - When asked to enter a result for a match, provide one of:
     - 1   (white won)
     - 0   (black won)
     - 0.5 (draw)
   - The application will update players' gamesplayed and recalculate their ELO using each player's K-factor. K-factor rules used by the app:
     - coef_k = 40 for new/active players with few games
     - coef_k = 20 for established players
     - coef_k = 10 for players with rating ≥ 2400

4. Reports
   - Templates are in the templates/ directory (Jinja2).  
   - Generated HTML reports are written to the reports/ directory.
   - To view reports, open reports/index.html in your browser (or click the link printed by the program).

## Data files and templates

- data/players.json
  - Contains all player records. Each record includes:
    - surname, name, date_of_birth, federation_chess_id, elo, coef_k, games_played
- data/tournaments.json
  - Contains tournament records with players, rounds, matches and a matches_history to avoid rematches.
- templates/
  - Jinja2 templates used to render HTML reports.

Keep a backup of the data/ directory before making manual edits.

## Development & Quality checks

- Linting
  - Flake8 can be used to check style. Run the following command line in the terminal:  
  `flake8 main.py --format=html --htmldir=flake8_rapport`
- In the newly created flake8_rapport/ directory, open the index.html file with your web browser to see the report

## Troubleshooting

- JSON errors on load
  - If players.json or tournaments.json is malformed the app will ignore invalid data and start with an empty list; fix the JSON file formatting and restart.
- Missing templates
  - If templates are not present the report generation will fail; ensure the templates/ directory exists and contains the expected .html.j2 files.
- Terminal link not clickable
  - If your terminal does not support clickable links, open reports/index.html manually in your browser.

## Contributing

- Feel free to open issues or PRs on the project's GitHub repository. Describe expected behavior and provide steps to reproduce any bug.

## Author

- **Quentin Tellier** *alias* [@Q1009](https://github.com/Q1009)
