#!/usr/bin/python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Luiz Ramos
# Date: 1/3/2017

import board as sboard
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
# Subroutines
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
    '''Selects the game type by name. Defaults to easy'''
    if arg == MEDIUM:
        return sboard.LEVEL_MEDIUM
    elif arg == HARD:
        return sboard.LEVEL_HARD
    else:
        return sboard.LEVEL_EASY

def print_time(reference_timestamp):
    print 'Time: %.2lf s' % (time.time()-reference_timestamp)

def option_discovery():
    t1 = time.time()
    board = discover.find_seed_board()
    bprint.print_board_raw(board)
    print_time(t1)

def option_full():
    board = sboard.make_full_board()
    bprint.draw_board(board)

def option_game(level_name):
    level = get_level_from_arg(level_name)
    filename = fman.make_filename()
    board = sboard.make_game(level)
    print "saved: %s" % filename
    bprint.draw_board(board)
    fman.write(board, filename)

def option_view(filename):
    board = fman.read(filename)
    bprint.draw_board(board)

def option_solve(filename):
    board = fman.read(argv[2])
    bprint.draw_board(board)
    t1 = time.time()
    if not solver.validate(board):
        print 'Invalid board. No solutions.'
    elif solver.solve(board):
        bprint.draw_board(board)
    else:
        print 'Found no solutions for this board.'
    print_time(t1)

################################################################################
# Main menu handling
argv = sys.argv
argc = len(argv)
name = argv[0]

error = False
if argc <= 1:
    error = True
elif argv[1] == DISCOVER:
    option_discovery()
elif argv[1] == FULL:
    option_full()
elif argc != 3:
    error = True
elif argv[1] == GAME:
    option_game(argv[2])
elif argv[1] == VIEW:
    option_view(argv[2])
elif argv[1] == SOLVE:
    option_solve(argv[2])
else:
    error = True

if error == True:
    help(name)
