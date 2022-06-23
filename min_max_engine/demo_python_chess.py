import chess

# create and print out board
board = chess.Board()
print(board)

# find all the legal moves
mvs = list(board.legal_moves)
m = mvs[0]

# apply one move
board.push(m)
print(board)

# turn is 
# -> true when it's whites move
# -> false when it's black move
board.turn

# undo last move
board.pop()
print(board)

board.outcome()

p = board.piece_at(0)
p.color # true if white, false if black
print(type(p.piece_type)) # piece types are ints
chess.piece_name(p.piece_type)

# piece types
print(chess.piece_name(1)) # pawn
print(chess.piece_name(2)) # knight
print(chess.piece_name(3)) # bishop
print(chess.piece_name(4)) # rook
print(chess.piece_name(5)) # queen
print(chess.piece_name(6)) # king

piece_values = {
    1 : 1, # pawn
    2 : 3, # knight
    3 : 3, # bishop
    4 : 5, # rook
    5 : 9, # queen
}

def chess_score(board: chess.Board):
    white_score = 0
    black_score = 0
    for i in range(0, 8*8):
        board.piece_at(i)

    if board.turn:
        # white's turn
        return white_score - black_score
    else:
        return black_score - white_score

print(chess_score(board))

chess.square_name(5)