#!/usr/bin/python3

import argparse
from appJar import gui
from tkinter import messagebox

from minesweeper import *

def mouse_left_click( event ):
	game.mouse_left_click(event)

def mouse_right_click( event ):
	game.mouse_right_click(event)

def verbose_left_click( event ):
	game.verbose(True)

def verbose_right_click( event ):
	game.verbose(False)

class GameGui(MineSweeper):
	def __init__(self, row, col, mine):
		return MineSweeper.__init__(self, row, col, mine)

	def get_cell_name(self, row, col):
		return str(row).zfill(2) + "-" + str(col).zfill(2)

	def message(self, msg):
		messagebox.showinfo("MineSweeper", msg)

	def update_cell(self, row, col, is_real=False):
		fgcolors = ["","green", "yellow", "blue", "purple", "navy", "orange", "maroon", "red"]
		cell = self.get_cell(row, col)

		# default state is closed
		bgcolor = "DarkGrey"
		relief = "raised"
		val = cell.get_str_val()

		if cell.is_open() :
			bgcolor = "LightGrey"
			relief = "sunken"

		if is_real:
			val = cell.get_str_real_val()



		l = self.get_cell_name(row+1, col+1)
		lbl = self.app.getLabelWidget(l)

		fgcolor = fgcolors[cell.get_mine_count()]
		if fgcolor != "":
			self.app.setLabelFg(l, fgcolor)

		self.app.setLabelBg(l, bgcolor)
		lbl.config(relief=relief)
		lbl.config(text = val)

	def verbose(self, enable):
		self.draw_board(enable)

	def mouse_left_click(self, event):
		result = self.open(event.widget.row, event.widget.col)
		self.update_count()

		if  result == False :
			self.draw_board(True)
			self.message("You Lost!!!")
			self.app.stop()

		if self.check_win() == True:
			self.message("You won!!!")
			self.app.stop()

	def mouse_right_click(self, event):
		cell = self.get_cell(event.widget.row, event.widget.col)
		if cell.is_marked() :
			self.unmark(event.widget.row, event.widget.col)
		else:
			self.mark(event.widget.row, event.widget.col)

		self.update_count()

		if self.check_win() == True:
			self.message("You won!!!")
			self.app.stop()

	def create_board(self):
		#create the cells
		for i in range(self.row_count + 1):
			for j in range(self.col_count + 1):
				l = self.get_cell_name(i, j)
				lbl = self.app.addLabel(l, " ", i, j)
				self.app.setLabelBg(l, "DarkGrey")
				self.app.setLabelWidth(l, 40)
				self.app.setLabelHeight(l, 40)

				if i > 0 and j > 0:
					lbl.config(borderwidth=2, relief="raised")
					lbl.bind( "<Button-1>", mouse_left_click )
					lbl.bind( "<Button-3>", mouse_right_click )
					lbl.row = i - 1
					lbl.col = j - 1

		#draw cols
		for i in range(self.col_count):
			lbl = self.get_cell_name(0, i+1)
			self.app.setLabel(lbl, str(self.cols[i]))
			self.app.setLabelBg(lbl, "LightBlue")
			self.app.getLabelWidget(lbl).config(relief="ridge")

		#draw rows
		for i in range(self.row_count):
			lbl = self.get_cell_name(i+1, 0)
			self.app.setLabel(lbl, self.rows[i])
			self.app.setLabelBg(lbl, "LightBlue")
			self.app.getLabelWidget(lbl).config(relief="ridge")

		# set verbose events
		l = self.get_cell_name(0, 0)
		lbl = self.app.getLabelWidget(l)
		lbl.bind( "<Button-1>", verbose_left_click )
		lbl.bind( "<Button-3>", verbose_right_click )


	def draw_board(self, is_real = False):
		self.update_count()
		for i in range(self.row_count):
			for j in range(self.col_count):
				self.update_cell(i, j, is_real)

	def update_count(self):
		l = self.get_cell_name(0, 0)
		lbl = self.app.getLabelWidget(l)
		lbl.config(text=str(self.mine_count - self.found))

	def play(self):
		width = (self.col_count + 1) * 40
		height = (self.row_count + 1) * 40
		self.app = gui("Minesweeper by yasam", str(width)+"x"+str(height), handleArgs=False)
		self.app.setSticky("news")
		self.app.setExpand("both")
		self.create_board()
		self.draw_board()
		self.app.go()

def main():
	global game
	argparser = argparse.ArgumentParser()
	argparser.add_argument("-r", "--row", help="rows count", type=int, default=16)
	argparser.add_argument("-c", "--col", help="cols count", type=int, default=30)
	argparser.add_argument("-m", "--mine", help="mines count", type=int, default=99)

	args = argparser.parse_args()

	game = GameGui(args.row, args.col, args.mine)
	game.play()

if __name__ == "__main__":
	main()

