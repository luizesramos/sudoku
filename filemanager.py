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
