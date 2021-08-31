from checkers.utility import position_to_notation
import pygame
from .constants import WHITE, BLACK, GREEN_TILE, SQUARE_SIZE, AI_PLAYER, move_sound, capture_sound, multi_capture_sound, game_start_sound, game_end_sound, king_sound
from .board import Board
from .move import Move, Moves
from .settings import srufim

class Game:
    def __init__(self, win):
        self._init()
        game_start_sound.play()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        if (self.selected):
            self.draw_valid_moves()
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = Moves()

    def winner(self):
        winner = self.board.winner(self.turn)
        if winner is not None:
            self.turn = None
            game_end_sound.play()
            if winner == BLACK:
                print('Black wins!')
            else:
                print('White wins!')
        return winner

    def reset(self):
        self._init()

    def select(self, row, col):
        # If there's already a selected piece, try to move the piece to a selected square
        if self.selected:
            result = self._move(row, col)
            # If moving didn't work make self.selected empty and activate the function again
            if not result:
                self.selected = None
                self.select(row, col)
        # If there's nothing selected then select the piece and get its valid moves
        piece = self.board.get_piece(row, col)
        if piece != None and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        # This will be the target tile in the target row and col, and will be used to check if the row and col are available
        target_tile = self.board.get_piece(row, col)
        
        if srufim:
            srufim_moves = self.board.filter_srufim(self.turn)
            move = srufim_moves.get_move(row, col) 
            if move is None: # If move doesn't exist, then moving failed
                return False
        else:
            move = self.valid_moves.get_move(row, col)

        if self.selected and target_tile == None and move is not None:
            #move.print_move(self.selected.color, position_to_notation(self.selected.row, self.selected.col))
            self.board.move(self.selected, move.target[0], move.target[1])

            skipped = move.skipped
            # Only plays the moving sounds if no pieces were captured. if a piece was captured, play the capture sound instead.
            if skipped:
                self.board.remove(skipped)

                if not self.winner():
                    if len(skipped) > 1:
                        multi_capture_sound.play()
                    else:
                        capture_sound.play()
            else:
                move_sound.play()
            self.change_turn()
            return True
        else:
            return False

    def draw_valid_moves(self):
        if srufim:
            srufim_moves = self.board.filter_srufim(self.turn)
            for move in self.valid_moves.moves:
                if srufim_moves.does_move_exist(move):
                    row, col = move.target[0], move.target[1]
                    pygame.draw.rect(self.win, GREEN_TILE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        else:
            for move in self.valid_moves.moves:
                row, col = move.target[0], move.target[1]
                pygame.draw.rect(self.win, GREEN_TILE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

        self.valid_moves = Moves()

    def get_board(self):
        return self.board
    
    def ai_move(self, board):
        old_friendly_kings = self.board.black_kings if AI_PLAYER == BLACK else self.board.white_kings
        old_enemy_pieces = self.board.white_left if AI_PLAYER == BLACK else self.board.black_left

        self.board = board

        new_friendly_kings = self.board.black_kings if AI_PLAYER == BLACK else self.board.white_kings
        new_enemy_pieces = self.board.white_left if AI_PLAYER == BLACK else self.board.black_left

        # For sounds:
        if new_friendly_kings > old_friendly_kings: # If the num of friendly kings changed, then a piece was promoted
            king_sound.play()
        
        if old_enemy_pieces - new_enemy_pieces > 1: # If the enemy is missing more than 1 piece, then a multi capture occured
            multi_capture_sound.play()
        elif old_enemy_pieces - new_enemy_pieces > 0: # If the enemy is missing a single piece, then a capture occured
            capture_sound.play()
        else: # If no captures occured then just play the regular move sound
            move_sound.play()

        self.change_turn()
        self.winner()