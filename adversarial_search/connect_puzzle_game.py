from adversarial_search.connect_ai import minmax
from adversarial_search.connect_puzzle import Connect, WrongInputError, SlotFullError


class Game:
    SEARCH_DEPTH: int = 10

    def __init__(self) -> None:
        self.connect: Connect = Connect()

    def turn_ai(self) -> None:
        print('Thinking...')
        slot: int = minmax(self.connect, self.SEARCH_DEPTH).slot
        self.connect.play_move(slot)

    @staticmethod
    def input_human_turn() -> int:
        slot: str = input('Make your move: ')
        if not slot.isdigit():
            raise WrongInputError('Input positive integer number!')
        return int(slot) - 1

    def turn_human(self) -> None:
        try:
            slot: int = self.input_human_turn()
            self.connect.play_move(slot)
        except (ValueError, WrongInputError, SlotFullError) as e:
            print(str(e))
            self.turn_human()

    def start(self) -> None:
        while self.connect:
            if self.connect.player_turn == 1:
                self.turn_ai()
            else:
                self.turn_human()
            print(self.connect)
        print(self.connect.winner or 'Draw!')


def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
