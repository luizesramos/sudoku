import random as generator
import time
from globals import *
import seeds

################################################################################
# Row, col, and subsquare shuffling
def _select_seed(generator):
    index = random_int(generator, len(seeds.seeds))
    return seeds.seeds[index]

def _intra_ss_row_swap(board, args):
    '''Swaps rows a and b inside a set of subsquares'''
    ssrow = args[0]
    ssoffset_a = args[1]
    ssoffset_b = args[2]

    row_top = ss_to_raw((ssrow, 0))[0]
    top_left_a = row_top + ssoffset_a
    top_left_b = row_top + ssoffset_b

    row_a = fetch_raw_row(board, top_left_a)
    row_b = fetch_raw_row(board, top_left_b)
    assign_raw_row(board, top_left_a, row_b)
    assign_raw_row(board, top_left_b, row_a)

def _intra_ss_col_swap(board, args):
    '''Swaps cols a and b inside a set of subsquares'''
    ssrow = args[0]
    ssoffset_a = args[1]
    ssoffset_b = args[2]

    col_left = ss_to_raw((ssrow, 0))[0]
    top_left_a = col_left + ssoffset_a
    top_left_b = col_left + ssoffset_b

    col_a = fetch_raw_col(board, top_left_a)
    col_b = fetch_raw_col(board, top_left_b)
    assign_raw_col(board, top_left_a, col_b)
    assign_raw_col(board, top_left_b, col_a)

def _ss_swap_all_rows(board, args):
    '''Swaps all rows of subsquares a and b'''
    subsquare_a = args[0]
    subsquare_b = args[1]

    base_a = ss_to_raw((subsquare_a, 0))[0]
    base_b = ss_to_raw((subsquare_b, 0))[0]

    for offset in xrange(SUB_SQUARE_DIM):
        row_a = fetch_raw_row(board, base_a + offset)
        row_b = fetch_raw_row(board, base_b + offset)
        assign_raw_row(board, base_a + offset, row_b)
        assign_raw_row(board, base_b + offset, row_a)

def _ss_swap_all_cols(board, args):
    '''Swaps all cols of subsquares a and b'''
    subsquare_a = args[0]
    subsquare_b = args[1]

    base_a = ss_to_raw((0, subsquare_a))[1]
    base_b = ss_to_raw((0, subsquare_b))[1]

    for offset in xrange(SUB_SQUARE_DIM):
        col_a = fetch_raw_col(board, base_a + offset)
        col_b = fetch_raw_col(board, base_b + offset)
        assign_raw_col(board, base_a + offset, col_b)
        assign_raw_col(board, base_b + offset, col_a)

################################################################################
# Board-transforming operations
valid_operations = [_intra_ss_row_swap, _intra_ss_col_swap, _ss_swap_all_rows, _ss_swap_all_cols]

def _random_pair(generator):
    '''Returns a random pair of indices for swapping'''
    a = random_int(generator, SUB_SQUARE_DIM)
    b = random_int(generator, SUB_SQUARE_DIM)
    if a == b:
        b = (b + 1) % SUB_SQUARE_DIM
    return (a, b)

def _random_operation(generator):
    '''Returns a random valid operation to transform the SUDOKU board'''
    index = random_int(generator, len(valid_operations))
    return valid_operations[index]

def _random_sequence_generator(generator):
    '''Returns random operations with operators'''
    while True:
        operation = _random_operation(generator)
        pair = _random_pair(generator)
        if operation == _intra_ss_row_swap or operation == _intra_ss_col_swap:
            subsquares_at_row = random_int(generator, SUB_SQUARE_DIM)
            yield (operation, (subsquares_at_row, pair[0], pair[1]))
        else:
            yield (operation, pair)

################################################################################
# Level generation

# distribution of white spaces
LEVEL_EASY = (4, 4, 4, 5, 5, 5, 6, 6, 6)
LEVEL_MEDIUM = (5, 5, 5, 5, 5, 6, 6, 6, 6)
LEVEL_HARD = (5, 5, 5, 5, 6, 6, 6, 7, 7)

def _get_mask_for_level(level, index):
    spaces = level[index]
    mask = [ True ] * spaces + [ False ] * (len(level) - spaces)
    generator.shuffle(mask)
    return mask

def _apply_subsquare_mask(board, level, generator):
    '''Applies whitespace (zero) mask on subsquares'''
    k = 0
    for ssrow in xrange(SUB_SQUARE_DIM):
        for sscol in xrange(SUB_SQUARE_DIM):
            sstop_left = (ssrow, sscol)
            top_left = ss_to_raw(sstop_left)
            mask = _get_mask_for_level(level, k)
            k += 1
            ss = fetch_subsquare(board, top_left)
            ss_masked = map(lambda x, y : 0 if x else y, mask, ss)
            assign_subsquare(board, sstop_left, ss_masked)

################################################################################
# Public
def make_full_board():
    generator.seed(time.time())

    # select a random known SUDOKU board as a seed
    board = seeds.seeds[0] #_select_seed(generator)

    # transform the SUDOKU board via random operations
    sequence = _random_sequence_generator(generator)
    for i in xrange(20):
        op = next(sequence)
        op[0](board, op[1])

    return board

def make_game(level):
    board = make_full_board()
    generator.seed(time.time())
    _apply_subsquare_mask(board, level, generator)
    return board
