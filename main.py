import requests
import random
import sqlite3
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from fastapi import FastAPI

class Player(BaseModel):
    id: Optional[UUID] = None
    first_name: str
    last_name: str
    ab: int
    runs: int
    hits: int
    doubles: int
    triples: int
    hr: int
    rbi: int
    sb: int
    bb: int
    ba: float
    obp: float
    slg: float


class Team(BaseModel):
    id: Optional[UUID] = None
    location: str
    mascot: str
    division: Optional[str] = None
    stadium: Optional[str] = None
    players: List[Player]


def create_database():
    conn = sqlite3.connect("baseball_teams.db")
    cursor = conn.cursor()

    # Create teams and players tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY,
        team_id TEXT,
        location text,
        mascot TEXT,
        division TEXT,           
        name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        team_id INTEGER,
        first_name TEXT,
        last_name TEXT,
        FOREIGN KEY (team_id) REFERENCES teams(id)
    )
    """)

    conn.commit()
    conn.close()

def insert_data(teams):
    conn = sqlite3.connect("baseball_teams.db")
    cursor = conn.cursor()

    for idx, team in enumerate(teams, start=1):
        # Insert team into teams table
        cursor.execute("INSERT INTO teams (name) VALUES (?)", (f"Team {idx}",))
        team_id = cursor.lastrowid

        # Insert players into players table
        for player in team:
            first_name, last_name = player  # Unpack the first and last names from the player tuple
            print(f"Inserting player: {first_name} {last_name}")  # Debug print
            #print("Type of first_name:", type(first_name))  # Debug print
            #print("Type of last_name:", type(last_name))  # Debug print
            cursor.execute("INSERT INTO players (team_id, first_name, last_name) VALUES (?, ?, ?)", (team_id, first_name, last_name))
            conn.commit()  # Commit after each player insertion

    conn.close()




def get_player_names(url):
    # Send a GET request to the URL
    with open('players.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    
    #response = requests.get(url)
    
 
        # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    #print(soup)
    # Find the elements containing player names
    player_name_elements = soup.find_all('a', class_='p-related-links__link')
    player_names = [name.text.strip() for name in player_name_elements]
    return player_names
        
def create_player(player_names):
    first_names, last_names = zip(*(name.split() for name in player_names))
    first_names = list(first_names)  # Convert to mutable list
    last_names = list(last_names)  # Convert to mutable list
    random.shuffle(first_names)
    random.shuffle(last_names)
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    ab = random.randint(468, 650)
    hits = random.randint(100, 250)
    doubles =  random.randint(0, round(hits/2))
    triples = random.randint(0, doubles-1)
    hr = random.randint(0, (hits-doubles-triples))
    runs = random.randint(hr, 150)
    rbi =  random.randint(hr, hits*4)
    sb =  random.randint(0, 10)
    bb= random.randint(0, 132)
    ba =  hits/ab
    obp = (hits+bb)/ab
    slg = ((hr*4)+(triples*3)+(doubles*2)+(hits-doubles-triples-hr))/ab

    player = Player(first_name=first_name, last_name=last_name, ab=ab, runs=runs, hits=hits, doubles=doubles, triples=triples, hr=hr,
                    rbi=rbi, sb=sb, bb=bb, ba=ba, obp=obp, slg=slg )
    
    
    return player




def populate_teams(player_names, num_teams=30, players_per_team=25):
    teams = []
    first_names, last_names = zip(*(name.split() for name in player_names))
    first_names = list(first_names)  # Convert to mutable list
    last_names = list(last_names)  # Convert to mutable list
    #print(last_names)
    random.shuffle(first_names)
    random.shuffle(last_names)
    
    for _ in range(num_teams):
        team = []
        for _ in range(players_per_team):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            team.append((first_name, last_name))
        teams.append(team)
    return teams






if __name__ == "__main__":
    url = "https://www.mlb.com/players"
    # If parsing player names from a web site, set the URL above
    # Currently the get_player_names function reads a local HTML file
    player_names = get_player_names(url)
    if player_names:
        teams = populate_teams(player_names)
        create_database()
        #insert_data(teams)

    else:
        print("No player names fetched, cannot generate teams.")
