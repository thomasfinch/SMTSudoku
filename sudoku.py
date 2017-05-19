#!/usr/bin/python

import math, z3
from itertools import product

def printPuzzle(puzzle):
	puzzleSize = len(puzzle)
	subSquareSize = int(math.sqrt(puzzleSize))
	puzzleStr = ''
	borderStr = (('+' + ('-' *  subSquareSize * 3)) * subSquareSize) + '+\n'

	for row in range(puzzleSize):
		if row % subSquareSize == 0:
			puzzleStr += borderStr

		for col in range(puzzleSize):
			if col % subSquareSize == 0:
				puzzleStr += '|'

			num = puzzle[row][col]
			numStr = str(num) if num != 0 else '.'
			puzzleStr += ' ' + numStr + ' '

		puzzleStr += '|\n'

	puzzleStr += borderStr

	print(puzzleStr)

def verifyPuzzle(puzzle):
	puzzleSize = len(puzzle)

	# Make sure the puzzle is square
	assert(int(math.sqrt(puzzleSize)) == math.sqrt(puzzleSize))

	for row in puzzle:
		# Make sure each row is the right size
		assert(len(row) == puzzleSize)

		# Make sure each number is in the right range
		for number in row:
			assert(number >= 0 and number <= puzzleSize)

def solvePuzzle(puzzle):
	puzzleSize = len(puzzle)
	solver = z3.Solver()

	# Create symbolic variables for each cell
	cellVars = [[z3.Int('r' + str(row) + 'c' + str(col)) for col in range(puzzleSize)] for row in range(puzzleSize)]

	for row, col in product(range(puzzleSize), range(puzzleSize)):
		# If this cell is known, add its value to the solver
		if puzzle[row][col] != 0:
			solver.add(cellVars[row][col] == puzzle[row][col])
			continue

		# Cell values must be >= 1 and <= puzzleSize
		solver.add(cellVars[row][col] >= 1)
		solver.add(cellVars[row][col] <= puzzleSize)

		for i in range(puzzleSize):
			# Cell must not equal anything in its row
			if i != col:
				solver.add(cellVars[row][col] != cellVars[row][i])

			# Cell must not equal anything in its column
			if i != row:
				solver.add(cellVars[row][col] != cellVars[i][col])

		# Cell must not equal anything in its sub-square
		subSquareSize = int(math.sqrt(puzzleSize))
		subSquareCoords = lambda r, c: (int(r) / subSquareSize, int(c) / subSquareSize)
		for row2, col2 in product(range(puzzleSize), range(puzzleSize)):
			if not (row2 == row and col2 == col) and subSquareCoords(row2, col2) == subSquareCoords(row, col):
				solver.add(cellVars[row][col] != cellVars[row2][col2])

	if str(solver.check()) == 'unsat':
		return None
	else:
		model = solver.model()
		solvedPuzzle = [[0] * puzzleSize for i in range(puzzleSize)]

		for row, col in product(range(puzzleSize), range(puzzleSize)):
			solvedPuzzle[row][col] = model[cellVars[row][col]].as_long()

		return solvedPuzzle

def main():
	# Easy puzzle (4 x 4)
	# 0 = unknown
	easyPuzzle = [
		[0, 3, 0, 1],
		[1, 0, 3, 2],
		[3, 0, 1, 0],
		[0, 1, 0, 3]
	]

	# Normal puzzle (9 x 9)
	normalPuzzle = [
		[8, 0, 0, 4, 0, 6, 0, 0, 7],
		[0, 0, 0, 0, 0, 0, 4, 0, 0],
		[0, 1, 0, 0, 0, 0, 6, 5, 0],
		[5, 0, 9, 0, 3, 0, 7, 8, 0],
		[0, 0, 0, 0, 7, 0, 0, 0, 0],
		[0, 4, 8, 0, 2, 0, 1, 0, 3],
		[0, 5, 2, 0, 0, 0, 0, 9, 0],
		[0, 0, 1, 0, 0, 0, 0, 0, 0],
		[3, 0, 0, 9, 0, 2, 0, 0, 5]
	]

	# Empty puzzle (will generate a valid size x size puzzle)
	size = 9
	emptyPuzzle = [[0] * size] * size

	puzzle = normalPuzzle

	verifyPuzzle(puzzle)
	
	print('Input puzzle:')
	printPuzzle(puzzle)

	print('Solving...')
	solved = solvePuzzle(puzzle)

	if solved is None:
		print('No solution :(')
	else:
		print('Solved!\n')
		printPuzzle(solved)

if __name__ == '__main__':
	main()
