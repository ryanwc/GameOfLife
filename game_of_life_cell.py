

class GameOfLifeCell(object):
    """
    Represent a cell in the Game of Life.
    """
    def __init__(self, rect, row, col, is_alive=False):
        self.rect = rect
        self.row = row
        self.col = col
        self.is_alive = is_alive

    def bring_to_life(self):
        self.is_alive = True

    def kill(self):
        self.is_alive = False
