from globals import *

################################################################################
# Board evaluation
def _has_violations(row_or_col):
    '''Returns True if there is a violation'''
    non_zeros = non_zero(row_or_col)
    return len(non_zeros) != len(set(non_zeros))

def evaluate_row_col(board, sstop_left):
    '''Returns True if no elements in the row,col of the subsquare violates the row and col sudoku rules'''
    top_left = ss_to_raw(sstop_left)
    for pivot_row in xrange (top_left[0], top_left[0] + SUB_SQUARE_DIM):
        if _has_violations(fetch_raw_row(board, pivot_row)):
            return False

    for pivot_col in xrange (top_left[1], top_left[1] + SUB_SQUARE_DIM):
        if _has_violations(fetch_raw_col(board, pivot_col)):
            return False

    return True

def _evaluate_subsquare(board, sstop_left):
    '''Returns True if element at raw top_left does not violate the subsquare sudoku rules'''
    return not _has_violations(fetch_subsquare(board, sstop_left))

def _get_candidate_set(board, row, col, possible_set):
    '''Returns set of non-zero potential candidates by raw row and col'''
    row_array = non_zero(fetch_raw_row(board,row))
    col_array = non_zero(fetch_raw_col(board,col))
    return possible_set ^ set(row_array + col_array) # symmetric difference

def solve_subsquare(board, sstop_left, seed_set):
    '''Returns unique solution for subsquare if any. Returns None otherwise'''
    top_left = ss_to_raw(sstop_left)
    unique_solution = []
    for row in xrange(top_left[0], top_left[0] + SUB_SQUARE_DIM):
        for col in xrange(top_left[1], top_left[1] + SUB_SQUARE_DIM):
            candidates = _get_candidate_set(board, row, col, seed_set)
            if len(candidates) == 1:
                unique_solution.extend(list(candidates))
            else:
                return None

    return unique_solution

def _is_element_valid(board, row_col):
    '''Returns True if element at raw (row col) respects the SUDOKU rules'''
    if _has_violations(fetch_raw_row(board, row_col[0])):
        return False

    if _has_violations(fetch_raw_col(board, row_col[1])):
        return False

    return _evaluate_subsquare(board, raw_to_ss(row_col))

################################################################################
# Solution discovery
def _solve(board, targets, index, possible_set):
    '''Creates SUDOKU solutions in place. Returns True if solution is feasible'''
    row = targets[index][0]
    col = targets[index][1]
    available_set = _get_candidate_set(board, row, col, possible_set)

    if len(available_set) == 0:
        return False

    for possibility in available_set:
        board[raw_addr(row,col)] = possibility

        if index == len(targets)-1:
            return True # solution is viable (nothing left to try)

        if _solve(board, targets, index + 1, possible_set):
            return True # solution is viable (subtree )
        else:
            board[raw_addr(row,col)] = 0

    return False

################################################################################
# Public
def solve(board):
    '''Creates SUDOKU solutions in place. Returns True if solution is feasible'''
    possible_set = set(range(1, BOARD_DIM + 1))
    targets = [row_col(i) for i in xrange(BOARD_DIM * BOARD_DIM) if board[i] == 0]
    return _solve(board, targets, 0, possible_set)

def validate(board):
    '''Returns True if the SUDOKU board is valid'''
    for i in xrange(BOARD_DIM * BOARD_DIM):
        if not _is_element_valid(board, row_col(i)):
            return False

    return True
