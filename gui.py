#!/usr/bin/python3

import sys
import random
import json
from appJar import gui
from tkinter import messagebox

from minesweeper import *

def mouse_left_click( event ):
	game.mouse_left_click(event)

def mouse_right_click( event ):
	game.mouse_right_click(event)

class GameGui(MineSweeper):
	def __init__(self, row, col, mine):
		return MineSweeper.__init__(self, row, col, mine)

	def get_cell_name(self, row, col):
		return str(row).zfill(2) + "-" + str(col).zfill(2)

	def message(self, msg):
		messagebox.showinfo("MineSweeper", msg)

	def mouse_left_click(self, event):
		result = self.open(event.widget.row, event.widget.col)
		self.draw_board()
		if  result == False :
			self.message("You Lost!!!")
			self.app.stop()

		if self.check_win() == True:
			self.message("You won!!!")
			self.app.stop()

	def mouse_right_click(self, event):
		cell = self.get_cell(event.widget.row, event.widget.col)
		if cell == CELL_INVALID or cell == CELL_MARK :
			self.unmark(event.widget.row, event.widget.col)
		else:
			self.mark(event.widget.row, event.widget.col)

		self.draw_board()

		if self.check_win() == True:
			self.message("You won!!!")
			self.app.stop()

	def create_board(self):
		for i in range(self.row_count + 1):
			for j in range(self.col_count + 1):
				l = self.get_cell_name(i, j)
				lbl = self.app.addLabel(l, " ", i, j)
				self.app.setLabelBg(l, "DarkGrey")

				if i > 0 and j > 0:
					lbl.config(borderwidth=2, relief="raised")
					lbl.bind( "<Button-1>", mouse_left_click )
					lbl.bind( "<Button-3>", mouse_right_click )
					lbl.row = i - 1
					lbl.col = j - 1

		for i in range(self.col_count):
			lbl = self.get_cell_name(0, i+1)
			self.app.setLabel(lbl, str(self.cols[i]))
			self.app.setLabelBg(lbl, "LightBlue")
			self.app.getLabelWidget(lbl).config(relief="ridge")

		for i in range(self.row_count):
			lbl = self.get_cell_name(i+1, 0)
			self.app.setLabel(lbl, self.rows[i])
			self.app.setLabelBg(lbl, "LightBlue")
			self.app.getLabelWidget(lbl).config(relief="ridge")

	def draw_board(self, is_real = False):
		l = self.get_cell_name(0, 0)
		lbl = self.app.getLabelWidget(l)
		lbl.config(text=str(self.mine_count - self.found))

		for i in range(self.row_count):
			for j in range(self.col_count):
				cell = self.get_cell(i, j)
				l = self.get_cell_name(i+1, j+1)
				lbl = self.app.getLabelWidget(l)
				if is_real == False:
					if cell == CELL_MINE:
						cell = CELL_CLOSED
					elif cell == CELL_INVALID:
						cell = CELL_MARK

				if cell == CELL_CLOSED:
					lbl.config(relief="raised")
					lbl.config(text = "")
				elif cell == CELL_OPEN:
					self.app.setLabelBg(l, "LightGrey")
					lbl.config(relief="sunken")
					lbl.config(text = "")
				elif cell == CELL_MINE:
					lbl.config(relief="raised")
					lbl.config(text = str(cell))
				elif cell == CELL_INVALID:
					lbl.config(relief="raised")
					lbl.config(text = str(cell))
				elif cell == CELL_MARK:
					lbl.config(relief="raised")
					lbl.config(text = str(cell))
				elif cell == CELL_BOMB:
					lbl.config(relief="raised")
					lbl.config(text = str(cell))
				else:
					self.app.setLabelBg(l, "LightGrey")
					lbl.config(relief="sunken")
					lbl.config(text = str(cell))

	def play(self):
		self.app = gui("Minesweeper by yasam", "1200x600")
		self.app.setSticky("news")
		self.app.setExpand("both")
		self.create_board()
		self.draw_board()
		self.app.go()

def main():
	global game
	game = GameGui(16, 30, 99)
	game.play()

if __name__ == "__main__":
	main()

