#!/usr/bin/python
import board
import bprint
import sys
import discover
import solver
import filemanager as fman
import time

################################################################################
# Keywords
DISCOVER='discover'
FULL='full'
GAME='game'
EASY='easy'
MEDIUM='medium'
HARD='hard'
VIEW='view'
SOLVE='solve'

################################################################################
# Util
def help(name):
    options = (DISCOVER, FULL, GAME, EASY, MEDIUM, HARD, VIEW, SOLVE)
    tab = '  '
    print 'Usage:', name, '[%s | %s | %s <%s|%s|%s> | %s file.csv | %s file.csv]' % options
    print tab, '\'%s\' attempts to find a valid SUDOKU seed (takes seconds to minutes)' % DISCOVER
    print tab, '\'%s\' creates complete SUDOKU board from a known seed' % FULL
    print tab, '\'%s\' creates a SUDOKU game at the specified level (%s, %s, or %s)' % (GAME, EASY, MEDIUM, HARD)
    print tab, '\'%s\' prints the SUDOKU puzzle from CSV file' % VIEW
    print tab, '\'%s\' solves the SUDOKU puzzle in CSV file' % SOLVE
    print tab

def get_level_from_arg(arg):
    if arg == EASY:
        return board.LEVEL_EASY
    elif arg == MEDIUM:
        return board.LEVEL_MEDIUM
    elif arg == HARD:
        return board.LEVEL_HARD
    else:
        return None

################################################################################
# Usage
argv = sys.argv
argc = len(argv)
name = argv[0]

error = False
if argc <= 1:
    error = True
elif argv[1] == DISCOVER:
    board = discover.find_seed_board()
    bprint.print_board_raw(board)
elif argv[1] == FULL:
    board = board.make_full_board()
    bprint.draw_board(board)
elif argv[1] == GAME and argc == 3:
    level = get_level_from_arg(argv[2])
    if level == None:
        error = True
    else:
        filename = fman.make_filename()
        board = board.make_game(level)
        print "saved: %s" % filename
        bprint.draw_board(board)
        fman.write(board, filename)
elif argv[1] == VIEW and argc == 3:
    board = fman.read(argv[2])
    bprint.draw_board(board)
elif argv[1] == SOLVE and argc == 3:
    board = fman.read(argv[2])
    bprint.draw_board(board)
    t1 = time.time()
    if not solver.validate(board):
        print 'Invalid board. No solutions.'
    elif solver.solve(board):
        bprint.draw_board(board)
    else:
        print 'Found no solutions for this board.'
    print 'Time: %.2lf s' % (time.time()-t1)
else:
    error = True

if error == True:
    help(name)
