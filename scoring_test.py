import unittest

from Player import Player, Point
from Weiqi import Stone_liberty, GameState, Action, Board
import Scoring
COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: ' . ',
    Player.black: ' x ',
    Player.white: ' o ',
}
def print_board(board):
    for row in range(board.board_cols, 0, -1):
        bump = " " if row <= 9 else ""
        line = []
        for col in range(1, board.board_cols + 1):
            stone = board.place(Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print('%s%d %s' % (bump, row, ''.join(line)))
    print('    ' + '  '.join(COLS[:board.board_cols]))


class ScoringTest(unittest.TestCase):
    def test_scoring(self):
        # .w.ww
        # wwww.
        # bbbww
        # .bbbb
        # .b.b.
        board = Board(5)
        board.place_stone(Player.black, Point(1, 2))
        board.place_stone(Player.black, Point(1, 4))
        board.place_stone(Player.black, Point(2, 2))
        board.place_stone(Player.black, Point(2, 3))
        board.place_stone(Player.black, Point(2, 4))
        board.place_stone(Player.black, Point(2, 5))
        board.place_stone(Player.black, Point(3, 1))
        board.place_stone(Player.black, Point(3, 2))
        board.place_stone(Player.black, Point(3, 3))
        board.place_stone(Player.white, Point(3, 4))
        board.place_stone(Player.white, Point(3, 5))
        board.place_stone(Player.white, Point(4, 1))
        board.place_stone(Player.white, Point(4, 2))
        board.place_stone(Player.white, Point(4, 3))
        board.place_stone(Player.white, Point(4, 4))
        board.place_stone(Player.white, Point(5, 2))
        board.place_stone(Player.white, Point(5, 4))
        board.place_stone(Player.white, Point(5, 5))
        territory = Scoring.evaluate_territory(board)
        print(Scoring.evaluate_territory(board).num_black_stones)


        self.assertEqual(9, territory.num_black_stones)
        self.assertEqual(4, territory.num_black_territory)
        self.assertEqual(9, territory.num_white_stones)
        self.assertEqual(3, territory.num_white_territory)
        self.assertEqual(0, territory.num_dame)


class GameTest(unittest.TestCase):
    def test_new_game(self):
        start = GameState.new_game(5)
        start = start.apply_move(Action.move(Point(1, 2)))
        start = start.apply_move(Action.move(Point(3, 4)))
        start = start.apply_move(Action.move(Point(1, 4)))
        start = start.apply_move(Action.move(Point(3, 5)))
        start = start.apply_move(Action.move(Point(2, 2)))
        start = start.apply_move(Action.move(Point(4, 1)))
        start = start.apply_move(Action.move(Point(2, 3)))
        start = start.apply_move(Action.move(Point(4, 2)))
        start = start.apply_move(Action.move(Point(2, 4)))
        start = start.apply_move(Action.move(Point(4, 3)))
        start = start.apply_move(Action.move(Point(2, 5)))
        start = start.apply_move(Action.move(Point(4, 4)))
        start = start.apply_move(Action.move(Point(3, 1)))
        start = start.apply_move(Action.move(Point(5, 2)))
        start = start.apply_move(Action.move(Point(3, 2)))
        start = start.apply_move(Action.move(Point(5, 4)))
        start = start.apply_move(Action.move(Point(3, 3)))
        start = start.apply_move(Action.move(Point(1, 1)))

        result = Scoring.compute_game_result(start)
        print_board(start.board)
        print(result)

if __name__ == '__main__':
    unittest.main()