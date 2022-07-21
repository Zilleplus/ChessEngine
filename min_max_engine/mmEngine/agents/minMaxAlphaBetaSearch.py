from multiprocessing.sharedctypes import Value
from typing import Optional, Tuple
import chess
from mmEngine.agents import Agent
from mmEngine.value_funtions import ValueFunctionMaterial, ValueFunction
import sys

def MinMaxAlphaBetaSearch(board: chess.Board, evaluation_function: ValueFunction, depth, best_white: int, best_black: int) -> Tuple[list[chess.Move], int]:
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

        if board.turn:
            # playing with white
            best_white = max(best_white, best_score)
            if score_opponent < best_black:
                # black has better options to play
                break
        else:
            best_black = max(best_black, best_score)
            if score_opponent < best_white:
                # white has better options to play
                break

    return (best_moves, best_score)


class MinMaxAlphaBetaAgent(Agent):
    """
    Chess agent using min max algorithm
    """
    evaluation_function: ValueFunction
    depth: int
    def __init__(self, evaluation_function: ValueFunction=ValueFunctionMaterial(), depth: int = 3):
        self.evaluation_function = evaluation_function
        self.depth = depth

    def select_move(self, board: chess.Board) -> Optional[chess.Move]:
        eval = self.evaluation_function
        moves = list(board.legal_moves)

        best_black: int = -sys.maxsize
        best_white: int = -sys.maxsize


        best_score: int = -sys.maxsize
        best_moves: list[chess.Move] = []
        for m in moves:
            board.push(m)
            moves, score_opponent = MinMaxAlphaBetaSearch(board, self.evaluation_function,
                self.depth - 1, best_white=best_white, best_black=best_black)
            score = -score_opponent
            if score > best_score:
                best_score = score
                best_moves = [m] + moves
            board.pop()

            if board.turn:
                best_white = max(best_white, best_score)
            else:
                best_black = max(best_black, best_score)

        if len(best_moves) == 0:
            return None

        return best_moves[0]