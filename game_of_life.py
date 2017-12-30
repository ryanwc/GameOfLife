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

    def __init__(self):
        """
        Initialize an instance of Game of Life.
        Board defaults to taking up whole window.
        """
        self.screen = pygame.display.set_mode()
        self.screen_info = self.screen.Info()
        self.clock = pygame.time.Clock()
        self.frames_per_second = 30
        self.deltat = self.clock.tick(self.frames_per_second)
        self.game_phase = GameOfLife.game_phases['initialization']
        self.menu = ['start simulation', 'create board', 'load board', 'quit']
        self.default_board = {
            'rows': 8,
            'cols': 6,
            'live_cell_coords': None,
            'GUI_components': {
                'draw_surface': pygame.display.get_surface(),
                'cell_width': self.screen_info.current_w,
                'cell_height': self.screen_info.current_h,
                'cell_shape_generator': pygame.Rect,
                'alive_color': pygame.Color('blue'),
                'dead_color': pygame.Color('white'),
                'cell_draw_func': pygame.draw.rect
            }
        }
        self.menu_selections = {
            'board': self.default_board
        }
        self.game = None

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
        self.start_game()

    def start_board_creation(self):
        """
        Start the phase of the game where player creates the board.
        """
        self.game_phase = GameOfLife.game_phases['board creation']

    def reset_menu_selections(self):
        self.menu_selections = None

    def start_game(self):
        """
        Start the Game of Life.
        """
        if not self.menu_selections:
            return None

        self.game_phase = GameOfLife.game_phases['simulation']
        # TODO: begin an instance of the Game of Life based on user selections
        self.game = {
            'board': GameOfLifeBoard(**self.default_board)
        }

        while self.game['board'].put_board_in_next_state:
            continue

if 'name' == '__main__':
    game = GameOfLife()
    game.start()
