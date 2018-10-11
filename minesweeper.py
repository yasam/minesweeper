#!/usr/bin/python3

import sys
import random
import json

CELL_CLOSED 	= '-'
CELL_OPEN 	= ' '
CELL_MINE 	= 'M'
CELL_INVALID 	= 'I'
CELL_MARK 	= 'X'
CELL_BOMB 	= 'O'


class MineSweeper:
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

	def get_cell(self, row, col):
		return self.board[row][col]

	def set_cell(self, row, col, val):
		self.board[row][col] = val

	def check_win(self):
		if self.found == self.mine_count and self.open_count == ((self.row_count * self.col_count) - self.mine_count) :
			return True
		return False

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
		if row < 0 or row >= self.row_count:
			return

		if col < 0 or col >= self.col_count:
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
				if (row + i)  >= self.row_count or (row + i) < 0:
				    continue
				if (col + j)  >= self.col_count or (col + j) < 0:
				    continue
				if self.get_cell(row + i, col + j) == CELL_CLOSED :
					self.open_cell(row + i, col + j)
	def open(self, row, col):
		cell = self.get_cell(row, col)
		if cell == CELL_MINE :
			self.set_cell(row, col, CELL_BOMB)
			# You lost !!!
			return False
		elif cell == CELL_CLOSED :
			self.open_cell(row, col)
		else:
			self.message("You cannot open this cell!")
		return True

	def mark(self, row, col):
		cell = self.get_cell(row, col)
		if cell == CELL_MINE:
			self.set_cell(row, col, CELL_MARK)
			self.found += 1
		elif cell == CELL_CLOSED:
			self.set_cell(row, col, CELL_INVALID)
			self.found += 1
		else:
			self.message("You cannot mark this cell!")

	def unmark(self, row, col):
		cell = self.get_cell(row, col)
		if cell == CELL_INVALID :
			self.set_cell(row, col, CELL_CLOSED)
			self.found -= 1
		elif cell == CELL_MARK :
			self.set_cell(row, col, CELL_MINE)
			self.found -= 1
		else:
			self.message("You cannot unmark this cell!")

	def message(self, msg):
		raise NotImplementedError("Subclass must implement abstract method!!!")


