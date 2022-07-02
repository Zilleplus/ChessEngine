from typing import Optional, Tuple
import chess
from mmEngine.agents import Agent
from mmEngine.value_funtions import ValueFunctionMaterial
import numpy as np
import sys

def MinMaxAlphaBetaSearch(board: chess.Board, evaluation_function, depth, best_white: int, best_black: int) -> Tuple[list[chess.Move], int]:
    """
    Min-max search on the board for a certain depth

    returns: (moves of full horizon, cost)
    """
    if depth == 0:
        # end the recusion
        return ([], evaluation_function(board))

    moves: list[chess.Move] = list(board.legal_moves)
    if not any(moves):
        # unable to make any moves, evaluate board position
        return ([], evaluation_function(board))

    best_score: int = -sys.maxsize
    best_moves: list[chess.Move] = []
    for m in moves:
        board.push(m)
        moves_opponent, score_opponent = MinMaxAlphaBetaSearch(
            board,
            evaluation_function,
            depth -1,
            best_white=best_white,
            best_black=best_black)
        score = -score_opponent
        if score > best_score:
            best_score =  score
            best_moves = [m] + moves_opponent
        board.pop()

    return (best_moves, best_score)


class MinMaxAlphaBetaAgent(Agent):
    """
    Chess agent using min max algorithm
    """
    depth: int
    def __init__(self, evaluation_function=ValueFunctionMaterial, depth: int = 3):
        self.evaluation_function = evaluation_function
        self.depth = depth

    def select_move(self, board: chess.Board) -> Optional[chess.Move]:
        eval = self.evaluation_function
        moves = list(board.legal_moves)

        best_score: int = -sys.maxsize
        best_moves: list[chess.Move] = []
        for m in moves:
            board.push(m)
            # The evaluation function always evaluates 
            # for the player that has the move.
            # So if we make a move, and we want to know 
            # the score in respect to the player that just
            # played -> invert the cost.
            new_eval = lambda b: -self.evaluation_function(b)
            moves, score_opponent = MinMaxAlphaBetaSearch(board, self.evaluation_function,
                self.depth - 1, best_white=0, best_black=0)
            score = -score_opponent
            if score > best_score:
                best_score = score
                best_moves = [m] + moves
            board.pop()

        if len(best_moves) == 0:
            return None

        return best_moves[0]