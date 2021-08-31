import pygame
import math
from copy import deepcopy
from checkers.constants import AI_PLAYER, HUMAN_PLAYER
from checkers.settings import srufim, advanced_evalaute

def minimax(position, depth, alpha, beta, max_player):
    # If we've hit the end of the algorithim or the game is over, end the algorithm
    if depth == 0 or position.winner(AI_PLAYER if max_player else HUMAN_PLAYER):
        if advanced_evalaute:
            return position.advanced_evaluate(), position
        else:
            return position.simple_evaluate(), position

    # If max player is true, maximize the score, If false, minimize it
    if max_player:
        maxEval = -math.inf
        best_move = None

        # Evaluate every single move by activating the minimax function recursively, and switching the max_player
        for move in get_all_boards_after_moves(position, AI_PLAYER):
            evaluation = minimax(move, depth-1, alpha, beta, False)[0]

            maxEval = max(maxEval, evaluation)
            # For alpha beta pruning: Checks whether or not this branch needs to be pruned
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
            # If the current move is the best move then set the best move as the current move
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move
    else:
        minEval = math.inf
        best_move = None

        # Evaluate every single move by activating the minimax function recursively, and switching the max_player
        for move in get_all_boards_after_moves(position, HUMAN_PLAYER):
            evaluation = minimax(move, depth-1, alpha, beta, True)[0]

            minEval = min(minEval, evaluation)
            # For alpha beta pruning: Checks whether or not this branch needs to be pruned
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
            # If the current move is the best move then set the best move as the current move
            if minEval == evaluation:
                best_move = move

        return minEval, best_move

def simulate_move(piece, move, board, skip):
# Simulates a move
    board.move(piece, move[0], move[1])

    if skip:
        board.remove(skip)
    
    return board

def get_all_boards_after_moves(board, color):
# Returns all possible move for a color in a board (in board form)
    moves = [] # List of all the boards after every move
    
    if srufim:
        srufim_moves = board.filter_srufim(color)

        for piece in board.get_all_pieces(color):
            valid_moves = board.get_valid_moves(piece)

            for move in valid_moves.moves:
                if not srufim_moves.does_move_exist(move): # If move doesn't exist after srufim filter, skip it
                    continue

                # Copies the board and simulates the move on it
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)

                new_board = simulate_move(temp_piece, move.target, temp_board, move.skipped)
                moves.append(new_board)
    else:
        for piece in board.get_all_pieces(color):
            valid_moves = board.get_valid_moves(piece)

            for move in valid_moves.moves:
                # Copies the board and simulates the move on it
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)

                new_board = simulate_move(temp_piece, move.target, temp_board, move.skipped)
                moves.append(new_board)

    return moves