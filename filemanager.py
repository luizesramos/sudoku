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
import time
import csv

def read(filename):
    '''Reads a '''
    board = []
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            board.extend([int(x) for x in row])
    return board

def write(board, filename):
    with open(filename, 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(board)

def make_filename():
    return time.strftime("puzzles/%Y%m%d-%H%M%S.csv")
