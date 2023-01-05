

keyboard_list = [
    ["arrow_up", "up"], ["arrow_down", "down"],
    ["arrow_left", "left"], ["arrow_right", "right"],
    ["space", "space"], ["control", "control"],
    ["e", "e"], ["q", "q"],
    ["a", "a"], ["s", "s"], ["w", "w"], ["d", "d"]]


movement_data = {
    "Shift Index": ["NW", "SW", "SE", "NE"],
    "SW": [-5, -5, -45],
    "SW Move": [0.05, -0.05, 0.05, -0.05],
    "SE": [5, -5, 45],
    "SE Move": [0.05, -0.05, -0.05, 0.05],
    "NW": [-5, 5, -135],
    "NW Move": [-0.05, 0.05, 0.05, -0.05],
    "NE": [5, 5, 135],
    "NE Move": [-0.05, 0.05, -0.05, 0.05],
    "North": [+1, 0, 90],
    "South": [-1, 0, 270],
    "East": [0, +1, 0],
    "West": [0, -1, 180]}


class Thing3D:
    def __init__(self, x=0, y=0, z=0,
                 model_name='catalog/terrain/basic/Floor1.gltf'):
        self.name = 'Thing'
        self.model_name = model_name
        self.facing = "North"
        self.draw_at = [x, y, z]
        self.move_to = [0, 0, 0]
        self.tags = []
        self.instance = None


class GridTile(Thing3D):
    def __init__(self, x=0, y=0, z=0):
        Thing3D.__init__(self, x=x, y=y, z=z)
        self.floor = False
        self.occupied_by = None


class MapChunk:
    def __init__(self):
        self.chunk_id = 'Chunk1'
        self.tiles = {'0,0': GridTile(0, 0, 0), '1,1': GridTile(1, 1, 0)}
        self.characters = {}
        self.items = {}
        self.active = True
        self.minimap_color = ['green', 'grey']
        # for squares - Key=location as a string (for example: '1,1')
        #               Value=square instance.


class LocationMap:
    def __init__(self):
        self.name = 'Menu'
        self.terrain_model_list = []
        self.chunk_locations = {'0,0': 'Chunk1', '1,1': 'Chunk1'}
        self.chunks = {'Chunk1': MapChunk()}


class Character(Thing3D):
    def __init__(self):
        Thing3D.__init__(self)
        self.player = 'GM'
        self.stats = {}
        self.scores = {}
        self.skills = {}
        self.campaign_info = {}


class Pointer(Thing3D):
    def __init__(self):
        Thing3D.__init__(self)
        self.selected_tile = '0,1'


class Player():
    def __init__(self):
        self.name = 'Player'
        self.handle = 'Plizzy'
        self.email = 'ThisGuy@righthere.com'
        self.gm_mode = False
        self.new_player = True
        self.token = None
        self.multiplayer_PCs = []
        self.single_player_PCs = [Character()]


helpfile = [
    'Arrow Keys : Move camera\n',
    'Q and E Keys : Rotate camera\n',
    'Spacebar : Reset camera to cursor\n',
    'ASWD Keys : Move cursor\n',
    'Shift+ASWD Keys : Rotate cursor\n',
    'Ctrl+N : New tile at pointer\n',
    'Ctrl+X : Delete tile at pointer\n'
]