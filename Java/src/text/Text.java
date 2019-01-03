/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package text;

import java.util.Arrays;

/**
 *
 * @author yasam
 */
public class Text extends MineSweeper {

    public Text(int row, int col, int mine) {
        super(row, col, mine);
    }

    @Override
    void updateCell(int row, int col) {
        
    }

    @Override
    void message(String msg) {
        System.out.println(msg);
    }
    
    private void printBoard(boolean isReal) {
        Cell cell;
         //default, "green", "yellow", "blue", "magenta", "cyan", "light red", "light magenta", "red", "dark gray"
        String colors[] = {"\033[39m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\33[36m", "\033[91m", "\033[95m" , "\033[31m"};
        String bgnormal = "\033[49m";
        String bgclosed = "\033[100m";
        String bgopen = "\033[47m";
       
        String cols = "  ";
        
        for(int i = 1; i<= this.colCount; i++) {
            cols += i + " ";
            if(i < 9 )
                cols += " ";
        }
        
        this.message(cols);
        
        for(int i = 0; i< this.rowCount; i++) {
            String row;
            row = "";
            
            row += Character.toString((char)('A' + i));
                    
            for(int j=0; j< this.colCount; j++) {
                String bgcolor;
                String color;
                String val;

                cell = this.board[i][j];
                bgcolor = bgclosed;
                color = colors[0];

                val = cell.getValueAsString();

                if (cell.isMarked() == false && cell.isOpen() == false)
                    val = ".";

                if(isReal)
                    val = cell.getRealValueAsString();

                if(cell.isOpen()) {
                    bgcolor = bgopen;
                    color = colors[cell.getMineCount()];
                }

                row += bgcolor + color + " " + val + " " + colors[0] + bgnormal;
            }
            this.message(row);
        }
    }
    
    private int readCol() {
        int col;
       
        while(true) {
            System.out.print("Enter col:");
            try {
                col = Integer.parseInt(System.console().readLine());
            } catch(NumberFormatException ex) 
            {
                this.message("Exception:"+ex);
                continue;
            }
            if (col <=0 ) {
                this.message("Invalid col:" + col);
                continue;
            }
            if (col > this.colCount) {
                this.message("Invalid col:"+col);
                continue;
            }

            return col - 1;
        }
    }
    
    private int readRow() {
        int row;
        String r;
        char[] c;
       
        while(true) {
            System.out.print("Enter row:");
            r = System.console().readLine();
            c = r.toCharArray();
            row = c[0] - 'A';
            
            if(row < 0) {
                this.message("Invalid row:"+row);
                continue;
            }
            if(row >= this.rowCount) {
                this.message("Invalid row:"+row);
                continue;
            }
            return row;
        }
    }
    private String readAction() {
        String action;
        String[] values = {"O","M","U","C", "D", "E"};
       
        while(true) {
            System.out.print("Enter command(O:Open, M:Mark, U:Unmark, C:Cancel, D:Dummp, E:Exit):");
            action = System.console().readLine();
            boolean contains = Arrays.stream(values).anyMatch(action::equals);
            if(contains)
                return action;
            this.message("Invalid command:"+action);
        }
    }
    
    public void play() {
        int row;
        int col;
        String action;
        
        this.printBoard(true);
        while(true) {
            try {
                this.printBoard(false);
                row = this.readRow();
                col = this.readCol();
                action = this.readAction();
                //System.out.println("col:"+col+", row:"+row+", action:"+action);

                if(action.equals("O")) {
                    if (this.open(row, col) == false) {
                        this.printBoard(true);
                        this.message("You lost!!!");
                        break;
                    }
                }

                if(action.equals("M"))
                    this.mark(row, col);

                if(action.equals("U"))
                    this.unmark(row, col);

                if(action.equals("D"))
                    this.printBoard(true);

                if(action.equals("C"))
                    continue;

                if(action.equals("E"))
                    break;

                if(this.checkWin()) {
                    this.message("You won!!!");
                    break;
                }
                this.message("Found:"+this.foundCount+", Open:"+this.openCount);
            }
            catch(Exception e)
            {
                this.message("Exception:"+ e);
                e.printStackTrace();
            }
        }
    }
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Text text = new Text(16, 30, 99);
        text.play();
    }
    
}
