import chess

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

def ValueFunctionMaterial(board: chess.Board):
    (white, black) = MaterialCount(board)

    if board.turn:
        return white - black
    else:
        return black - white