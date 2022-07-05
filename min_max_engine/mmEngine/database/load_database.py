from pathlib import Path
from os.path import exists
from chess.pgn import read_game, read_headers

def load_database():
    database_dir = Path(__file__).parents[0]
    database_location =   Path(database_dir , "database.pgn")

    if not exists(database_location):
        print(f"cant find database at {database_location}")
        return None

    print(f"Reading database from: {database_location}")

    data = open(database_location)

    # should we convert to numpy?
    games = []
    for i in range(int(1e9)):
        try:
            g = read_game(data)
            if g is None:
                break
            games.append(g)
        except:
            print(f"error on game{i}")
    
    return None