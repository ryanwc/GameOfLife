import statistics
from functools import partial

from game_of_life_cell import GameOfLifeCell
import pdb


class GameOfLifeBoard(object):
    """
    Represent a board in the Game of Life.
    Holds GameOfLifeCells in a 2D list.
    Can hold GUI components or not, depending on client game engine.
    """
    stat_categories = ['longest_living_streak', 'longest_death_streak',
                       'births', 'deaths', 'gens_alive', 'gens_dead']

    def __init__(
            self, rows, cols, live_cell_coords=None, GUI_components=None):
        """
        Use dependency injection pattern to provide GUI components.
        Leaves room between cell shapes for outlines.
        """
        # TODO: error handling for illegal sizes, live tiles
        if GUI_components is None:
            GUI_components = {}
        self.stats = None
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

    def advance_board_one_generation(self):
        """
        Set the board to the next state based on the rules of the Game of Life.

        Rules:
        1. A cell's 'neighbors' includes all cells adjacent in row, col, or
            diagonal.
        2. Any live cell with fewer than two live neighbors dies.
        3. Any live cell with more than three live neighbors dies.
        4. Any live cell with two or three live neighbors lives.
        5. Any dead cell with exactly three live neighbors becomes live.

        Return True if made a change to the board, False otherwise.
        """
        cells_to_flip = set([])

        # calculate next gen and increment counters for current gen
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell.is_alive:
                    cell.stats['gens_alive'] += 1
                    cell.stats['current_living_streak'] += 1
                    if (cell.stats['current_living_streak'] >
                            cell.stats['longest_living_streak']):
                        cell.stats['longest_living_streak'] = \
                            cell.stats['current_living_streak']
                else:
                    cell.stats['gens_dead'] += 1
                    cell.stats['current_dead_streak'] += 1
                    if (cell.stats['current_dead_streak'] >
                            cell.stats['longest_dead_streak']):
                        cell.stats['longest_dead_streak'] = \
                            cell.stats['current_dead_streak']
                will_be_alive = self.get_next_cell_state(cell)
                if ((will_be_alive and not cell.is_alive) or
                        (not will_be_alive and cell.is_alive)):
                    cell.stats['current_living_streak'] = 0
                    cell.stats['current_dead_streak'] = 0
                    cells_to_flip.add(cell)

        # set next gen
        for cell in cells_to_flip:
            cell.is_alive = not cell.is_alive
            if cell.is_alive:
                cell.births += 1
            else:
                cell.deaths += 1
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
                if ((curr_row == cell.row and curr_col == cell.col) or
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

    def calculate_game_stats(self):
        """
        Calculate the stats for the game, such as cell with longest living
        streak, cell with most deaths, percentiles for each cell, etc.
        Stores results in the board's 'stats' variable.
        """
        self.stats = {
            self.GameOfLifeStat(self, category)
            for category in GameOfLifeBoard.stat_categories
        }

        for row in range(self.rows):
            for col in range(self.cols):
                cell_stats = self.board[row][col].stats
                for stat in self.stats:
                    stat.stats['list'].append(cell_stats[stat.category])

        for stat in self.stats:
            stat.calculate_stats()

    class GameOfLifeStat(object):
        """
        Hold a GameOfLife stats for a particular board and stat category.
        A category is a name like 'births' or 'longest_living_streak',
        and the actual stats would be, for example, 'max' or 'median'.

        Category must be numerical (not, e.g., 'color' where 'color' can be
        'red', 'yellow', etc.).
        """

        def __init__(self, board, category, stats=None):

            if dict is None:
                stats = {
                    'list': [],
                    'max': None,
                    'min': None,
                    'median': None,
                    'mean': None,
                    'stdev': None
                }

            self.board = board
            self.category = category
            self.stats = stats

        def __str__(self):
            """
            Only prints stats whose vals can be converted to an int (but
            does not necessarily print this conversion).
            """
            self_str = '**********\nStat category: {}'.format(self.category)
            for stat, val in self.stats.items():
                try:
                    int(val)
                except:
                    continue
                self_str += '\n<{}>: {}'.format(stat, val)

            self_str += '\n**********'
            return self_str

        def calculate_stats(self):
            """
            Calculate and set the stats from the stats list.
            """
            self.stats['list'].sort(reverse=True)
            self.stats['max'] = self.stats['list'][0]
            self.stats['min'] = self.stats['list'][-1]
            self.stats['median'] = statistics.median(self.stats['list'])
            self.stats['mean'] = sum(self.stats['list'])/len(self.stats['list'])
            self.stats['stdev'] = statistics.pstdev(
                self.stats['list'], mu=self.stats['mean'])
