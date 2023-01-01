

keyboard_list = [
    ["arrow_up", "up"], ["arrow_down", "down"],
    ["arrow_left", "left"], ["arrow_right", "right"],
    ["space", "space"], ["control", "control"],
    ["e", "e"], ["q", "q"]]


movement_data = {
    "Shift Index": ["NW", "SW", "SE", "NE"],
    "SW": [-5, -5, -45],
    "SW Move": [0.05, -0.05, 0.05, -0.05],
    "SE": [5, -5, 45],
    "SE Move": [0.05, -0.05, -0.05, 0.05],
    "NW": [-5, 5, -135],
    "NW Move": [-0.05, 0.05, 0.05, -0.05],
    "NE": [5, 5, 135],
    "NE Move": [-0.05, 0.05, -0.05, 0.05]}


class Thing3D:
    def __init__(self, x=0, y=0, z=0):
        self.name = 'Thing'
        self.model_name = 'catalog/terrain/basic/Floor1.gltf'
        self.facing = 0
        self.draw_at = [x, y, z]
        self.tags = []
        self.instance = None


class GridTile(Thing3D):
    def __init__(self, x=0, y=0, z=0):
        Thing3D.__init__(self, x=x, y=y, z=z)
        self.floor = False
        self.occupied_by = None
        self.minimap_color = 'green'


class MapChunk:
    def __init__(self):
        self.chunk_id = ''
        self.tiles = {'0,0': GridTile(0, 0, 0),'1,1': GridTile(1, 1, 0)}
        self.active = True
        # for squares - Key=location as a string (for example: '1,1')
        #               Value=square instance.


class LocationMap:
    def __init__(self):
        self.name = 'Menu'
        self.terrain_model_list = []
        self.chunks = {'Chunk1': MapChunk()}


class Character(Thing3D):
    def __init__(self):
        Thing3D.__init__(self)
        self.player = {}
        self.stats = {}
        self.scores = {}
        self.skills = {}
