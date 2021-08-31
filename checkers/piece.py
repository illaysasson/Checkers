import pygame
from pygame.math import Vector2
from .constants import WHITE, BLACK, SQUARE_SIZE, PIECE_RADIUS, KING_PADDING
from .utility import position_to_notation

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.notation = position_to_notation(row, col)
        self.color = color
        self.king = False

        self.pos = Vector2(0, 0)
        self.calc_pos()
    
    # Calculates the piece's position based on row and col
    def calc_pos(self):
        self.pos.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.pos.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    # Makes the piece a king
    def make_king(self):
        self.king = True

    # Draws the piece
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.pos.x, self.pos.y), PIECE_RADIUS)
        
        if (self.king):
            if (self.color == WHITE):
                pygame.draw.circle(win, BLACK, (self.pos.x, self.pos.y), PIECE_RADIUS - KING_PADDING)
            else:
                pygame.draw.circle(win, WHITE, (self.pos.x, self.pos.y), PIECE_RADIUS - KING_PADDING)
            pygame.draw.circle(win, self.color, (self.pos.x, self.pos.y), PIECE_RADIUS/2)

    # Moves the piece
    def move(self, row, col):
        self.row = row
        self.col = col
        self.notation = position_to_notation(row, col)

        self.calc_pos()

    def get_piece_color(self):
        return "White" if self.color == WHITE else "Black"

    # For example will return: "White King 4"
    def __repr__(self):
        if (self.king):
            return self.get_piece_color() + " King " + str(self.notation)
        else:
            return self.get_piece_color() + " Piece " + str(self.notation)
