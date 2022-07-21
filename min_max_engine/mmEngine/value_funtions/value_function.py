from chess import Board
from typing import Protocol

class ValueFunction(Protocol):
    def __call__(self, board: Board):
        ...