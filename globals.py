import random

################################################################################
# Global Constants
SUB_SQUARE_DIM = 3
BOARD_DIM = SUB_SQUARE_DIM * SUB_SQUARE_DIM
TOTAL_SUB_SQUARES = BOARD_DIM/SUB_SQUARE_DIM

################################################################################
# Utils
def raw_addr(row, col):
    return (row * BOARD_DIM) + col

def row_col(i):
    return (i / BOARD_DIM, i % BOARD_DIM)

def ss_to_raw(sstop_left):
    '''Converts sub-square address (SUB_SQUARE_DIM**2) to raw board address (BOARD_DIM**2)'''
    return (sstop_left[0] * SUB_SQUARE_DIM, sstop_left[1] * SUB_SQUARE_DIM)

def raw_to_ss(top_left):
    '''Converts a raw board address into the top left of its containing subsquare'''
    return ((top_left[0]/SUB_SQUARE_DIM)*SUB_SQUARE_DIM, (top_left[1]/SUB_SQUARE_DIM)*SUB_SQUARE_DIM)

def get_raw_elem(board, row, col):
    return board[raw_addr(row, col)]

def fetch_raw_row(board, row):
    '''Returns an array with the elements of row'''
    return board[raw_addr(row, 0) : raw_addr(row, BOARD_DIM)]

def fetch_raw_col(board, col):
    '''Returns an array with the elements of col'''
    return [board[raw_addr(row, col)] for row in xrange(BOARD_DIM)]

def fetch_subsquare(board, sstop_left):
    '''Returns an array with the elements of subsquare containing element'''
    return [board[raw_addr(sstop_left[0]+row, sstop_left[1]+col)] for row in xrange(SUB_SQUARE_DIM) for col in xrange(SUB_SQUARE_DIM)]

def non_zero(data):
    '''Returns the data list without zeros'''
    return filter(lambda x: x != 0, data)

def assign_raw_row(board, row, data):
    '''Replaces the elements of row with the elements of data'''
    board[raw_addr(row, 0) : raw_addr(row, BOARD_DIM)] = data

def assign_raw_col(board, col, data):
    '''Replaces the elements of row with the elements of data'''
    for row in xrange(BOARD_DIM):
        board[raw_addr(row, col)] = data[row]

def assign_subsquare(board, sstop_left, sub_square_data):
    top_left = ss_to_raw(sstop_left)
    k = 0
    for row in xrange (top_left[0], top_left[0] + SUB_SQUARE_DIM):
        for col in xrange (top_left[1], top_left[1] + SUB_SQUARE_DIM):
            board[raw_addr(row, col)] = sub_square_data[k]
            k += 1

def clear_subsquare(board, sstop_left):
    assign_subsquare(board, sstop_left, [0] * (SUB_SQUARE_DIM * SUB_SQUARE_DIM))

def clear_board(board):
    for i in xrange(BOARD_DIM * BOARD_DIM):
        board[i] = 0

def random_int(generator, max):
    '''Generates random integer between 0 and max'''
    return int((((generator.random() * 17 * 11) / 13) + 7) % max)
