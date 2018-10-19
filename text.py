#!/usr/bin/python3

import sys
import random
import json
from minesweeper import *

ACTION_OPEN 	= 'O'
ACTION_MARK 	= 'M'
ACTION_UNMARK 	= 'U'
ACTION_CANCEL 	= 'C'
ACTION_DUMP 	= 'D'
ACTION_EXIT 	= 'E'



class GameText(MineSweeper):
	def __init__(self, row, col, mine):
		return MineSweeper.__init__(self, row, col, mine)

	def message(self, msg):
		print(msg)


	def update_cell(self, row, col, is_real=False):
		#do nothing in text mode
		return


	def print_board(self, is_real = False):
		col = ""
		for i in range(self.col_count):
			if i < 9:
				col += "  "
			else:
				col += " "
			col +=  str(self.cols[i])

		print(" " + col)

		for i in range(self.row_count):
			row = ""
			for j in range(self.col_count):
				cell = self.get_cell(i, j)
				val = cell.get_str_val()
				if cell.is_open():
					if is_real:
						val = cell.get_str_real_val()
				else:
					if cell.is_marked() == False:
						val = "-"

					if is_real:
						val = cell.get_str_real_val()

				row += "  " + val

			print(self.rows[i] + row)

	def read_row(self):
		while True:
			row = input("Enter row:")
			if len(row) <= 0:
				continue
			if ord(row[0]) < ord('A') or ord(row[0]) >= (ord('A') + self.row_count):
				self.message("Invalid row:" + row)
				continue;
			return ord(row[0]) - ord('A')

	def read_col(self):
		while True:
			col = input("Enter col:")
			try:
				col = int(col)
			except ValueError:
				self.message("Invalid value:" + col)
				continue

			if col < 1 or col > self.col_count:
				self.message("Invalid col:" + str(col))
				continue;
			return col - 1

	def read_action(self):
		while True:
			action = input("Enter action (O:Open, M:Mark, U:Unmark, C:Cancel):")
			if len(action) <= 0:
				continue
			if action[0] == ACTION_OPEN or action[0] == ACTION_MARK or \
			   action[0] == ACTION_UNMARK or action[0] == ACTION_CANCEL or \
			   action[0]==ACTION_DUMP or action[0]==ACTION_EXIT:
				return action[0]
			else:
				self.message("Invalid action:"+action)
	def play(self):
		while True:
			self.print_board(False)
			row = self.read_row();
			col = self.read_col();
			action = self.read_action();

			if action == ACTION_OPEN:
				if self.open(row, col) == False :
					self.message("You Lost!!!")
					break
			elif action == ACTION_MARK:
				self.mark(row, col)
			elif action == ACTION_UNMARK:
				self.unmark(row, col)
			elif action == ACTION_CANCEL:
				debug("action is cancel, do nothing")
			elif action == ACTION_DUMP:
				self.print_board(True)
			elif action == ACTION_EXIT:
				break
			else:
				self.message("Unknown action:"+action)

			if self.check_win() == True:
				self.message("You won!!!")
				break
			else:
				print("Found:"+ str(self.found) + " , Open:"+ str(self.open_count))

		self.print_board(True)


def main():
	global game
	game = GameText(16, 30, 99)
	game.play()

if __name__ == "__main__":
	main()
