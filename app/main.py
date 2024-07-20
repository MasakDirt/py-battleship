from collections import Counter


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return (f"Deck(row={self.row}, "
                f"column={self.column}, live={self.is_alive})")


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.decks = []
        self.__fill_decks(start, end)

    def __fill_decks(self, start: tuple, end: tuple) -> None:
        if start == end:
            self.decks.append(Deck(start[0], start[1]))
        elif start[0] == end[0]:
            for i in range(start[1], end[1] + 1):
                self.decks.append(Deck(start[0], i))
        else:
            for i in range(start[0], end[0] + 1):
                self.decks.append(Deck(i, start[1]))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def is_last_alive(self, row: int, column: int) -> bool:
        sum_of_alive = sum(deck.is_alive for deck in self.decks)
        if sum_of_alive > 1:
            return False
        current_deck = self.get_deck(row, column)
        if (sum_of_alive == 1 and current_deck is not None
                and current_deck.is_alive):
            return True

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is not None and self.is_last_alive(row, column):
            deck.is_alive = False
            return "Sunk!"
        if deck is not None and deck.is_alive:
            deck.is_alive = False
            return "Hit!"
        return "Miss!"

    def __repr__(self) -> str:
        return str(self.decks)


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            start = ship[0]
            end = ship[1]
            self.__fill_ship_key(start, end)

        self._validate_field()

    def __fill_ship_key(self, start: tuple, end: tuple) -> None:
        result_list = []
        if start == end:
            result_list.append((start[0], start[1]))
        elif start[0] == end[0]:
            for i in range(start[1], end[1] + 1):
                result_list.append((start[0], i))
        else:
            for i in range(start[0], end[0] + 1):
                result_list.append((i, start[1]))

        self.field[tuple(result_list)] = Ship(start, end)

    def fire(self, location: tuple) -> str:
        for cords in self.field:
            if location in cords:
                return self.field[cords].fire(location[0], location[1])

        return "Miss!"

    def __repr__(self) -> str:
        return str(self.field)

    def _validate_field(self) -> None:
        assert len(self.field) == 10, \
            "the total number of the ships should be 10"

        expected_dict = {"1": 4, "2": 3, "3": 2, "4": 1}
        counter = Counter(str(len(cords)) for cords in self.field)
        assert expected_dict == counter, \
            """In Battleship should be:
                 4 single-deck ships;
                 3 double-deck ships;
                 2 three-deck ships;
                 1 four-deck ship;
            """
