"""
Sudoku puzzle solver.
Hasn't been extensively tested against examples, but seems to work fairly well.
"""

class Cell:
	def __init__(self, row, col, block, val=None):
		self.row = row                      # row number
		self.col = col                      # column number
		self.block = block                  # block number
		if val:                             # if this cell has an given value, initialize possibleVals to a one-number list
			self.possibleVals = [val]
		else:                               # otherwise, this cell could hold any possible value
			self.possibleVals = [i for i in range(1, 10, 1)]
		self.val = val

	def __str__(self):
		return "Cell@<{0}, {1}>: ".format(str(self.row), str(self.col)) + str(self.possibleVals)

class Board:
	def __init__(self, n, givensDict=None):
		"""
		Initializes an n x n to the initial state given by givensDict.
		:param n: Dimension of the board.
		:param givensDict: Dictionary of given values on the board.
		"""
		self.n = n                      # dimension of the board, usually 9
		self.n2 = n ** 2
		self.grid = []                  # List of Cell objects
		for i in range(self.n2):
			row = i // self.n
			col = i % self.n
			block = 3 * (row // 3) + col // 3
			if givensDict and str((row, col)) in givensDict:                            # if there's a given value for this cell, specify it
				self.grid.append(Cell(row, col, block, givensDict[str((row, col))]))
			else:                                                                       # otherwise, just init as empty
				self.grid.append(Cell(row, col, block))

	def __str__(self):
		rows = []
		rowLine = "---+---+---+---+---+---+---+---+---\n"
		for i in range(0, self.n2, self.n):
			rowItems = [str(item.val) if item.val else ' ' for item in self.grid[i:i+self.n]]
			newRowStr = " " + " | ".join(rowItems) + "\n"
			rows.append(newRowStr)
		return rowLine.join(rows)

	def getRowOf(self, cell):
		row = self.grid[cell.row * self.n: (cell.row + 1) * self.n: 1]
		row.remove(cell)
		return row

	def getColOf(self, cell):
		col = self.grid[cell.col:self.n2:self.n]
		col.remove(cell)
		return col

	def getBlockOf(self, cell):
		# can we do better than n2?
		# probably, but I don't wanna go through the calculations right now
		# TODO optimize past O(n2)
		block = [self.grid[i] for i in range(self.n2) if self.grid[i].block == cell.block and self.grid[i] != cell]
		return block

	def getCellAt(self, row, col):
		index = row * 9 + col
		return self.grid[index]

	def isSolved(self):
		for cell in self.grid:
			if not cell.val:
				return False
		return True

	def evaluateCell(self, cell, verbose=False):
		if not cell.val:
			# get the row, column, and block that the cell occupies
			row = self.getRowOf(cell)
			col = self.getColOf(cell)
			block = self.getBlockOf(cell)

			others = []
			others.extend(row)
			others.extend(col)
			others.extend(block)

			for otherCell in others:
				if otherCell.val:
					try:
						cell.possibleVals.remove(otherCell.val)
					except ValueError:
						pass
			if len(cell.possibleVals) == 1:
				cell.val = cell.possibleVals[0]
				if verbose:
					print("Resolved cell: " + str(cell))
					print(str(self))

	def solve(self):
		# assume initial board state is given
		while not self.isSolved():
			for cell in self.grid:
				self.evaluateCell(cell)
		print("Solution found:")
		print(str(self))

# TODO implement a checkpointed "what-if" system that allows alg. to "guess" and see if what results is valid?

if __name__ == "__main__":
	# gather initial state from user
	givensDict = {}
	print("Please specify the initial state of the board.")
	for i in range(9 ** 2):
		row = i // 9
		col = i % 9
		val = int(input("Please give the value at ({0}, {1}) (Enter 0 if no value)".format(str(row), str(col))))
		if val:
			givensDict[str((row,col))] = val

	board = Board(9, givensDict)

	print("Solving the following board:")
	print(str(board))

	board.solve()