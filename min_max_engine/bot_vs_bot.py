from random import Random
from time import sleep
import chess
import numpy as np
import chess.svg
from mmEngine.agents import RandomAgent, MinMaxAgent, minMaxAlphaBetaSearch, Agent
from mmEngine.value_funtions import NNKerasValueFunction
from mmEngine.value_funtions import MaterialCount
from pathlib import Path

def main():
    board = chess.Board()
    nn_location = Path("./trial_network.keras")

    print("game started... ")
    bot_white = minMaxAlphaBetaSearch(NNKerasValueFunction(nn_location))
    bot_black = RandomAgent()
    for i in range(40):
        if board.is_game_over():
            break

        assert board.turn
        white_move = bot_white.select_move(board)
        if white_move is None:
            break
        print(f"white picked move {board.san(white_move)}")
        board.push(white_move)

        assert not board.turn
        black_move = bot_black.select_move(board)
        print(f"black picked move {board.san(black_move)}")
        board.push(black_move)

    print(board)
    (white, black) = MaterialCount(board)
    print(f"white score is {white}")
    print(f"black score is {black}")

    outcome = board.outcome()
    if outcome is not None:
        print(f"The reason for termination: {outcome.termination}")
        winner = outcome.winner
        if winner is not None:
            print(f"The winner is: {winner}")


if __name__ == '__main__':
    main()