

keyboard_list = [
    ["arrow_up", "up"], ["arrow_down", "down"],
    ["arrow_left", "left"], ["arrow_right", "right"],
    ["space", "space"], ["control", "control"],
    ["e", "e"], ["q", "q"]]


movement_data = {
    "Shift Index": ["NW", "NE", "SW", "SE"],
    "NE": [-5, -5, -45],
    "NE Move": [0.05, -0.05, 0.05, -0.05],
    "NW": [5, -5, 45],
    "NW Move": [0.05, -0.05, -0.05, 0.05],
    "SW": [-5, 5, -135],
    "SW Move": [-0.05, 0.05, 0.05, -0.05],
    "SE": [5, 5, 135],
    "SE Move": [-0.05, 0.05, -0.05, 0.05]}


class Thing3D:
    def __init__(self, x=0, y=0, z=0):
        self.name = 'Thing'
        self.model_name = 'catalog/terrain/basic/Floor1.gltf'
        self.this_instance = None
        self.facing = 0
        self.draw_at = [x, y, z]
        self.tags = []


class GridSquare(Thing3D):
    def __init__(self, x=0, y=0, z=0):
        Thing3D.__init__(self, x=x, y=y, z=0)
        self.terrain_type = "Impassable"
        self.occupied_by = None


class MapChunk:
    def __init__(self):
        self.name = ''
        self.terrain_model_list = []
        self.character_list = []
        self.grid = [[GridSquare(x, y) for x in range(20)] for y in range(20)]


class Character(Thing3D):
    def __init__(self):
        Thing3D.__init__(self)
        self.player = {}
        self.stats = {}
        self.scores = {}
        self.skills = {}