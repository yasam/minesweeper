#include <stdio.h>
#include <stdio_ext.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define fpurge __fpurge

#define ROW_COUNT 16
#define COL_COUNT 30
#define MINE_COUNT 99


#define CELL_CLOSED	'-'
#define CELL_OPEN	' '
#define CELL_MINE	'M'
#define CELL_INVALID	'I'
#define CELL_MARK	'X'
#define CELL_BOMB	'O'

#define ACTION_OPEN	'O'
#define ACTION_MARK	'M'
#define ACTION_UNMARK	'U'
#define ACTION_CANCEL	'C'

#define	GET(row, col) (board[row][col])
#define	SET(row, col, val) board[row][col] = val

char board[ROW_COUNT][COL_COUNT];


void init_board()
{
	int row;
	int col;

	//       srand(time(NULL));
	for (int i = 0; i < ROW_COUNT; i++)
		for (int j = 0; j < COL_COUNT; j++)
			SET(i, j, CELL_CLOSED);

	for (int i = 0; i < MINE_COUNT;) {
		row = rand() % ROW_COUNT;
		col = rand() % COL_COUNT;

		if (GET(row, col) == CELL_MINE)
			continue;

		SET(row, col, CELL_MINE);
		i++;
	}
}

void print_board(int real)
{
	char p;
	char tmp[8];

	printf(" "); // space for col name
	for (int i = 0; i < COL_COUNT; i++) {
		sprintf(tmp, "%d", i + 1);
		printf("%3s", tmp);
	}
	printf("\n");

	for (int i = 0; i < ROW_COUNT; i++) {
		printf("%c", 'A' + i);

		for (int j = 0; j < COL_COUNT; j++) {
			if (real)
				p = board[i][j];
			else {
				switch (GET(i, j)) {
				case CELL_MINE:
					p = CELL_CLOSED;
					break;
				case CELL_INVALID:
					p = CELL_MARK;
					break;
				default:
					p = GET(i, j);
					break;
				}
			}
			printf("  %c", p);
		}
		printf("\n");
	}
}

int get_row()
{
	char c;
	while (1) {
		fpurge(stdin);
		printf("Enter row(A-P):");
		scanf("%c", &c);
		if (c < 'A' && c > ('A' + ROW_COUNT)) {
			printf("Invalid row:%c\n", c);
			continue;
		}
		return c - 'A';
	}
}

int get_col()
{
	int c;
	while (1) {
		fpurge(stdin);
		printf("Enter col(1-30):");
		scanf("%d", &c);
		if (c < 1 && c > COL_COUNT) {
			printf("Invalid col:%d\n", c);
			continue;
		}
		return c - 1;
	}
}

char get_action()
{
	char c;
	while (1) {
		fpurge(stdin);
		printf("Enter action(O: Open, M: Mark, U: Unmark, C: Cancel):");
		scanf("%c", &c);

		switch (c) {
		case ACTION_MARK:
			break;
		case ACTION_OPEN:
			break;
		case ACTION_UNMARK:
			break;
		case ACTION_CANCEL:
			break;
		default:
			printf("Invalid action:%c\n", c);
			continue;
		}

		return c;
	}
}

int get_mine_count(int row, int col)
{
	int cnt = 0;
	int r;
	int c;

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			if (i == 1 && j == 1)
				continue;
			r = row - 1 + i;
			c = col - 1 + j;
			if (r < 0 || r >= ROW_COUNT)
				continue;

			if (c < 0 || c >= COL_COUNT)
				continue;

			if (GET(r, c) == CELL_MINE || GET(r, c) == CELL_MARK)
				cnt++;
		}
	}

	return cnt;
}

int open_cell(int row, int col)
{
	int cnt;
	int r;
	int c;

	if (row < 0 || row >= ROW_COUNT)
		return 0;

	if (col < 0 || col >= COL_COUNT)
		return 0;

	cnt = get_mine_count(row, col);

	if (cnt != 0) {
		SET(row, col, ('0' + cnt));
		return 1;
	}

	// cnt is 0, explore around
	SET(row, col, CELL_OPEN);
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			r = row - 1 + i;
			c = col - 1 + j;
			if (GET(r, c) == CELL_CLOSED)
				cnt += open_cell(r, c);
		}
	}
	
	return cnt + 1;
}

int main()
{
	int row;
	int col;
	char action;
	int ret;
	int found = 0;
	int open = 0;

	init_board();
	//print_board(1);

	while (1) {
		print_board(0);
		row = get_row();
		col = get_col();
		action = get_action();

		switch (action) {
		case ACTION_OPEN:
			if (GET(row, col) == CELL_CLOSED || GET(row, col) == CELL_MINE) {
				if (GET(row, col) == CELL_MINE) {
					SET(row, col, CELL_BOMB);
					printf("You lost!!!\n");
					goto end;
				}

				ret = open_cell(row, col);
				open += ret;
			} else {
				printf("Invalid action(%c) for this cell\n", action);
				continue;
			}
			break;
		case ACTION_MARK:
			if (GET(row, col) == CELL_CLOSED || GET(row, col) == CELL_MINE) {
				found++;
				if (GET(row, col) == CELL_MINE)
					SET(row, col, CELL_MARK);
				else
					SET(row, col, CELL_INVALID);
			} else {
				printf("Invalid action(%c) for this cell\n", action);
				continue;
			}
			break;
		case ACTION_UNMARK:
			if (GET(row, col) == CELL_INVALID || GET(row, col) == CELL_MARK) {
				found--;
				SET(row, col, CELL_CLOSED);
			} else {
				printf("Invalid action(%c) for this cell\n", action);
				continue;
			}
			break;
		case ACTION_CANCEL:
			break;
		}

		if ((open + found) >= (ROW_COUNT * COL_COUNT)) {
			printf("You won!!!\n");
			break;
		} else {
			printf("Marked:%d, Open:%d\n", found, open);
		}
	}
end:
	print_board(1);
	return 0;
}
