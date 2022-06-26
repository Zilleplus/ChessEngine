from mmEngine.agents import Agent
import numpy as np
import chess

class RandomAgent(Agent):
    """
    Most basic of bots, just picks random
    valid moves.
    """
    def select_move(self, board: chess.Board) -> chess.Move:
        player = board.turn
        moves = list(board.legal_moves)
        num_moves = len(moves)
        if num_moves == 0:
            return None
        random_moves = np.random.choice(a=moves, size=num_moves, replace=False)

        # Pick the first move that is not suicide
        for m in random_moves:
            board.push(m)
            if board.is_game_over():
                outcome = board.outcome()
                if outcome is not None and outcome.winner != player:
                        # don't pick this move, it's suicide
                        board.pop()
                        continue
                else:
                    # might be a draw now, but that's fine for now
                    board.pop()
                    return m
            else:
                board.pop()
                return m

        return moves[0]

