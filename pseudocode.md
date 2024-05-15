
# Game of Life

Python Implementation

## Backend

NxN grid of cells
Cells can be dead or alive (0 or 1)

**Dead Cells**
- Three neighbors will bring the cell to life
- Anything else will keep it unchanged

**Living Cells**
- Zero or one neighbors -> it will die
- Four or more neighbors -> it will die
- Two or three neighbors -> it will survive

***Main Game Loop Steps***
1. Compute next frame state of each cell
    - If cell is dead and has three live neighbors -> set state to alive
    - If cell is alive
        - If not two or three neighbors -> set state to dead
2. Once they are all computed, update the cells accordingly

































**Bitwise operations**

How to represent the cells
0b00 -> dead to dead
0b01 -> alive to dead
0b10 -> dead to alive
0b11 -> alive to alive

Step 1
Kill mask = 0b01
& the mask and the cell
Ex with two possible living cell states 
    0b11 & 0b01 = 0b01
    0b01 & 0b01 = 0b01

Live mask = 0b11


Step 2
Bitwise >> -> sets current state bit to value of future bit
