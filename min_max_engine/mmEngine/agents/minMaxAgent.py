import chess
from mmEngine.agents import Agent
from mmEngine.value_funtions import ValueFunctionMaterial
import numpy as np
import sys

def MinMaxSearch(board: chess.Board, evaluation_function, depth):
    if depth == 0:
        # end the recusion
        return evaluation_function(board)

    moves = board.legal_moves
    if not any(moves):
        # unable to make any moves, evaluate board position
        return evaluation_function(board)

    costs = []
    for m in moves:
        board.push(m)
        new_eval = lambda b: -evaluation_function(b)
        cost = MinMaxSearch(board, new_eval, depth -1)
        costs.append(cost)
        board.pop()

    return max(costs)


class MinMaxAgent(Agent):
    """
    Chess agent using min max algorithm
    """
    def __init__(self, evaluation_function=ValueFunctionMaterial, depth = 3):
        self.evaluation_function = evaluation_function
        self.depth = depth

    def select_move(self, board: chess.Board):
        eval = self.evaluation_function
        moves = list(board.legal_moves)

        costs = []
        for m in moves:
            board.push(m)
            new_eval = lambda b: -self.evaluation_function(b)
            cost = MinMaxSearch(board, new_eval, self.depth - 1)
            costs.append(cost)
            board.pop()
        optimal_index = np.argmax(costs)

        return moves[optimal_index]