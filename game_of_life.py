import pygame

from game_of_life_board import GameOfLifeBoard
import pdb


class GameOfLife(object):
    """
    Represent the Game of Life.
    """
    GAME_PHASES = {
        'transition': -1,
        'initialization': 0,
        'menu': 1,
        'board creation': 2,
        'simulation': 3,
        'post-game': 4
    }
    LEFT_MOUSE_BUTTON_CODE = 1
    QUIT_KEY_CODES = [113]  # 'q'

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
        self.animation_delay_length = 1000
        self.game_phase = GameOfLife.GAME_PHASES['initialization']
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
        self.game_phase = GameOfLife.GAME_PHASES['menu']
        # TODO: wait for and process user menu selections
        self.start_board_creation()

    def start_board_creation(self):
        """
        Start the phase of the game where player creates the board.
        """
        self.game_phase = GameOfLife.GAME_PHASES['board creation']
        self.game = {
            'board': GameOfLifeBoard(**self.default_board)
        }

        self.game['board'].display_self()
        pygame.display.flip()

        while self.game_phase == GameOfLife.GAME_PHASES['board creation']:
            self.clock.tick(self.frames_per_second)
            for event in pygame.event.get():
                if hasattr(event, 'key') and event.key == pygame.K_RETURN:
                    self.game_phase = GameOfLife.GAME_PHASES['transition']
                    break
                elif (event.type == pygame.MOUSEBUTTONDOWN and
                        event.button == GameOfLife.LEFT_MOUSE_BUTTON_CODE):
                    clicked_cell = self.get_cell_from_screen_coords(event.pos)
                    if not clicked_cell:
                        continue
                    clicked_cell.is_alive = not clicked_cell.is_alive
                    clicked_cell.draw_self()
                    pygame.display.flip()
                    break

        self.start_game()

    def start_game(self):
        """
        Start the Game of Life.
        """
        self.game_phase = GameOfLife.GAME_PHASES['simulation']

        pygame.time.delay(self.animation_delay_length)
        while self.game['board'].put_board_in_next_state():
            pygame.display.flip()
            pygame.time.delay(self.animation_delay_length)

        self.game_phase = GameOfLife.GAME_PHASES['post-game']
        while self.game_phase == GameOfLife.GAME_PHASES['post-game']:
            self.clock.tick(self.frames_per_second)
            for event in pygame.event.get():
                if (hasattr(event, 'key') and
                        event.key in GameOfLife.QUIT_KEY_CODES):
                    self.game_phase = GameOfLife.GAME_PHASES['transition']

    def reset_menu_selections(self):
        self.menu_selections = None

    def get_cell_from_screen_coords(self, screen_coords):
        """
        Return the GameOfLifeCell at the given (x, y) screen coords.
        Return None if coords are out of board bounds.
        """
        row = int(
            screen_coords[1]/self.game['board'].GUI_components['cell_height'])
        col = int(
            screen_coords[0]/self.game['board'].GUI_components['cell_width'])
        if (row < 0 or row >= self.game['board'].rows or
                col < 0 or col >= self.game['board'].cols):
            return None
        return self.game['board'].board[row][col]

if __name__ == '__main__':
    game = GameOfLife()
    game.start()
