from typing import Optional
import unittest
import chess
from mmEngine.agents import MinMaxAlphaBetaAgent

class MinMaxAgentAlphaBeta_test(unittest.TestCase):
    def test_given_free_material_take_it(self):
        b = chess.Board()
        b.clear()
        white_king = chess.Piece(piece_type=chess.KING, color=True)
        black_king = chess.Piece(piece_type=chess.KING, color=False)
        b.set_piece_at(chess.A2, white_king)
        b.set_piece_at(chess.A7, black_king)

        white_rook = chess.Piece(piece_type=chess.ROOK, color=True)
        b.set_piece_at(chess.F1, white_rook)
        black_rook = chess.Piece(piece_type=chess.ROOK, color=False)
        b.set_piece_at(chess.F7, black_rook)
        b.turn = True # whites move

        self.assertFalse(b.is_game_over())

        agent = MinMaxAlphaBetaAgent(depth=3)
        optimal_move: Optional[chess.Move] = agent.select_move(b)

        self.assertIsNotNone(optimal_move)
        str_optimal_move: str = str(optimal_move)

        expected_move = chess.Move(chess.F1, chess.F7)

        self.assertEqual(expected_move, optimal_move)



if __name__ == "__main__":
    unittest.main()