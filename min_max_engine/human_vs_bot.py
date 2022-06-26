from random import Random
import chess
import numpy as np
import chess.svg
from mmEngine.agents import RandomAgent

def main():
    board = chess.Board()

    print("game started... ")
    bot = RandomAgent()
    while not board.is_game_over():
        human_move = None
        while human_move is None:
            try:
                human_input = input("move:")
                if human_input == 'q':
                    return
                if human_input == 'm':
                    print([board.san(m) for m in board.legal_moves])
                human_move = board.parse_san(human_input)
                board.push(human_move)
            except ValueError as e:
                print(f"{e}")
        print(board)

        bot_move = bot.select_move(board)
        print(f"\nbot picked move {board.san(bot_move)}")
        board.push(bot_move)
        print(board)
        print('A B C D E F G H')



if __name__ == '__main__':
    main()
