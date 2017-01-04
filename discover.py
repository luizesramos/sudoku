from globals import *
import solver
import random
import time

################################################################################
# Constants
MAX_ATTEMPTS = 15000

################################################################################
# Board building
def _generate_subsquare_unconstrained(board, sstop_left, seed):
    '''Creates a random subsquare with unique elements'''
    random.shuffle(seed)
    assign_subsquare(board, sstop_left, seed)

def _generate_subsquare_constrained(board, sstop_left, seed):
    '''Creates a valid subsquare assuming unique elements'''
    attempts = 1
    while attempts < MAX_ATTEMPTS:
        random.shuffle(seed)
        assign_subsquare(board, sstop_left, seed)
        if (solver.evaluate_row_col(board, sstop_left)):
            break
        else:
            attempts += 1
    return attempts

def _generate_board_solution(board, seed):
    '''Random board generation in the following order: center, left, right, top, bottom, top-left, bottom-left, bottom-right, top-right'''
    seed_set = set(seed)

    # fill center subsquare
    sstop_left = (1,1)
    _generate_subsquare_unconstrained(board, sstop_left, seed)

    # use a sequence to generate the intermediate subsquares
    # left, right, top, bottom, top-left, bottom-left, bottom-right
    sequence = [(1,0), (1,2), (0,1), (2,1), (0,0), (2,0), (2,2)]
    progress = 0
    while progress < len(sequence):
        sstop_left = sequence[progress]
        att = _generate_subsquare_constrained(board, sstop_left, seed)
        print("Subsquare(%d,%d): %d attempts" % (sstop_left[0], sstop_left[1], att))

        if att == MAX_ATTEMPTS:
            return False

        progress += 1

    # solve for the top-right subsquare (the last remaining one)
    sstop_left = (0, 2)
    solution = solver.solve_subsquare(board, sstop_left, seed_set)
    if solution == None:
        print "= No solution"
        return False
    else:
        assign_subsquare(board, sstop_left, solution)
        return True

def find_seed_board():
    '''Iteratively attempts to find a valid SUDOKU board'''
    board = [0] * (BOARD_DIM * BOARD_DIM)
    seed = range(1, BOARD_DIM + 1)
    seedValue = time.time()

    random.seed(seedValue)

    while not _generate_board_solution(board, seed):
        print "=== START SEQUENCE seed:", seedValue, seed
        clear_board(board)
        continue

    return board
