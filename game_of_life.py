import pygame

from game_of_life_board import GameOfLifeBoard
import pdb


class GameOfLife(object):
    """
    Represent the Game of Life.
    """
    game_phases = {
        'transition': -1,
        'initialization': 0,
        'menu': 1,
        'board creation': 2,
        'simulation': 3,
        'post-game': 4
    }
    start_game_key_code = 13  # 'enter', '/r'
    end_game_key_code = 113  # 'q'

    def __init__(self):
        """
        Initialize an instance of Game of Life.
        Board defaults to taking up whole window.
        """
        self.surface = pygame.display.set_mode()
        self.screen_info = pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.frames_per_second = 30
        self.deltat = self.clock.tick(self.frames_per_second)
        self.animation_delay = 1000
        self.game_phase = GameOfLife.game_phases['initialization']
        self.menu = ['start simulation', 'create board', 'load board', 'quit']
        rows = 6
        cols = 8
        self.default_board = {
            'rows': rows,
            'cols': cols,
            'live_cell_coords': (
                (1, 1), (2, 2), (3, 3)
            ),
            'GUI_components': {
                'draw_surface': self.surface,
                'cell_width': self.screen_info.current_w / cols,
                'cell_height': self.screen_info.current_h / rows,
                'cell_shape_generator': pygame.Rect,
                'cell_outline_color': pygame.Color('black'),
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
        self.start_board_creation()

    def start_board_creation(self):
        """
        Start the phase of the game where player creates the board.
        """
        self.game_phase = GameOfLife.game_phases['board creation']
        self.game = {
            'board': GameOfLifeBoard(**self.default_board)
        }

        self.game['board'].display_self()
        pygame.display.flip()

        while self.game_phase == GameOfLife.game_phases['board creation']:
            self.clock.tick(self.frames_per_second)
            for event in pygame.event.get():
                if (hasattr(event, 'key') and
                            event.key == GameOfLife.start_game_key_code):
                    self.game_phase = GameOfLife.game_phases['transition']

        self.start_game()

    def start_game(self):
        """
        Start the Game of Life.
        """
        self.game_phase = GameOfLife.game_phases['simulation']

        pygame.time.delay(self.animation_delay)
        while self.game['board'].put_board_in_next_state():
            pygame.display.flip()
            pygame.time.delay(self.animation_delay)

        self.game_phase = GameOfLife.game_phases['post-game']
        pdb.set_trace()
        while self.game_phase == GameOfLife.game_phases['post-game']:
            self.clock.tick(self.frames_per_second)
            for event in pygame.event.get():
                if (hasattr(event, 'key') and
                            event.key == GameOfLife.end_game_key_code):
                    self.game_phase = GameOfLife.game_phases['transition']

    def reset_menu_selections(self):
        self.menu_selections = None

if __name__ == '__main__':
    game = GameOfLife()
    game.start()
