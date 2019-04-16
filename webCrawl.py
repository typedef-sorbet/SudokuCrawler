from selenium import webdriver
import sudoku
import time

if __name__ == "__main__":
	"""
	Open the sudoku page, solve the puzzle, and enter in the data.
	"""

	driver = webdriver.Firefox()

	driver.get("https://nine.websudoku.com/?level=1")


	while True:

		givensDict = {}

		# grab the data

		for row in range(9):
			for col in range(9):
				webCell = driver.find_element_by_xpath('//*[@id="f' + str(col) + str(row) + '"]')
				cellValue = webCell.get_property('value')
				if cellValue:
					givensDict[str((row, col))] = int(cellValue)

		board = sudoku.Board(9, givensDict)

		print("Solving the following board:")
		print(str(board))

		# solve the puzzle

		board.solve()

		# enter the data

		for row in range(9):
			for col in range(9):
				solutionCell = board.getCellAt(row, col)
				webCell = driver.find_element_by_xpath('//*[@id="f' + str(col) + str(row) + '"]')
				if not webCell.get_property('readonly'):
					webCell.send_keys(str(solutionCell.val))

		time.sleep(1)

		driver.find_element_by_xpath('//*[@name="submit"]').click()

		time.sleep(1)

		driver.find_element_by_xpath('//*[@name="newgame"]').click()

		time.sleep(1)