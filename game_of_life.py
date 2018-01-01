#!/usr/bin/env python
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
    CANVAS_COLOR = pygame.Color('white')
    COLORS = {'red', 'blue', 'green', 'brown', 'purple', 'orange', 'violet',
              'black', 'yellow', 'grey', 'white'}
    LEFT_MOUSE_BUTTON_CODE = 1
    QUIT_KEY_CODES = {113}  # 'q'

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
        self.animation_delay_length = self.get_animation_delay_length()
        self.game_phase = GameOfLife.GAME_PHASES['initialization']
        self.menu = ['start simulation', 'create board', 'load board', 'quit']
        rows, cols = self.get_board_size()

        pygame.draw.rect(
            self.surface,
            GameOfLife.CANVAS_COLOR,
            [0, 0, self.screen_info.current_w, self.screen_info.current_h], 0)
        pygame.display.flip()

        self.menu_selections = {
            'board': {
                'rows': rows,
                'cols': cols,
                'live_cell_coords': self.load_board(rows, cols),
                'GUI_components': {
                    'draw_surface': self.surface,
                    'cell_width': self.screen_info.current_w / cols,
                    'cell_height': self.screen_info.current_h / rows,
                    'cell_shape_generator': pygame.Rect,  # always click rects
                    'cell_outline_color': self.get_item_color('cell outline'),
                    'alive_color': self.get_item_color('alive cell'),
                    'dead_color': self.get_item_color('dead cell'),
                    'cell_draw_func': self.get_cell_draw_func()
                }
            }
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
            'board': GameOfLifeBoard(**self.menu_selections['board'])
        }

        self.game['board'].display_self()
        pygame.display.flip()

        # player builds board by clicking on cells, then starts game
        pygame.event.get()  # clear events
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

        # simulate
        pygame.time.delay(self.animation_delay_length)
        while self.game['board'].advance_board_one_generation():
            pygame.display.flip()
            pygame.time.delay(self.animation_delay_length)

        # wait for player to quit
        self.game_phase = GameOfLife.GAME_PHASES['post-game']
        pygame.event.get()  # clear events
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

    def get_board_size(self):
        """
        Get user input for num of rows and cols in game.
        Return as a tuple.
        """
        while True:
            try:
                print('***************')
                rows = int(input('Enter number of rows: '))
                if 0 < rows <= 100:
                    break
            except:
                print('enter a number between 1 and 100')

        while True:
            try:
                print('***************')
                cols = int(input('Enter number of columns: '))
                if 0 < cols <= 100:
                    break
            except:
                print('enter a number between 1 and 100')

        return rows, cols

    def load_board(self, rows, cols):
        """
        Load a board from user input.
        Does not rigorously check for bad input.
        """
        live_cell_coords = set([])
        print('***************')
        print(
            'Enter comma and space-separated list of live cell coordinates.')
        print('Coordinates are zero-indexed from the top left, '
              'so (0,0) is the top left cell.')
        print(
            'Example: If cells (0,3) and (3,2) are alive, enter \'0,3 3,2\'.')
        print('Leave blank to provide no live cells.')

        # could improve defensiveness/readability of this logic
        while True:
            had_error = False
            live_cell_string = input()
            if len(live_cell_string) < 1:
                break
            live_cells = live_cell_string.split(' ')
            for live_cell in live_cells:
                coords = live_cell.split(',')
                try:
                    row = int(coords[0])
                    col = int(coords[1])
                    if (len(coords) != 2 or
                            not 0 <= row < rows or not 0 <= col < cols):
                        raise Exception
                    live_cell_coords.add((row, col))
                except:
                    print('Error processing live cells; please try again')
                    had_error = True
                    break
            if not had_error:
                break

        return live_cell_coords

    def get_item_color(self, item_to_color):
        """
        Get color for item from user input.
        Is allowed to conflict with other item colors.
        """
        print('***************')
        while True:
            color = input('Enter {} color: '.format(item_to_color))
            if color in GameOfLife.COLORS:
                return pygame.Color(color)
            print('Color not recognized')

    def get_cell_draw_func(self):
        """
        Return's the cell draw func based on user input.
        """
        print('***************')
        while True:
            shape = input(
                'Enter cell shape (either \'square\' or \'circle\'): ')
            if shape == 'square':
                return pygame.draw.rect
            elif shape == 'circle':
                return pygame.draw.ellipse

    def get_animation_delay_length(self):
        """
        Get the animation delay length based on user input.
        """
        print('***************')
        while True:
            try:
                speed = int(input('Enter animation speed (1 - 10, 10 being '
                                 'slowest): '))
                if 1 <= speed <= 10:
                    return 100*speed
            except:
                pass

if __name__ == '__main__':
    game = GameOfLife()
    game.start()
