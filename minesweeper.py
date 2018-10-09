#!/usr/bin/python3

import sys
import random

ROW_COUNT 	= 16
COL_COUNT 	= 30
MINE_COUNT 	= 99

CELL_CLOSED 	= '-'
CELL_OPEN 	= ' '
CELL_MINE 	= 'M'
CELL_INVALID 	= 'I'
CELL_MARK 	= 'X'
CELL_BOMB 	= 'O'

ACTION_OPEN 	= 'O'
ACTION_MARK 	= 'M'
ACTION_UNMARK 	= 'U'
ACTION_CANCEL 	= 'C'


def debug(msg):
	print(msg)

class game:
	def __init__(self, row, col, mine):
		self.open_count = 0
		self.found = 0
		self.rows = []
		self.cols = []
		self.row_count = row
		self.col_count = col
		self.mine_count = mine
		self.init_board()
		self.set_mines()

	def init_board(self):
		self.board = []
		row = []
		for i in range(self.col_count):
			row.append(CELL_CLOSED)
			self.cols.append(i + 1)

		for i in range(self.row_count):
			self.board.append(row.copy())
			self.rows.append(chr(ord('A') + i))

	def set_mines(self):
		mines = 0
		while mines < self.mine_count:
			row = random.randint(0, self.row_count-1)
			col = random.randint(0, self.col_count-1)
			#debug("cell:"+str(row)+", "+str(col))
			cell = self.get_cell(row, col)
			if cell != CELL_MINE :
				mines = mines + 1
				self.set_cell(row, col, CELL_MINE)

	def print_board(self, is_real = False):
		col = ""
		for i in range(self.col_count):
			if i < 9:
				col += "  " + str(self.cols[i])
			else:
				col += " " + str(self.cols[i])

		print(" " + col)

		for i in range(self.row_count):
			row = ""
			for j in range(self.col_count):
				cell = self.get_cell(i, j)
				if is_real == False:
					if cell == CELL_MINE:
						cell = CELL_CLOSED
					elif cell == CELL_INVALID:
						cell = CELL_MARK
				
				row += "  " + cell
				
			print(self.rows[i] + "" + row)

	def read_row(self):
		while True:
			row = input("Enter row:")
			if ord(row[0]) < ord('A') or ord(row[0]) >= (ord('A') + self.row_count):
				print("Invalid row:" + row)
				continue;
			return ord(row[0]) - ord('A')

	def read_col(self):
		while True:
			col = input("Enter col:")
			try:
				col = int(col)
			except ValueError:
				print("Invalid value:" + col)
				continue

			if col < 1 or col > self.col_count:
				print("Invalid col:" + str(col))
				continue;
			return col - 1

	def read_action(self):
		while True:
			row = input("Enter action (O:Open, M:Mark, U:Unmark, C:Cancel):")
			if row[0] == ACTION_OPEN or row[0] == ACTION_MARK or row[0] == ACTION_UNMARK or row[0] == ACTION_CANCEL:
				return row[0]
			else:
				print("Invalid action:"+row)
	def get_cell(self, row, col):
		return self.board[row][col]

	def set_cell(self, row, col, val):
		self.board[row][col] = val

	def get_mine_count(self, row, col):
		cnt = 0;
		for i in (-1, 0, 1):
			if (row + i) < 0 :
				continue
			if (row + i) >= self.row_count :
				continue
			
			for j in (-1, 0, 1):
				if (col + j) < 0:
					continue
				if (col + j) >= self.col_count:
					continue
				cell = self.get_cell(row + i, col + j)
				if cell == CELL_MINE or cell == CELL_MARK:
					cnt += 1

		return cnt

	def open_cell(self, row, col):
		if row < 0 or row > self.row_count:
			return

		if col < 0 or col > self.col_count:
			return

		cnt = self.get_mine_count(row, col)
		if cnt != 0:
			self.set_cell(row, col, str(cnt))
			self.open_count += 1
			return

		self.set_cell(row, col, CELL_OPEN)
		self.open_count += 1

		for i in (-1, 0, 1):
			for j in (-1, 0 , 1):
				if self.get_cell(row + i, col + j) == CELL_CLOSED :
					self.open_cell(row + i, col + j)

	def play(self):
		self.print_board(True)
		while True:
			self.print_board(False)
			row = self.read_row();
			#debug(str(row))
			col = self.read_col();
			#debug(str(col))
			action = self.read_action();
			#debug(str(action))

			cell = self.get_cell(row, col)
			if action == ACTION_OPEN:
				if cell == CELL_MINE :
					self.set_cell(row, col, CELL_BOMB)
					print("You lost!!!")
					break
				elif cell == CELL_CLOSED :
					self.open_cell(row, col)
				else:
					print("You cannot open this cell!")

			elif action == ACTION_MARK:
				if cell == CELL_MINE:
					self.set_cell(row, col, CELL_MARK)
					self.found += 1
				elif cell == CELL_CLOSED:
					self.set_cell(row, col, CELL_INVALID)
					self.found += 1
				else:
					print("You cannot mark this cell!")

			elif action == ACTION_UNMARK:
				if cell == CELL_INVALID :
					self.set_cell(row, col, CELL_CLOSED)
					self.found -= 1
				elif cell == CELL_MARK :
					self.set_cell(row, col, CELL_MINE)
					self.found -= 1
				else:
					print("You cannot unmark this cell")

			elif action == ACTION_CANCEL:
				debug("action is cancel, do nothing")
			
			if self.found == self.mine_count and self.open_count == ((self.row_count * self.col_count) - self.mine_count) :
				print("You won!!!")
				break
			else:
				print("Found:"+ str(self.found) + " , Open:"+ str(self.open_count))

		self.print_board(True)



def main():
	game(ROW_COUNT, COL_COUNT, MINE_COUNT).play()

if __name__ == "__main__":
	main()
