from pathlib import Path
from os.path import exists
from typing import Any, Optional, Tuple
from chess.pgn import read_game, read_headers
import numpy as np
import chess

def convert(board: chess.Board) -> np.ndarray:
    # we have 8*8=64 squares(so 64 times a byte) and one last byte to store the turn
    x: np.ndarray = np.zeros(8*8 + 1, np.uint8)

    for i in range(8*8):
        p: Optional[chess.Piece] = board.piece_at(i)
        if p is None:
            continue
        x[i] = p.piece_type

    x[64] = 1 if board.turn else 0

    return x

def get_database_dir() -> Path:
    return Path(__file__).parents[0]

def load_database(num_games: int) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    database_dir = get_database_dir()
    database_location =   Path(database_dir , "database.pgn")

    if not exists(database_location):
        print(f"cant find database at {database_location}")
        return None

    print(f"Reading database from: {database_location}")

    with open(database_location) as data:
        X: list[np.ndarray] = []
        Y: list[np.int8] = []
        for i in range(num_games):
            try:
                g = read_game(data)
                if g is None:
                    break # end of the file

                board = g.board()
                outcome: Optional[chess.Outcome] = g.end().board().outcome()
                y = np.int8(0)
                if outcome is not None:
                    winner: Optional[chess.Color] = outcome.winner
                    if winner is not None:
                        if winner:
                            y = np.int8(1)  # white wins
                        else:
                            y = np.int8(-1)  # black wins

                for i, move in enumerate(g.mainline_moves()):
                    board.push(move)
                    x = convert(board)
                    X.append(x)
                    Y.append(y)
            except:
                print(f"error on game{i}")
        
        return (np.array(X), np.array(Y))