/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package text;

/**
 *
 * @author yasam
 */
public class Cell {
    private boolean open;
    private boolean mine;
    private boolean mark;
    private boolean bomb;
    private int mineCount;
    private String val;
    private String realVal;
    
            
    public Cell() {
        this.open = false;
        this.mark = false;
        this.bomb = false;
        this.mine = false;
        this.mineCount = 0;
        this.val = " ";
        this.realVal = " ";
    }

    public Cell(Cell cell) {
        this.open = cell.open;
        this.mark = cell.mark;
        this.bomb = cell.bomb;
        this.mine = cell.mine;
        this.mineCount = cell.mineCount;
        this.val = cell.val;
        this.realVal = cell.realVal;
    }
    
    public void actionOpen() {
        this.open = true;
    }
    
    public void actionMark() {
        this.mark = true;
        this.val = "X";
        this.realVal = "X";
        if(this.isMine() == false)
            this.realVal = "I";
    }

    public void actionUnmark() {
        this.mark = false;
        this.val = " ";
        this.realVal = " ";
        if(this.isMine())
            this.realVal = "M";
    }

    public void setMine() {
        this.mine = true;
        this.realVal = "M";
    }

    public void setMineCount(int count) {
        this.mineCount = count;
        if (this.mineCount != 0) {
            this.val = Integer.toString(mineCount);
            this.realVal = Integer.toString(mineCount);
        }
    }

    public int getMineCount() {
        return this.mineCount;
    }

    public void setBomb() {
        this.bomb = true;
        this.val = "O";
        this.realVal = "O";
    }

    public boolean isOpen() {
        return this.open;
    }
    
    public boolean isMarked() {
        return this.mark;
    }

    public boolean isMine() {
        return this.mine;
    }
    public boolean isBomb() {
        return this.bomb;
    }
    
    public String getValueAsString() {
        return this.val;
    }

    public String getRealValueAsString() {
        return this.realVal;
    }
}
