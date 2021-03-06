

class GameOfLifeCell(object):
    """
    Represent a cell in the Game of Life.
    """
    def __init__(
            self, row, col, is_alive=False, GUI_components=None):
        """
        Init a cell in the Game of Life.
        Clients should provide any GUI components they expect to use, such
        as shapes, colors, draw functions, etc.
        """
        if GUI_components is None:
            GUI_components = {}
        self.row = row
        self.col = col
        self.is_alive = is_alive
        self.stats = {
            'gens_alive': 0,
            'gens_dead': 0,
            'longest_living_streak': 0,
            'current_living_streak': 0,
            'longest_death_streak': 0,
            'current_death_streak': 0,
            'births': 0,
            'deaths': 0
        }
        self.GUI_components = GUI_components

    def draw_outline(self):
        """
        If possible, draw outline with thickness 1 around cell's shape.
        """
        if any(not self.GUI_components.get(GUI_key) for GUI_key in
               ['shape', 'draw_func', 'outline_color']):
            return None
        shape = self.GUI_components['shape']
        self.GUI_components['draw_func'](
            self.GUI_components['outline_color'],
            [shape.x-1, shape.y-1, shape.width+2, shape.height+2], 1)

    def draw_self(self, stat_modifiers=None):
        """
        Draw the cell to the GUI.
        Depends on client providing a GUI draw function which takes a color
        (alive or dead), shape, and outline thickness/shape fill flag
        as parameters.

        :param stat_modifiers: dict of instructions for drawing the cell
        as a stat.
        """
        if any(not self.GUI_components.get(GUI_key) for GUI_key in
               ['shape', 'draw_func', 'alive_color',
                'dead_color', 'get_fill_param']):
            return None

        old_alpha = None
        if stat_modifiers:
            color = self.GUI_components.get('alive_color')
            old_alpha = color.a
            color.a = stat_modifiers.get('alpha')
        else:
            color = (self.GUI_components.get('alive_color') if self.is_alive
                     else self.GUI_components.get('dead_color'))

        self.GUI_components['draw_func'](
            color, self.GUI_components.get('shape'),
            self.GUI_components['get_fill_param'](self.is_alive))

        self.GUI_components['current_alpha'] = color.a
        if old_alpha:
            color.a = old_alpha
