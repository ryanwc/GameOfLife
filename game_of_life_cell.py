

class GameOfLifeCell(object):
    """
    Represent a cell in the Game of Life.
    """
    def __init__(
            self, row, col, is_alive=False, GUI_components=None):
        if GUI_components is None:
            GUI_components = {}
        self.row = row
        self.col = col
        self.is_alive = is_alive
        self.GUI_components = GUI_components

    def set_alive_status(self, is_alive):
        self.is_alive = is_alive

    def draw_self(self):
        """
        """
        color = (self.GUI_components.get('alive_color') if self.is_alive else
                 self.GUI_components.get('dead_color'))
        self.GUI_components['draw_func'](
            color, self.GUI_components.get('shape'),
            self.GUI_components['get_fill_param'](self.is_alive))
        print('drew cell ({},{})'.format(self.row, self.col))
