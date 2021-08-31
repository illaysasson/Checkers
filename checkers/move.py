from pygame.constants import MOUSEMOTION
from .utility import position_to_notation
from .constants import WHITE, BLACK

class Move:
    def __init__(self, target_row, target_col, skipped):
        self.target = (target_row, target_col)
        self.skipped = skipped
    
    def captures(self):
    # Returns the number of eaten pieces
        return len(self.skipped)

    def __eq__(self, other):
        if self.target != other.target:
            return False
        if self.skipped != other.skipped:
            return False
        
        return True

    def print_move(self, piece_color, start_not):
        color_string = 'White' if piece_color == WHITE else 'Black'

        string = color_string + " Move: " + str(start_not) + "-" + str(position_to_notation(self.target[0], self.target[1]))
        if self.skipped != []:
            string += " ("
            for piece in self.skipped:
                string += str(piece) + ", "
            string = string.strip()
            string += ")"
        
        print(string)


class Moves:
    def __init__(self):
        self.moves = [] # List of Moves

    def can_move(self):
    # Returns if there's more than one move
        if len(self.moves) > 0:
            return True
        else:
            return False

    
    def combine_moves(self, moves):
    # Adds all moves from given Moves class to this current Moves class
        for move in moves.moves:
            self.add_move(move)

    def add_move(self, move):
    # If given a single move, adds the move to the list. If given Moves class, combines the two
        if isinstance(move, Move):
            self.moves.append(move)
        elif isinstance(move, Moves):
            self.combine_moves(move)
        else:
            return
    
    def get_move(self, row, col):
    # Checks if the target row and col exist in moves list. If it does, returns the move. If not, returns None
        target = (row, col)

        for move in self.moves:
            if move.target == target:
                return move
        
        return None

    def does_move_exist(self, find_move):
        for move in self.moves:
            if move == find_move:
                return True

        return False

    def max_captures(self):
    # Returns the maximum amount of captures out of all the moves
        max = 0

        for move in self.moves:
            if move.captures() > max:
                max = move.captures()
        
        return max
    
    def filter_moves_without_most_captures(self):
    # Removes all moves for a certain piece but the moves with the most captures:
        max = self.max_captures()
        new_moves = [move for move in self.moves if move.captures() == max]

        self.moves = new_moves


