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

from globals import *
import board

################################################################################
# Private
def _is_boundary(dimension):
    return (dimension % SUB_SQUARE_DIM) == (SUB_SQUARE_DIM-1)

def _make_divider(symbol):
    return (symbol + ('===' * SUB_SQUARE_DIM)) * SUB_SQUARE_DIM + symbol

################################################################################
# Public
def print_board_raw(board):
    print board # DEBUG

def print_board(board):
    for row in range(BOARD_DIM):
        print(board[row * BOARD_DIM : ((row+1) * BOARD_DIM)])

def draw_board(board):
    ext_divider = _make_divider('+')
    int_divider = _make_divider('|')
    print ext_divider
    for row in range(BOARD_DIM):
        line = '|'
        for col in range(BOARD_DIM):
            elem = get_raw_elem(board, row,col)
            line += ' ' + str(elem) if elem != 0 else '__'
            if (_is_boundary(col)):
                line += ' |'
            else:
                line += ' '
        print line
        if (_is_boundary(row)):
            print ext_divider
