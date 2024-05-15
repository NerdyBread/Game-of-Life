from cell import Cell

class GameOfLife:
    def __init__(self, n):
        self.n = n
        self._generate_grid()
        self.neighbor_coords = [(-1, -1), (-1, 0), (-1, 1),
                                (0, -1), (0, 1),
                                (1, -1), (1, 0), (1, 1)]
        
    def get_cell(self, x, y):
        return self.grid[y][x]
    
    def _generate_grid(self):
        self.grid = []
        for i in range(self.n):
            new_row = []
            for j in range(self.n):
                new_row.append(Cell(self))
            self.grid.append(new_row)
    
    def _get_cell_neighbors(self, x, y) -> int:
        living_neighbors = 0
        for pair in self.neighbor_coords:
            if 0 <= (x + pair[0]) < self.n and 0 <= y+pair[1] < self.n:
                neighbor = self.grid[y+pair[1]][x+pair[0]]
                neighbor_current_state = neighbor.is_alive()
                living_neighbors += neighbor_current_state
        return living_neighbors
    
    def set_next_frame_states(self):
        """Updates first bit of each cell according to what state it should be next frame"""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                neighbor_count = self._get_cell_neighbors(x, y)
                if cell.is_dead() and neighbor_count == 3:
                    cell.set_alive()
                if cell.is_alive():
                    if neighbor_count not in (2, 3):
                        cell.set_dead()
                    else:
                        # Keep cells alive next frame if they hit neighbor requirement
                        cell.set_alive()
    
    def update_cells(self):
        """Finish the two-pass cell update cycle"""
        for row in self.grid:
            for cell in row:
                cell.next_frame()
                
    def show_grid(self):
        for row in self.grid:
            row_text = ""
            for cell in row:
                row_text += str(int(cell.is_alive()))
            print(row_text)
        print("--------------")
            
    def switch_cell(self, x, y):
        cell = self.grid[y][x]
        cell.set_alive() # Set cells to live next frame
        cell.next_frame() # Move cells to next frame
            
    def main(self):
        """Main game loop"""
        print("The Game of Life")
        for i in range(1, 10):
            self.set_next_frame_states()
            self.update_cells()
            # Any user cell updates
            if i == 1:
                self.switch_cell(1, 0)
                self.switch_cell(2, 1)
                self.switch_cell(0, 2)
                self.switch_cell(1, 2)
                self.switch_cell(2, 2)
            self.show_grid()
        
if __name__ == "__main__":
    test = GameOfLife(15)
    test.main()