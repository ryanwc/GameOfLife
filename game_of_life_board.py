from game_of_life_tile import GameOfLifeTile


class GameOfLifeBoard(object):
    """
    Represent a board in the Game of Life.
    """
    def __init__(self, width, height):
        self.board = [[GameOfLifeTile(x, y) for x in range(width)]
                      for y in range(height)]
        self.on_tiles = set([])  # set members: coords of 'on' tiles

    def put_board_in_next_state(self):
        """
        Set the board to the next state based on the rule of the Game of Life.
        """
        # TODO: implement algo
