from game_of_life_cell import GameOfLifeCell


class GameOfLifeBoard(object):
    """
    Represent a board in the Game of Life.
    """
    def __init__(self, width, height, live_cell_coords=None):
        # TODO: error handling for illegal sizes, live tiles
        self.width = width
        self.height = height
        self.board = [[GameOfLifeCell(x, y, is_alive=(x,y) in live_cell_coords)
                       for x in range(width)]
                      for y in range(height)]
        self.alive_tiles = set(live_cell_coords)

    def put_board_in_next_state(self):
        """
        Set the board to the next state based on the rule of the Game of Life.

        Rules:
        1. A cell's 'neighbors' includes all cells adjacent in row, col, or
            diagonal.
        2. Any live cell with fewer than two live neighbors dies.
        3. Any live cell with more than three live neighbors dies.
        4. Any live cell with two or three live neighbors lives.
        5. Any dead cell with exactly three live neighbors becomes live.
        """
        # TODO: implement algo
        cells_to_set_alive = set([])

        # calculate next state
        for row in range(self.width):
            for col in range(self.height):
                if self.get_next_cell_state(self.board[row][col]):
                    cells_to_set_alive.add((row, col))

        # set next state
        for row in range(self.width):
            for col in range(self.height):
                if (row, col) in cells_to_set_alive:
                    self.board[row][col].is_alive = True
                else:
                    self.board[row][col].is_alive = False

    def get_next_cell_state(self, cell):
        """
        Returns True if next state for given cell is alive, False otherwise.
        """
        num_live_neighbors = self.get_num_live_neighbors(cell)
        if not cell.is_alive:
            return num_live_neighbors == 3  # could de-hardcode
        if num_live_neighbors < 2 or num_live_neighbors > 3:
            return False
        return True

    def get_num_live_neighbors(self, cell):
        """
        Return the number of live neighbors for a cell.
        """
        num_live_neighbors = 0
        for curr_row in range(cell.row-1, cell.row+2):
            for curr_col in range(cell.col-1, cell.col+2):
                if ((curr_row == cell.col and curr_col == cell.row) or
                        (curr_row < 0 or curr_row >= self.width) or
                        (curr_col < 0 or curr_col >= self.height)):
                    continue
                if self.board[curr_row][curr_col].is_alive:
                    num_live_neighbors += 1
        return num_live_neighbors
