import chess

from mmEngine.value_funtions.value_function import ValueFunction

piece_values = {
    1 : 1, # pawn
    2 : 3, # knight
    3 : 3, # bishop
    4 : 5, # rook
    5 : 9, # queen
    6 : 0, # king
}

def MaterialCount(board: chess.Board):
    white_material = 0
    black_material = 0
    for i in range(0, 8*8):
        p = board.piece_at(i)
        if p is None:
            continue
        color = p.color
        if color:
            white_material = white_material + piece_values[p.piece_type]
        else:
            black_material = black_material + piece_values[p.piece_type]

    return (white_material, black_material)


class ValueFunctionMaterial:
    """
    Classic material count value function

    Satisfies the ValueFunction protocol
    """
    def __call__(self, board: chess.Board) -> float:
        out = board.outcome()
        if out is not None:
            winner = out.winner
            if winner is not None:
                # the game is over with a winner
                if winner == board.turn:
                    return 1000.0
                else:
                    return -1000.0

        (white, black) = MaterialCount(board)

        if board.turn:
            return float(white - black)
        else:
            return float(black - white)