#!/usr/bin/python3

import sys
import random
import json
import copy

class Cell:
	def __init__(self):
		self.__open = False
		self.__mine = False
		self.__mine_count = 0
		self.__mark = False
		self.__bomb = False
		self.__str_val = " "
		self.__str_real_val = " "

	def open(self):
		self.__open = True
		self.update_str_val()

	def mark(self):
		self.__mark = True
		self.update_str_val()

	def unmark(self):
		self.__mark = False
		self.update_str_val()

	def set_mine(self):
		self.__mine = True
		self.update_str_val()

	def set_bomb(self):
		self.__bomb = True
		self.update_str_val()

	def set_mine_count(self, count):
		self.__mine_count = count
		self.update_str_val()

	def is_open(self):
		return self.__open

	def is_marked(self):
		return self.__mark

	def is_mine(self):
		return self.__mine

	def is_bomb(self):
		return self.__bomb

	def get_mine_count(self):
		return self.__mine_count

	def get_str_val(self):
		return self.__str_val

	def get_str_real_val(self):
		return self.__str_real_val

	def update_str_val(self):
		val = " "
		real_val = " "
		if self.is_open() :
			cnt = self.get_mine_count()
			if cnt != 0 :
				val = str(cnt)
				real_val = str(cnt)

		else:
			if self.is_marked():
				val = "X"
				real_val = "X"

			if self.is_bomb():
				val = "O"
				real_val = "O"
			elif self.is_mine():
				if self.is_marked() == False:
					real_val = "M"
			else:
				if self.is_marked():
					real_val = "I"

		self.__str_val = val
		self.__str_real_val = real_val



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
			row.append(Cell())
			self.cols.append(i + 1)

		for i in range(self.row_count):
			self.board.append(copy.deepcopy(row))
			self.rows.append(chr(ord('A') + i))

	def set_mines(self):
		mines = 0
		while mines < self.mine_count:
			row = random.randint(0, self.row_count-1)
			col = random.randint(0, self.col_count-1)
			cell = self.get_cell(row, col)
			#print("cell:"+str(row)+", "+str(col))
			if cell.is_mine() != True :
				mines = mines + 1
				cell.set_mine()
				#print(":::::cell:"+str(row)+", "+str(col))


	def get_cell(self, row, col):
		return self.board[row][col]

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
				if cell.is_mine():
					cnt += 1

		return cnt

	def explore_cell(self, row, col):
		cell = self.get_cell(row, col)
		cnt = self.get_mine_count(row, col)
		cell.open()
		self.open_count += 1
		self.update_cell(row, col)

		if cnt != 0:
			cell.set_mine_count(cnt)
			self.update_cell(row, col)
			return

		for i in (-1, 0, 1):
			if (row + i) >= self.row_count or (row + i) < 0:
			    continue
			for j in (-1, 0 , 1):
				if (col + j) >= self.col_count or (col + j) < 0:
				    continue

				cell = self.get_cell(row + i, col + j)

				if cell.is_open() == False and cell.is_marked() == False:
					self.explore_cell(row + i, col + j)

	def open(self, row, col):
		cell = self.get_cell(row, col)

		if cell.is_open():
			self.message("You cannot open this cell!")
			return True

		if cell.is_mine():
			cell.set_bomb()
			self.update_cell(row, col)
			# You lost !!!
			return False

		self.explore_cell(row, col)

		return True

	def mark(self, row, col):
		cell = self.get_cell(row, col)

		if cell.is_open() or cell.is_marked():
			self.message("You cannot mark this cell!")
			return

		cell.mark()
		self.found += 1
		self.update_cell(row, col)

	def unmark(self, row, col):
		cell = self.get_cell(row, col)
		if cell.is_marked() == False:
			self.message("You cannot unmark this cell!")
			return

		cell.unmark()
		self.found -= 1
		self.update_cell(row, col)


	def message(self, msg):
		raise NotImplementedError("Subclass must implement abstract method!!!")

	def update_cell(self, row, col):
		raise NotImplementedError("Subclass must implement abstract method!!!")


