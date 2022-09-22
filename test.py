import unittest
import six
from Player import Player, Point
from Weiqi import Stone_liberty, GameState, Action, Board

class BoardTest(unittest.TestCase):
    def test_capture(self):
        board = Board(19)
        board.place_stone(Player.black, Point(2, 2))
        board.place_stone(Player.white, Point(1, 2))
        self.assertEqual(Player.black, board.place(Point(2, 2)))
        board.place_stone(Player.white, Point(2, 1))
        self.assertEqual(Player.black, board.place(Point(2, 2)))
        board.place_stone(Player.white, Point(2, 3))
        self.assertEqual(Player.black, board.place(Point(2, 2)))
        board.place_stone(Player.white, Point(3, 2))
        self.assertIsNone(board.place(Point(2, 2)))

    def test_capture_two_stones(self):
        board = Board(19)
        board.place_stone(Player.black, Point(2, 2))
        board.place_stone(Player.white, Point(1, 2))
        board.place_stone(Player.black, Point(2, 3))
        board.place_stone(Player.white, Point(1, 3))
        self.assertEqual(Player.black, board.place(Point(2, 2)))
        self.assertEqual(Player.black, board.place(Point(2, 3)))
        board.place_stone(Player.white, Point(3, 2))
        board.place_stone(Player.white, Point(3, 3))
        self.assertEqual(Player.black, board.place(Point(2, 2)))
        self.assertEqual(Player.black, board.place(Point(2, 3)))
        board.place_stone(Player.white, Point(2, 1))
        board.place_stone(Player.white, Point(2, 4))
        self.assertIsNone(board.place(Point(2, 2)))
        self.assertIsNone(board.place(Point(2, 3)))

    def test_capture_is_not_suicide(self):
        board = Board(19)
        board.place_stone(Player.black, Point(1, 1))
        board.place_stone(Player.black, Point(2, 2))
        board.place_stone(Player.black, Point(1, 3))
        board.place_stone(Player.white, Point(2, 1))
        board.place_stone(Player.white, Point(1, 2))
        self.assertIsNone(board.place(Point(1, 1)))
        self.assertEqual(Player.white, board.place(Point(2, 1)))
        self.assertEqual(Player.white, board.place(Point(1, 2)))

    def test_remove_liberties(self):
        board = Board(5)
        board.place_stone(Player.black, Point(3, 3))
        board.place_stone(Player.white, Point(2, 2))
        white_string = board.get_stone(Point(2, 2))
        six.assertCountEqual(
            self,
            [Point(2, 3), Point(2, 1), Point(1, 2), Point(3, 2)],
            white_string.liberty)
        board.place_stone(Player.black, Point(3, 2))
        white_string = board.get_stone(Point(2, 2))
        six.assertCountEqual(
            self,
            [Point(2, 3), Point(2, 1), Point(1, 2)],
            white_string.liberty)

    def test_empty_triangle(self):
        board = Board(5)
        board.place_stone(Player.black, Point(1, 1))
        board.place_stone(Player.black, Point(1, 2))
        board.place_stone(Player.black, Point(2, 2))
        board.place_stone(Player.white, Point(2, 1))
        black_string = board.get_stone(Point(1, 1))
        six.assertCountEqual(
            self,
            [Point(3, 2), Point(2, 3), Point(1, 3)],
            black_string.liberty)

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

class GameTest(unittest.TestCase):
    def test_new_game(self):
        game = GameState.new_game(19)
        game = game.apply_move(Action.move(Point(16, 16)))
        game = game.apply_move(Action.move(Point(17, 16)))
        game = game.apply_move(Action.move(Point(17, 17)))
        game = game.apply_move(Action.move(Point(16, 17)))
        game = game.apply_move(Action.move(Point(16, 18)))
        game = game.apply_move(Action.move(Point(17, 18)))
        game = game.apply_move(Action.move(Point(15, 17)))
        game = game.apply_move(Action.move(Point(18, 17)))
        game = game.apply_move(Action.move(Point(5, 5)))
        game = game.apply_move(Action.move(Point(16, 17)))
        game = game.apply_move(Action.move(Point(17, 17)))
        game = game.apply_move(Action.move(Point(16, 17)))
        game = game.apply_move(Action.move(Point(17, 17)))
        print_board(game.board)



if __name__ == '__main__':
    unittest.main()