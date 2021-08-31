import pygame
pygame.init()

PAUSE_TIME = 250 # In milliseconds

# FEN - CURRENTLY UNUSED
DEFAULT_FEN = "W:W21,22,23,24,25,26,27,28,29,30,31,32:B1,2,3,4,5,6,7,8,9,10,11,12"

# SIZES
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS
PADDING = 12
KING_PADDING = 10
PIECE_RADIUS = SQUARE_SIZE//2 - PADDING


# COLORS
BACKGROUND = (75, 115, 153)
TILE = (238, 238, 210)
GREEN_TILE = (118, 150, 86)
WHITE = (252, 252, 247)
BLACK = (25, 25, 30)

# AI
AI_PLAYER = BLACK
HUMAN_PLAYER = WHITE if AI_PLAYER == BLACK else BLACK

# TEXT
font = pygame.font.SysFont("Arial", 200, True)
white_wins_text = font.render("White Wins!", True, pygame.Color('Black'))

# SOUNDS
VOLUME = 0.3

def create_sound(path):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(VOLUME)
    return sound

game_start_sound = create_sound('assets/game_start.mp3')
move_sound = create_sound('assets/move.mp3')
capture_sound = create_sound('assets/capture.mp3')
multi_capture_sound = create_sound('assets/multi_capture.mp3')
king_sound = create_sound('assets/king.mp3')
game_end_sound = create_sound('assets/game_end.mp3')


