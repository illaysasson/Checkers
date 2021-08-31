import pygame
import math
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, AI_PLAYER, BLACK, WHITE, PAUSE_TIME
from checkers.game import Game
from checkers.settings import ai_depth
from minimax.algorithm import minimax

FPS = 60

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE

    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == AI_PLAYER:
            pygame.time.wait(PAUSE_TIME)
            pygame.mixer.pause() # To pause moving sounds during AI calculations
            value, new_board = minimax(game.get_board(), ai_depth, -math.inf, math.inf, True) # Value currently unused
            print(value)
            pygame.mixer.unpause()
            game.ai_move(new_board)

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
        
        game.update()

    pygame.quit()

main()