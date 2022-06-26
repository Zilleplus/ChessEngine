from random import Random
from time import sleep
import chess
import numpy as np
import chess.svg
from mmEngine.agents import RandomAgent

def main():
    board = chess.Board()

    print("game started... ")
    bot_white = RandomAgent()
    bot_black = RandomAgent()
    for i in range(200):
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
        if black_move is None:
            break
        print(f"black picked move {board.san(black_move)}")
        board.push(black_move)

    print(board)



if __name__ == '__main__':
    main()