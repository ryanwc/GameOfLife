import pygame

from game_of_life_board import GameOfLifeBoard


class GameOfLife(object):
    """
    Represent the Game of Life.
    """
    game_phases = {
        'initialization': 0,
        'menu': 1,
        'board creation': 2,
        'simulation': 3,
        'post-game': 4
    }

    def __init__(self, rows=8, cols=6, live_cell_coords=None):
        """
        Initialize an instance of Game of Life.
        Board defaults to taking up whole window.
        """
        self.screen = pygame.display.set_mode()
        info = self.screen.Info()
        self.board = GameOfLifeBoard(
            info.current_w, info.current_h, rows, cols, live_cell_coords)
        self.clock = pygame.time.Clock()
        self.frames_per_second = 30
        self.deltat = self.clock.tick(self.frames_per_second)
        self.game_phase = GameOfLife.game_phases['initialization']
        self.menu_selections = None

    def start(self):
        """
        Start the Game of Life.
        """
        self.display_menu()

    def display_menu(self):
        """
        Display the menu for Game of Life and wait for user selections.
        """
        self.game_phase = GameOfLife.game_phases['menu']
        # TODO: wait for and process user menu selections

    def reset_menu_selections(self):
        self.menu_selections = None

    def start_game(self):
        """
        Start the Game of Life.
        """
        if not self.menu_selections:
            return None

        self.game_phase = GameOfLife.game_phases['board creation']
        # TODO: begin an instance of the Game of Life based on user selections

if 'name' == '__main__':
    game = GameOfLife()
    game.start()
