/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package text;
import java.util.Random;

/**
 *
 * @author yasam
 */
public abstract class MineSweeper {
    public int openCount;
    public int foundCount;
    public int rowCount;
    public int colCount;
    public int mineCount;
    public Cell[][] board;
    abstract void updateCell(int row, int col);
    abstract void message(String msg);
    
    
    public MineSweeper(int row, int col, int mine) {
        this.openCount = 0;
        this.foundCount = 0;
        this.mineCount = mine;
        this.rowCount = row;
        this.colCount = col;
        
        //this.board = new Cell()[this.rowCount][this.colCount];
        this.board = new Cell[this.rowCount][this.colCount];
        for(int i =0; i< this.rowCount; i++) {
            for(int j =0; j < this.colCount; j++)
                this.board[i][j] = new Cell();
        }
        
        
        Random rand = new Random();
        
        for(int i = 0; i < this.mineCount;) {
            int r = rand.nextInt(this.rowCount);
            int c = rand.nextInt(this.colCount);

            //this.message("row:"+r);
            //this.message("col:"+c);
            if(this.board[r][c].isMine())
                continue;
            
            this.board[r][c].setMine();
            i++;
        }
    }
    
    private Cell getCell(int row, int col) {
        if ( row < 0 || col < 0)
            return null;
        
        if (row >= this.rowCount)
            return null;
        
        if (col >= this.colCount)
            return null;
        
        return this.board[row][col];
    }
    
    private int getMineCount(int row, int col) {
        int ret = 0;
        
        for(int i=-1; i < 2; i++) {
            for(int j = -1; j < 2; j++) {
                Cell cell = this.getCell(row + i, col + j);
                
                if(cell == null)
                    continue;
                
                if(cell.isMine())
                    ret++;
            }
        }
        
        return ret;
    }
    
    private void exploreCell(int row, int col) {
        int count;
        Cell cell = this.getCell(row, col);
        
        cell.actionOpen();
        this.openCount++;
        count = this.getMineCount(row, col);
        cell.setMineCount(count);
        this.updateCell(row, col);
        
        if ( count != 0)
            return;
        
        for(int i=-1; i < 2; i++) {
            for(int j = -1; j < 2; j++) {
                cell = this.getCell(row + i, col + j);
                
                if(cell == null)
                    continue;
                
                if(cell.isOpen())
                    continue;
                
                if( cell.isMarked())
                    continue;
                
                this.exploreCell(row+i, col+j);
            }
        }
        
        
    }
    
    public boolean checkWin() {
        if(this.foundCount != this.mineCount)
            return false;
        
        return (this.openCount + this.foundCount) == (this.rowCount*this.colCount);
    }
    
    public boolean open(int row, int col) {
        Cell cell = this.getCell(row, col);

        if (cell.isOpen()) {
            this.message("You cannot open this cell!!!");
            return true;
        }
        
        if(cell.isMarked()) {
            this.message("You cannot open this cell!!!");
            return true;
        }
        
        if (cell.isMine()){
            cell.setBomb();
            this.updateCell(row, col);
            return false;
        }
        
        this.exploreCell(row, col);
        return true;
    }
    
    public void mark(int row, int col) {
        Cell cell = this.getCell(row, col);
        if(cell.isOpen()) {
            this.message("You cannot mark this cell!!!");
            return;
        }        

        if(cell.isMarked()) {
            this.message("You cannot mark this cell!!!");
            return;
        }
        
        cell.actionMark();
        this.foundCount++;
        this.updateCell(row, col);
        
    }

    public void unmark(int row, int col) {
        Cell cell = this.getCell(row, col);

        if(cell.isMarked() == false) {
            this.message("You cannot unmark this cell!!!");
            return;
        }
        
        cell.actionUnmark();
        this.foundCount--;
        this.updateCell(row, col);        
    }
}
