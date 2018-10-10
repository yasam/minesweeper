#!/usr/bin/python3

import sys
import random
import json
from appJar import gui

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
ACTION_DUMP 	= 'D'
ACTION_EXIT 	= 'E'


def debug(msg):
	print(msg)

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

	def execute(self, row, col, action):
		cell = self.get_cell(row, col)
		if action == ACTION_OPEN:
			if cell == CELL_MINE :
				self.set_cell(row, col, CELL_BOMB)
				# You lost !!!
				return False
			elif cell == CELL_CLOSED :
				self.open_cell(row, col)
			else:
				self.message("You cannot open this cell!")

		elif action == ACTION_MARK:
			if cell == CELL_MINE:
				self.set_cell(row, col, CELL_MARK)
				self.found += 1
			elif cell == CELL_CLOSED:
				self.set_cell(row, col, CELL_INVALID)
				self.found += 1
			else:
				self.message("You cannot mark this cell!")

		elif action == ACTION_UNMARK:
			if cell == CELL_INVALID :
				self.set_cell(row, col, CELL_CLOSED)
				self.found -= 1
			elif cell == CELL_MARK :
				self.set_cell(row, col, CELL_MINE)
				self.found -= 1
			else:
				self.message("You cannot unmark this cell")
		return True

	def message(self, msg):
		raise NotImplementedError("Subclass must implement abstract method")


class GameText(MineSweeper):
	def __init__(self, row, col, mine):
		return MineSweeper.__init__(self, row, col, mine)

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

	def message(self, msg):
		print(msg)

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
		self.print_board(True)
		while True:
			self.print_board(False)
			row = self.read_row();
			col = self.read_col();
			action = self.read_action();

			if action == ACTION_CANCEL:
				debug("action is cancel, do nothing")
			elif action == ACTION_DUMP:
				self.print_board(True)
			elif action == ACTION_EXIT:
				break
			else:
				if self.execute(row, col, action) == False :
					self.message("You Lost!!!")
					break

			if self.check_win() == True:
				self.message("You won!!!")
				break
			else:
				print("Found:"+ str(self.found) + " , Open:"+ str(self.open_count))

		self.print_board(True)

def mouseLeftClick( event ):
	game.mouseLeftClick(event)

def mouseRightClick( event ):
	game.mouseRightClick(event)

class GameGui(MineSweeper):
	def __init__(self, row, col, mine):
		return MineSweeper.__init__(self, row, col, mine)

	def get_cell_name(self, row, col):
		return str(row).zfill(2) + "-" + str(col).zfill(2)

	def message(self, msg):
		print(msg)

	def mouseLeftClick(self, event):
		#print(json.dumps(event.__dict__))
		#print( "mouse clicked at x=" + str(event.x) + " y=" + str(event.y) + "button=" + str(event.button))
		print( "mouse left clicked at x=" + str(event.x) + " y=" + str(event.y))
		print( "row=" + str(event.widget.row) + " col=" + str(event.widget.col))
		result = self.execute(event.widget.row, event.widget.col, ACTION_OPEN)
		self.draw_board()
		if  result == False :
			self.message("You Lost!!!")
			self.app.stop()

		if self.check_win() == True:
			self.message("You won!!!")
			self.app.stop()

	def mouseRightClick(self, event):
		#print(json.dumps(event.__dict__))
		#print( "mouse clicked at x=" + str(event.x) + " y=" + str(event.y) + "button=" + str(event.button))
		print( "mouse right clicked at x=" + str(event.x) + " y=" + str(event.y))
		print( "row=" + str(event.widget.row) + " col=" + str(event.widget.col))
		cell = self.get_cell(event.widget.row, event.widget.col)
		if cell == CELL_INVALID or cell == CELL_MARK :
			self.execute(event.widget.row, event.widget.col, ACTION_UNMARK)
		else:
			self.execute(event.widget.row, event.widget.col, ACTION_MARK)

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
					#"sunken"
					lbl.config(borderwidth=2, relief="raised")
					lbl.bind( "<Button-1>", mouseLeftClick )
					lbl.bind( "<Button-3>", mouseRightClick )
					lbl.row = i-1
					lbl.col = j-1

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
					lbl.config(relief="sunken")
					lbl.config(text = str(cell))

	def play(self):
		self.app = gui("Minesweeper by yasam", "1200x600")
		self.app.setSticky("news")
		self.app.setExpand("both")
		self.create_board()
		#self.draw_board()
		self.app.go()

def main():
	#GameText(16, 30, 99).play()
	global game
	game = GameGui(16, 30, 99)
	game.play()

if __name__ == "__main__":
	main()
