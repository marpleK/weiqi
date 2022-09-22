from collections import namedtuple
import enum
from Scoring import compute_game_result 
import copy
from Player import Player, Point

class Board():  
    def __init__(self, board_size):
        self.board_cols = board_size
        self.board_rows = board_size
        self._grid = {}
    def place_stone(self, player, point):
        """
        place_stone in board and there is no stone on the point 
        merge same color stones and liberties if liberty = 0 
        remove the stones
        """

        assert self.in_grid(point)
        assert self._grid.get(point) is None

        adjacent_same_color = []
        adjacent_opposite_color = []
        liberty = []
        for neighbor in point.neighbors(): 
            if not self.in_grid(neighbor):
                continue
            neighbor_stone = self._grid.get(neighbor)
            if neighbor_stone is None:
                liberty.append(neighbor)
            elif neighbor_stone.color == player:
                if neighbor_stone not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_stone)
            else:
                if neighbor_stone not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_stone)
        new_stone = Stone_liberty(player, [point], liberty)

        for same_color_stone in adjacent_same_color: 
            new_stone = new_stone.merged_with(same_color_stone)
        for new_stone_point in new_stone.stone:
            self._grid[new_stone_point] = new_stone
        for other_color_stone in adjacent_opposite_color: 
            other_color_stone.remove_liberty(point)
        for other_color_stone in adjacent_opposite_color:
            if other_color_stone.liberty_num == 0:
                self.remove_stone(other_color_stone)
        

    def in_grid(self, point):
        return 1 <= point.row <= self.board_rows and \
            1 <= point.col <= self.board_cols

    def place(self, point): 
        stone = self._grid.get(point)
        if stone is None:
            return None
        return stone.color

    def get_stone(self, point): 
        stone = self._grid.get(point)
        if stone is None:
            return None
        return stone

    def remove_stone(self, stone):
        for point in stone.stone:
            for neighbor in point.neighbors(): 
                neighbor_stone = self._grid.get(neighbor)
                if neighbor_stone is None:
                    continue
                if neighbor_stone is not stone:
                    neighbor_stone.add_liberty(point)
            del(self._grid[point])


#Rule
class Action:
    """
    Three action: 
    1.move
    2.pass this move
    3.resign
    """
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_move = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def move(cls, point):
        return Action(point=point)

    @classmethod
    def pass_move(cls):
        return Action(is_pass=True)

    @classmethod
    def resign(cls):
        return Action(is_resign=True)

    def __str__(self):
        if self.is_pass:
            return 'pass'
        if self.is_resign:
            return 'resign'
        return '(r %d, c %d)' % (self.point.row, self.point.col)

class Stone_liberty():  
    def __init__(self, color, stone_place, liberty):
        self.color = color
        self.stone = set(stone_place)
        self.liberty = set(liberty)

    def remove_liberty(self, point):
        self.liberty.remove(point)

    def add_liberty(self, point):
        self.liberty.add(point)

    def merged_with(self, stone_liberty): 
        """combine same color stones and liberties together"""
        assert stone_liberty.color == self.color
        combined_stones = self.stone | stone_liberty.stone
        return Stone_liberty(
            self.color,
            combined_stones,
            (self.liberty | stone_liberty.liberty) - combined_stones)

    @property
    def liberty_num(self):
        return len(self.liberty)

    def __eq__(self, other):
        return isinstance(other, Stone_liberty) and \
            self.color == other.color and \
            self.stone == other.stone and \
            self.liberty == other.liberty
            
class GameState():
    def __init__(self, board, next_player, previous, action):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = action

    def apply_move(self, action): 
        """ next move return new gamestate """
        if action.is_move:
            assert self.ko_rule(self.next_player, action)
            assert self.is_suicide(self.next_player, action)
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, action.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, action)

    def is_over(self):
        """ next move return new gamestate """
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    def is_suicide(self, player, action):
        """ don't suicide (next move liberty = 0)"""
        if not action.is_move:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, action.point)
        new_stone = next_board.get_stone(action.point)
        return new_stone.liberty_num != 0
    
    """ 打劫ko """
    @property
    def situation(self):
        return (self.next_player, self.board)

    def ko_rule(self, player, action):
        if not action.is_move:
            return True
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, action.point)
        next_situation = (player.other, next_board._grid)
        past_state = self.previous_state
        if past_state:
            past_situation = (player.other, past_state.board._grid)
            if past_situation == next_situation:
                return False
            past_state = past_state.previous_state
        return True

    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size,)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)

    def is_valid_move(self, action):
        if self.is_over():
            return False
        if action.is_pass or action.is_resign:
            return True
        return (
            self.board.place(action.point) is None and
            self.is_suicide(self.next_player, action) and
            self.ko_rule(self.next_player, action))

