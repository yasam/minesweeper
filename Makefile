TARGET=minesweeper

CFLAGS=-O0 -ggdb

all:$(TARGET)


.PHONY: $(TARGET)

$(TARGET):$(TARGET).o
	$(CC) -o $@ $^

clean:
	-rm $(TARGET) $(TARGET).o

