import math
import pygame
import random
from .utility import position_to_notation
from .constants import BACKGROUND, TILE, ROWS, COLS, SQUARE_SIZE, WHITE, BLACK, AI_PLAYER
from .piece import Piece
from .move import Move, Moves
from .settings import free_king_movement, backwards_eating_in_doubles, srufim

class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.white_left = self.black_left = 12
        self.white_kings = self.black_kings = 0

        self.create_board()

    # Draws the playable squares
    def draw_squares(self, win):
        win.fill(BACKGROUND)

        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, TILE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Creates the piece in the board
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(None)
                else:
                    self.board[row].append(None)
    
    def make_everyone_king(self):
    # Makes all pieces into kings. For testing purposes.
        for pieces in self.board:
            for piece in pieces:
                if piece is not None:
                    piece.make_king()
    
    # Draws the entire board and the pieces
    def draw(self, win):
        self.draw_squares(win)

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]

                if piece != None:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = None
            if piece.color == WHITE:
                if piece.king:
                    self.white_kings -= 1
                self.white_left -= 1
            else:
                if piece.king:
                    self.black_kings -= 1
                self.black_left -= 1

    def simple_evaluate(self):
    # Returns score for minimax algorithim
        if AI_PLAYER == BLACK:
            return self.black_left - self.white_left + (self.black_kings * 0.5 - self.white_kings * 0.5)
        else:
            return self.white_left - self.black_left + (self.white_kings * 0.5 - self.black_kings * 0.5)

    def advanced_evaluate(self):
    # 1111 - First two digits for blacks - whites (regular pieces are worth 3, kings 5), then 2 digits that are higher if more pieces are close to the edges, then a random digit
        pieces_eval = 0
        edges_eval = 0
        random_eval = random.randrange(0, 10)

        lose_flag = True

        if AI_PLAYER == BLACK:
            pieces_eval += self.black_left*3 - self.white_left*3 + (self.black_kings * 5 - self.white_kings * 5)
        else:
            pieces_eval += self.white_left*3 - self.black_left*3 + (self.white_kings * 5 - self.black_kings * 5)

        # Edge eval from 1-4 according to how close to the edge
        for row in self.board:
            for piece in row:
                if piece is not None and piece.color == AI_PLAYER:
                    if (piece.row == ROWS - 1 or piece.col == COLS - 1) or (piece.col == 0 or piece.row == 0):
                        edges_eval += 4
                    elif (piece.row == ROWS - 2 or piece.col == COLS - 2) or (piece.col == 1 or piece.row == 1):
                        edges_eval += 3
                    elif (piece.row == ROWS - 3 or piece.col == COLS - 3) or (piece.col == 2 or piece.row == 2):
                        edges_eval += 2
                    else:
                        edges_eval += 1

                    if self.get_valid_moves(piece).can_move(): # If at least one piece can move, then this board isn't a losing one
                        lose_flag = False

        eval = (pieces_eval * 1000) + (edges_eval * 10) + random_eval

        if lose_flag:
            return -math.inf
        else:
            return eval
                    
    
    def get_all_pieces(self, color):
        pieces = []

        for row in self.board:
            for piece in row:
                if piece is not None and piece.color == color:
                    pieces.append(piece)
        
        return pieces

    # Moves a piece to a given row and col        
    def move(self, piece, row, col):
        # Switches place with the piece in the target location
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        # Checks if needs to be made king
        if piece.color == WHITE and row == 0 and (not piece.king):
            piece.make_king()
            self.white_kings += 1
        elif piece.color == BLACK and row == ROWS - 1 and (not piece.king):
            piece.make_king()
            self.black_kings += 1

        piece.move(row, col)

    # Returns piece in given row and col
    def get_piece(self, row, col):
        return self.board[row][col]

    def winner(self, turn):
        moves_available = self.get_all_moves(turn)

        # Checks if a color has ran out of moves
        if not moves_available.can_move:
            if turn == WHITE:
                return BLACK
            else:
                return WHITE
        else:
            if (self.white_left) <= 0:
                return BLACK
            elif (self.black_left) <= 0:
                return WHITE
            return None

    def get_all_moves(self, color):
    # Gets all moves for a color
        moves = Moves()

        for piece in self.get_all_pieces(color):
            moves.add_move(self.get_valid_moves(piece))
        
        return moves

    def filter_srufim(self, color):
        # Returns a moves object for all moves for all pieces that contain the most amount of captures
        srufim_moves = self.get_all_moves(color)

        # Only keeps moves with max captures
        srufim_moves.filter_moves_without_most_captures()

        return srufim_moves


    def get_valid_moves(self, piece):
        moves = Moves()
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if free_king_movement:
            if not piece.king:
                if piece.color == WHITE:
                    moves.add_move(self._traverse_left(row - 1, max(row-3, -1), -1, piece.color, left))
                    moves.add_move(self._traverse_right(row - 1,  max(row-3, -1), -1, piece.color, right))
                elif piece.color == BLACK:
                    moves.add_move(self._traverse_left(row + 1, min(row+3, ROWS), 1, piece.color, left))
                    moves.add_move(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
            else:
                moves.add_move(self._traverse_left_king(row - 1, -1, -1, piece.color, left))
                moves.add_move(self._traverse_right_king(row - 1, -1, -1, piece.color, right))
                moves.add_move(self._traverse_left_king(row + 1, ROWS, 1, piece.color, left))
                moves.add_move(self._traverse_right_king(row + 1, ROWS, 1, piece.color, right))
        else:
            if piece.color == WHITE or piece.king:
                moves.add_move(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
                moves.add_move(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
            if piece.color == BLACK or piece.king:
                moves.add_move(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
                moves.add_move(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))

        return moves

    def _enemy_piece_on_diagonal(self, start, stop, step, color, col, left_or_right): # True for left diagonal, False for right diagonal
    # Checks if theres an enemy piece with a space behind it on specific diagonal.
        flag = None

        if left_or_right:
            col -= 1
        else:
            col += 1

        for r in range(start, stop, step):
            # Breaks if hitting the wall.
            if col < 0 and left_or_right:
                break
            if col >= COLS and not left_or_right:
                break
            
            current = self.board[r][col]

            if current == None:
            # If the tile is empty and there's an enemy piece beforehand, returns true.
                if flag:
                    return True
            elif current.color == color:
            # Breaks when hitting a friendly piece.
                break
            else:
            # Declares that an enemy piece has been found and now looking in the next interation to see if the tile after is empty
                flag = True
            
            if left_or_right:
                col -= 1
            else:
                col += 1

        return False

    def _traverse_left_king(self, start, stop, step, color, left, skipped=[]):
    # Checks moves on the left diagonal
        moves = Moves()
        last = []

        for r in range(start, stop, step):
            # Stops when hitting the wall
            if left < 0:
                break

            current = self.board[r][left]

            if current == None:
                captured_piece = skipped + last
                if not last: # Records empty moves 
                    moves.add_move(Move(r, left, captured_piece))
                else:
                    # Checks if a piece has been captured more than once to avoid infinite recursion
                    if not captured_piece.count(last[0]) > 1:
                        moves.add_move(Move(r, left, captured_piece))

                    # Checking for double jumps
                    # Check in the same diagonal:
                    if self._enemy_piece_on_diagonal(r + step, stop, step, color, left, True):
                        try:
                            moves.add_move(self._traverse_left_king(r + step, stop, step, color, left-1, last + skipped))
                        except RecursionError:
                            break
                    if step == -1:
                    # When moving up:
                        # Up diagonal:
                        if self._enemy_piece_on_diagonal(r - 1, -1, -1, color, left, False):
                            try:
                                moves.add_move(self._traverse_right_king(r - 1, -1, -1, color, left+1, last + skipped))
                            except RecursionError:
                                break
                        # Down diagonal:
                        if self._enemy_piece_on_diagonal(r + 1, ROWS, 1, color, left, True):
                            try:
                                moves.add_move(self._traverse_left_king(r + 1, ROWS, 1, color, left-1, last + skipped))
                            except RecursionError:
                                break
                    else:
                    # When moving down:
                        # Up diagonal:
                        if self._enemy_piece_on_diagonal(r - 1, -1, -1, color, left, True):
                            try:
                                moves.add_move(self._traverse_left_king(r - 1, -1, -1, color, left-1, last + skipped))
                            except RecursionError:
                                break
                            
                        # Down diagonal:
                        if self._enemy_piece_on_diagonal(r + 1, ROWS, 1, color, left, False):
                            try:
                                moves.add_move(self._traverse_right_king(r + 1, ROWS, 1, color, left+1, last + skipped))
                            except RecursionError:
                                break


            elif current.color == color:
            # Breaking when hitting a friendly color
                break
            elif last:
            # Breaking when hitting 2 enemy pieces in a row
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right_king(self, start, stop, step, color, right, skipped=[]):
    # Checks moves on the right diagonal
        moves = Moves()
        last = []

        for r in range(start, stop, step):
            # Stops when hitting the wall
            if right >= COLS:
                break

            current = self.board[r][right]

            if current == None:
                captured_piece = skipped + last
                if not last: # Records empty moves
                    moves.add_move(Move(r, right, captured_piece))
                else:
                    if not captured_piece.count(last[0]) > 1: # Checks if a piece has been captured more than once to avoid infinite recursion
                        moves.add_move(Move(r, right, captured_piece))

                    # Checking for double jumps
                    # Check in the same diagonal:
                    if self._enemy_piece_on_diagonal(r + step, stop, step, color, right, False):
                        try:
                            moves.add_move(self._traverse_right_king(r + step, stop, step, color, right+1, last + skipped))
                        except RecursionError:
                            break

                    if step == -1:
                    # When moving up:
                        # Up diagonal:
                        if self._enemy_piece_on_diagonal(r - 1, -1, -1, color, right, True):
                            try:
                                moves.add_move(self._traverse_left_king(r - 1, -1, -1, color, right-1, last + skipped))
                            except RecursionError:
                                break
                        # Down diagonal:
                        if self._enemy_piece_on_diagonal(r + 1, ROWS, 1, color, right, False):
                            try:
                                moves.add_move(self._traverse_right_king(r + 1, ROWS, 1, color, right+1, last + skipped))
                            except RecursionError:
                                break
                    else:
                    # When moving down:
                        # Up diagonal:
                        if self._enemy_piece_on_diagonal(r - 1, -1, -1, color, right, False):
                            try:
                                moves.add_move(self._traverse_right_king(r - 1, -1, -1, color, right+1, last + skipped))
                            except RecursionError:
                                break
                        # Down diagonal:
                        if self._enemy_piece_on_diagonal(r + 1, ROWS, 1, color, right, True):
                            try:
                                moves.add_move(self._traverse_left_king(r + 1, ROWS, 1, color, right-1, last + skipped))
                            except RecursionError:
                                break

            elif current.color == color:
            # Breaking when hitting a friendly color
                break
            elif last:
            # Breaking when hitting 2 enemy pieces in a row
                break
            else:
                last = [current]

            right += 1

        return moves


    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = Moves()
        last = []
        for r in range(start, stop, step):
            # Ends the search if hit the left wall
            if left < 0:
                break

            current = self.board[r][left]

            # If the target tile is empty
            if current == None:
                # If already skipped something and there are no moves left, ends the search
                if skipped and not last:
                    break
                # If already skipped something and there's an option to double jump, adds the next piece to the pieces you can eat
                elif skipped:
                    captured_piece = skipped + last
                    if not last: # Records empty moves
                        moves.add_move(Move(r, left, captured_piece))
                    else:
                        if not captured_piece.count(last[0]) > 1: # Checks if a piece has been captured more than once to avoid infinite recursion
                            moves.add_move(Move(r, left, captured_piece))
                else:
                    # Adds the move
                    moves.add_move(Move(r, left, last))

                if last:
                    try:
                        if step == -1:
                            row = max(r-3, -1)
                        else:
                            row = min(r+3, ROWS)

                        # If there's an option to eat a piece, activates the method again to see if there are any double jumps available
                        moves.add_move(self._traverse_left(r + step, row, step, color, left-1, skipped = last + skipped))
                        moves.add_move(self._traverse_right(r + step, row, step, color, left+1, skipped = last + skipped))

                        if backwards_eating_in_doubles:
                            step = -step
                            if step == -1:
                                row = max(r-3, -1)
                            else:
                                row = min(r+3, ROWS)

                            moves.add_move(self._traverse_left(r + step, row, step, color, left-1, skipped = last + skipped))
                            moves.add_move(self._traverse_right(r + step, row, step, color, left+1, skipped = last + skipped))
                    except RecursionError:
                        return moves
                break

            # If the tile is not empty, checks if on it is a same colored piece.
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = Moves()
        last = []
        for r in range(start, stop, step):
            # Ends the search if hit the right wall
            if right >= COLS:
                break

            current = self.board[r][right]

            # If the target tile is empty
            if current == None:
                # If already skipped something and there are no moves left, ends the search
                if skipped and not last:
                    break
                # If already skipped something and there's an option to double jump, adds the next piece to the pieces you can eat
                elif skipped:
                    captured_piece = skipped + last
                    if not last: # Records empty moves
                        moves.add_move(Move(r, right, captured_piece))
                    else:
                        if not captured_piece.count(last[0]) > 1: # Checks if a piece has been captured more than once to avoid infinite recursion
                            moves.add_move(Move(r, right, captured_piece))
                else:
                    # Adds the move
                    moves.add_move(Move(r, right, last))

                if last:
                    try:
                        if step == -1:
                            row = max(r-3, -1)
                        else:
                            row = min(r+3, ROWS)

                        # If there's an option to eat a piece, activates the method again to see if there are any double jumps available
                        moves.add_move(self._traverse_left(r + step, row, step, color, right-1, skipped = last + skipped))
                        moves.add_move(self._traverse_right(r + step, row, step, color, right+1, skipped = last + skipped))

                        if backwards_eating_in_doubles:
                            step = -step
                            if step == -1:
                                row = max(r-3, -1)
                            else:
                                row = min(r+3, ROWS)

                            moves.add_move(self._traverse_left(r + step, row, step, color, right-1, skipped = last + skipped))
                            moves.add_move(self._traverse_right(r + step, row, step, color, right+1, skipped = last + skipped))
                    except RecursionError:
                        return moves
                break

            # If the tile is not empty, checks if on it is a same colored piece.
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves