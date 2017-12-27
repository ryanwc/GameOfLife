
class GameOfLifeTile(object):
    """
    Represent a tile in the Game of Life.
    """
    def __init__(self, row, col, alive=False):
        self.row = row
        self.col = col
        self.alive = alive

    def bring_to_life(self):
        self.alive = True

    def kill(self):
        self.alive = False
        