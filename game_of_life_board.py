from functools import partial

from game_of_life_cell import GameOfLifeCell


class GameOfLifeBoard(object):
    """
    Represent a board in the Game of Life.
    """
    def __init__(
            self, rows, cols, live_cell_coords=None, GUI_components=None):
        """
        Use dependency injection pattern to provide GUI components.
        """
        # TODO: error handling for illegal sizes, live tiles
        if GUI_components is None:
            GUI_components = {}
        self.GUI_components = GUI_components
        self.rows = rows
        self.cols = cols
        cell_width = self.GUI_components.get('cell_width')
        cell_height = self.GUI_components.get('cell_height')
        surface = self.GUI_components.get('draw_surface')
        shape_generator = (self.GUI_components.get('cell_shape_generator') or
                           (lambda x,y,width,height: None))
        draw_func = (self.GUI_components.get('cell_draw_func') or
                     (lambda draw_surface,color,rect,w: None))
        self.board = [
            [GameOfLifeCell(
                row, col, is_alive=(row,col) in live_cell_coords,
                GUI_components={
                    'shape': shape_generator(
                        col*cell_width, row*cell_height, cell_width,
                        cell_height),
                    'alive_color': self.GUI_components.get('alive_color'),
                    'dead_color': self.GUI_components.get('dead_color'),
                    'get_fill_param': lambda is_alive: 0 if is_alive else 1,
                    'draw_func': partial(draw_func, surface)
                }
            )
                for row in range(rows)]
            for col in range(cols)
        ]

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

        Return True if made a change, False otherwise
        """
        cells_to_set_alive = set([])
        made_a_change = False

        # calculate next state
        for row in range(self.rows):
            for col in range(self.cols):
                if self.get_next_cell_state(self.board[row][col]):
                    cells_to_set_alive.add((row, col))

        # set next state
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                old_status = cell.is_alive
                cell.is_alive = (row, col) in cells_to_set_alive
                made_a_change = old_status == cell.is_alive
                if made_a_change and cell.draw_func:
                    cell.draw_self()

        return made_a_change

    def get_next_cell_state(self, cell):
        """
        Returns True if next state for given cell is alive, False otherwise.

        Currently, game rules are hardcoded into this method.
        """
        num_live_neighbors = self.get_num_live_neighbors(cell)
        if not cell.is_alive:
            return num_live_neighbors == 3
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
                        (curr_row < 0 or curr_row >= self.rows) or
                        (curr_col < 0 or curr_col >= self.cols)):
                    continue
                if self.board[curr_row][curr_col].is_alive:
                    num_live_neighbors += 1
        return num_live_neighbors
