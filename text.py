#!/usr/bin/python3

import sys
import random
import json
import argparse

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
		# default, "green", "yellow", "blue", "magenta", "cyan", "light red", "light magenta", "red", "dark gray"
		colors = ['\033[39m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\33[36m', '\033[91m', '\033[95m' , '\033[31m']
		bgnormal = '\033[49m'
		bgclosed = '\033[100m'
		bgopen = '\033[47m'

		col = ""
		for i in range(self.col_count):
			if i < 9:
				col += " "

			col +=  str(self.cols[i]) + " "

		print(" " + col)

		for i in range(self.row_count):
			row = ""
			for j in range(self.col_count):
				cell = self.get_cell(i, j)
				val = cell.get_str_val()

				color = ""
				if cell.is_open() == False and cell.is_marked() == False:
					val = "."
					bgcolor = bgclosed
				else:
					color = colors[cell.get_mine_count()]
					bgcolor = bgopen

				if is_real:
					val = cell.get_str_real_val()

				row += bgcolor+color + " " + val + " " + colors[0] + bgnormal

			print(self.rows[i] + row)

	def read_row(self):
		while True:
			row = input("Enter row:")
			if len(row) <= 0:
				continue

			if row[0] in self.rows :
				return ord(row[0]) - ord('A')

			self.message("Invalid row:" + row)


	def read_col(self):
		while True:
			col = input("Enter col:")
			try:
				col = int(col)
			except ValueError:
				self.message("Invalid value:" + col)
				continue

			if 1 < = col <= self.col_count:
				return col - 1

			self.message("Invalid col:" + str(col))


	def read_action(self):
		actions = [ACTION_OPEN, ACTION_MARK, ACTION_UNMARK, ACTION_CANCEL, ACTION_DUMP, ACTION_EXIT]
		while True:
			action = input("Enter action (O:Open, M:Mark, U:Unmark, C:Cancel):")
			if len(action) <= 0:
				continue

			if action[0] in actions :
				return action[0]
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
	argparser = argparse.ArgumentParser()
	argparser.add_argument("-r", "--row", help="rows count", type=int, default=16)
	argparser.add_argument("-c", "--col", help="cols count", type=int, default=30)
	argparser.add_argument("-m", "--mine", help="mines count", type=int, default=99)

	args = argparser.parse_args()

	game = GameText(args.row, args.col, args.mine)
	game.play()

if __name__ == "__main__":
	main()

