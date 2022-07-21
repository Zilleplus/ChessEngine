from typing import Optional, Tuple
import chess
from mmEngine.agents import Agent
from mmEngine.value_funtions import ValueFunctionMaterial, ValueFunction
import numpy as np
import sys

def MinMaxSearch(board: chess.Board, evaluation_function: ValueFunction, depth) -> Tuple[list[chess.Move], float]:
    """
    Min-max search on the board for a certain depth

    returns: (moves of full horizon, cost after playing these moves)
    """
    if depth == 0:
        # end the recusion
        return ([], evaluation_function(board))

    moves: list[chess.Move] = list(board.legal_moves)
    if not any(moves):
        # unable to make any moves, evaluate board position
        return ([], evaluation_function(board))

    best_score: float = -sys.maxsize
    best_moves: list[chess.Move] = []
    for m in moves:
        board.push(m)
        move_history_opponent, score_opponent = MinMaxSearch(board, evaluation_function, depth -1)
        score = -score_opponent
        if score > best_score:
            best_score =  score
            best_moves = [m] + move_history_opponent
        board.pop()

    return (best_moves, best_score)


class MinMaxAgent(Agent):
    """
    Chess agent using min max algorithm
    """
    evaluation_function: ValueFunction
    depth: int
    def __init__(self, evaluation_function: ValueFunction=ValueFunctionMaterial(), depth: int = 3):
        self.evaluation_function = evaluation_function
        self.depth = depth

    def select_move(self, board: chess.Board) -> Optional[chess.Move]:
        moves = list(board.legal_moves)

        best_score: float = -sys.maxsize
        best_moves: list[chess.Move] = []
        for m in moves:
            board.push(m)
            move_history, score_opponent = MinMaxSearch(board, self.evaluation_function, self.depth - 1)
            score = -score_opponent
            if score > best_score:
                best_score = score
                best_moves = [m] + move_history
            board.pop()

        if len(best_moves) == 0:
            return None

        return best_moves[0]