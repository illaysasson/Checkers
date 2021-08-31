from .constants import ROWS, COLS

def notation_to_position(notation):
    row = (notation-1) // (ROWS//2)
    
    if (row % 2 == 0):
        col = (notation % COLS)*2 - 1
    else:
        col = ((notation - 1) % (COLS//2))*2


    return row, col

def position_to_notation(row, col):
    row, col = row+1, col+1
    if (row % 2 == 0):
        notation = col+1 + ((row - 1)*ROWS)
    else:
        notation = col + ((row - 1)*ROWS)

    notation /= 2

    # Only returns if is a whole number after division
    if (notation - int(notation) == 0):
        return int(notation)