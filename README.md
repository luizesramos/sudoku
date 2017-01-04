# sudoku
Sudoku game generator and solver

```
Usage: ./sudoku.py [discover | full | game <easy|medium|hard> | view file.csv | solve file.csv]
   'discover' attempts to find a valid SUDOKU seed (takes seconds to minutes)
   'full' creates complete SUDOKU board from a known seed
   'game' creates a SUDOKU game at the specified level (easy, medium, or hard)
   'view' prints the SUDOKU puzzle from CSV file
   'solve' solves the SUDOKU puzzle in CSV file
 ```

# discover

Searches iteratively for a valid SUDOKU board by trying to randomly place an
array of unique integers (from 1-9) on the 3x3 sub-squares of the 9x9 board.
We use the following method:

(1) Randomly place the uniques in the center sub-square (1,1);

(0,0) | (0,1) | (0,2)
(1,0) | (1,1) | (1,2)
(2,0) | (2,1) | (2,2)

(2) Attempt to place uniques randomly on the other sub-squares while respecting
the SUDOKU rules. We following the order: left (1,0), right (1,2), top (0,1),
bottom (2,1), top-left (0,0), bottom-left (2,0), bottom-right (2,2).
We adopt a cap on the number of attempts. If at some point the cap is reached,
we go back to (1).

(3) Solve the resulting system for the top-right sub-square (0,2). If
the system is impossible, we go back to (1) and try again.

The search stops when we find a complete SUDOKU board, which we call seed.

Note: this mechanism is meant to find seeds, not to generate SUDOKU boards.
Please see `full` and `game`.

# full

Creates a complete SUDOKU board based on board seeds. A seed is a valid and
complete SUDOKU board. Based on a randomly selected seed from `seed.py`, we can
create an entirely new board by performing random operations that do not break
the validity of the board. The operations we implement here are:

(1) Swapping together all columns of two vertical groups of sub-squares.
For example, we could swap the columns of sub-squares (0,0), (1,0) and (2,0)
respectively with those of sub-squares (0,1), (1,1), and (2,1) without
invalidating the board.

(2) Swapping together all rows of two horizontal groups of sub-squares.

(3) Swapping columns within a vertical group of sub-squares.

(4) Swapping rows within a horizontal group of sub-squares.

# game

Creates a SUDOKU game with three difficulty levels and saves it to a CSV file in
the `puzzles` directory named by date and time. In this work, a game is a
complete (full) board with strategically selected random slots for the user to
figure out. Our strategy to create the slots is to assign a number of empty
slots to each sub-square. The number of slots per sub-square varies from 4-6 for
easy levels and from 5-7 for hard levels.

# view

Draws SUDOKU puzzles from CSV files as a board on the command line.

# solve

Traverses the empty slots in the board and recursively attempts to fill them
with feasible values. The program backtracks if an infeasible solution is found
and shows a solution if one is found.
