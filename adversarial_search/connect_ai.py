from __future__ import annotations
import copy
import random
from dataclasses import dataclass

from adversarial_search.connect_puzzle import Connect, ConnectError

MAX: int = 1
MIN: int = -1
INFINITY_NEGATIVE: float = float('-inf')
INFINITY_POSITIVE: float = float('inf')


@dataclass
class Move:
    slot: int = 0
    score: float = 0

    def __lt__(self, other: Move) -> bool:
        return self.score < other.score


def minmax(connect: Connect, depth: int, min_or_max: int = 1, slot: int = -1,
           alpha: float = INFINITY_NEGATIVE, beta: float = INFINITY_POSITIVE) -> Move:
    current_score: int = connect.get_score_for_ai()
    if current_score != 0 or connect.is_board_full or depth == 0:
        return Move(slot, current_score)

    best_move: Move = Move(-1, INFINITY_NEGATIVE * min_or_max)
    slots: list[int] = random.sample(range(connect.board_size_y), connect.board_size_y)
    for slot in slots:
        try:
            neighbor: Connect = copy.deepcopy(connect)
            neighbor.play_move(slot)
        except ConnectError:
            pass
        else:
            move: Move = minmax(neighbor, depth - 1, min_or_max * -1, slot)
            if min_or_max == MAX:
                best_move = max(best_move, move)
                alpha = max(alpha, best_move.score)
            else:
                best_move = min(best_move, move)
                beta = min(beta, best_move.score)

            if alpha >= beta:
                break

    return best_move
