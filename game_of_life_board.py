from game_of_life_tile import GameOfLifeTile


class GameOfLifeBoard(object):
    """
    Represent a board in the Game of Life.
    """
    def __init__(self, width, height, live_cell_coords=None):
        # TODO: error handling for illegal sizes, live tiles
        self.board = [[GameOfLifeTile(x, y, alive=(x,y) in live_cell_coords)
                       for x in range(width)]
                      for y in range(height)]
        self.alive_tiles = set(live_cell_coords)

    def put_board_in_next_state(self):
        """
        Set the board to the next state based on the rule of the Game of Life.
        """
        # TODO: implement algo
        # any live cell with fewer than two live neighbors dies
        # any live cell with more than three live neighbors dies
        # any live cell with two or three live neighbors lives on to next gen
        # anydead cell with exactly three live neighbors becomes live
