class ConnectError(Exception):
    ...


class SlotFullError(ConnectError):
    ...


class WrongInputError(ConnectError):
    ...


class Connect:
    HUMAN: str = 'H'
    AI: str = 'A'
    PLAYERS: dict[str, int] = {HUMAN: -1, AI: 1}

    BOARD_EMPTY_SLOT: str = '_'
    WINNING_SEQUENCE_COUNT: int = 4

    def __init__(self, board_size_x: int = 5, board_size_y: int = 4) -> None:
        self.board_size_x: int = board_size_x
        self.board_size_y: int = board_size_y
        self.board: list[list[str]] = self.generate_board()
        self.player_turn: int = self.PLAYERS[self.AI]

    def __str__(self) -> str:
        return '\n'.join([''.join(row) for row in self.board])

    def generate_board(self) -> list[list[str]]:
        return [[self.BOARD_EMPTY_SLOT] * self.board_size_y for _ in range(self.board_size_x)]

    def reset(self) -> None:
        self.board = self.generate_board()

    def status_turn(self) -> str:
        return 'It is Human to play' if self.player_turn == self.PLAYERS[self.HUMAN] else 'It is AI to play'

    def get_score_for_ai(self) -> int:
        if winner := self.winner:
            return 10 if winner == self.AI else -10
        return 0

    @property
    def winner(self) -> str | None:
        for row in range(self.board_size_x):
            for col in range(self.board_size_y):
                offsets: list[tuple[int, int]] = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Rows, cols, pos and neg diagonals
                for offset_x, offset_y in offsets:
                    if winner := self.has_a_row_from_point(row, col, offset_x, offset_y):
                        return winner
        return None

    def __bool__(self) -> bool:
        return self.winner is None and not self.is_board_full

    def has_a_row_from_point(self, x: int, y: int, offset_x: int, offset_y: int) -> str | None:
        winner: str = self.board[x][y]
        if winner == '_':
            return None
        for i in range(self.WINNING_SEQUENCE_COUNT - 1):
            x += offset_x
            y += offset_y
            if not self.is_within_bounds(x, y) or self.board[x][y] != winner:
                return None

        return winner

    def is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.board_size_x and 0 <= y < self.board_size_y

    def is_slot_full(self, slot: int) -> bool:
        for row in self.board:
            if row[slot] == self.BOARD_EMPTY_SLOT:
                return False
        return True

    @property
    def is_board_full(self) -> bool:
        return all(self.BOARD_EMPTY_SLOT not in row for row in self.board)

    def execute_move(self, player: str, slot: int) -> None:
        for i in range(self.board_size_x):
            if self.board[~i][slot] == '_':
                self.board[~i][slot] = player
                return

    def play_move(self, slot: int) -> None:
        if not 0 <= slot < self.board_size_y:
            raise WrongInputError('Wrong input number`s slot!')
        if self.is_slot_full(slot):
            raise SlotFullError('This slot is full!')

        if self.player_turn == self.PLAYERS[self.AI]:
            self.execute_move(self.AI, slot)
        else:
            self.execute_move(self.HUMAN, slot)
        self.player_turn *= -1


if __name__ == '__main__':
    connect: Connect = Connect()

    connect.board = [['A', 'H', 'A', 'H'],
                     ['A', 'H', 'A', 'H'],
                     ['A', 'A', 'H', 'H'],
                     ['H', 'H', 'A', 'A'],
                     ['A', 'H', 'A', 'H']]
    print(bool(connect))