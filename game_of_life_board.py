from functools import partial

from game_of_life_cell import GameOfLifeCell
import pdb


class GameOfLifeBoard(object):
    """
    Represent a board in the Game of Life.
    Holds GameOfLifeCells in a 2D list.
    Can hold GUI components or not, depending on client game engine.
    """
    def __init__(
            self, rows, cols, live_cell_coords=None, GUI_components=None):
        """
        Use dependency injection pattern to provide GUI components.
        Leaves room between cell shapes for outlines.
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

        # shape generator should be a function that takes four args:
        # top left x, top left y, width, and height, all in screen coords,
        # and returns some obj
        self.shape_generator = (self.GUI_components.get('cell_shape_generator')
                                or (lambda x,y,width,height: None))

        # cell draw function should be a function that takes at least one
        # positional arg: the surface to draw on
        draw_func = (self.GUI_components.get('cell_draw_func') or
                     (lambda draw_surface: None))

        # 2D list comprehension with a GameOfLifeCell in each slot
        self.board = [
            [GameOfLifeCell(
                row, col, is_alive=(row,col) in live_cell_coords,
                GUI_components={
                    'shape': self.shape_generator(
                        (col*cell_width)+1, (row*cell_height)+1,
                        cell_width-2, cell_height-2),
                    'outline_color': self.GUI_components.get(
                        'cell_outline_color'),
                    'alive_color': self.GUI_components.get('alive_color'),
                    'dead_color': self.GUI_components.get('dead_color'),
                    'get_fill_param': lambda is_alive: 0 if is_alive else 0,
                    'draw_func': partial(draw_func, surface)
                }
            )
                for col in range(cols)]
            for row in range(rows)
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
        cells_to_flip = set([])

        # calculate next state
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                will_be_alive = self.get_next_cell_state(cell)
                if ((will_be_alive and not cell.is_alive) or
                        (not will_be_alive and cell.is_alive)):
                    cells_to_flip.add(cell)

        # set next state
        for cell in cells_to_flip:
            cell.is_alive = not cell.is_alive
            cell.draw_self()

        return len(cells_to_flip) > 0

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
            if curr_row < 0 or curr_row >= self.rows:
                continue
            for curr_col in range(cell.col-1, cell.col+2):
                if ((curr_row == cell.col and curr_col == cell.row) or
                        (curr_col < 0 or curr_col >= self.cols)):
                    continue
                if self.board[curr_row][curr_col].is_alive:
                    num_live_neighbors += 1
        return num_live_neighbors

    def display_self(self):
        """
        Displays the board in the GUI by drawing each cell and cell outline
        with the provided draw functions.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col].draw_outline()
                self.board[row][col].draw_self()