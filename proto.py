

keyboard_list = [
    ["control", "control"], ['shift', 'shift'],
    ["arrow_up", "up"], ["arrow_down", "down"],
    ["arrow_left", "left"], ["arrow_right", "right"],
    ["space", "space"],
    ["e", "e"], ["q", "q"],
    ["a", "a"], ["s", "s"], ["w", "w"], ["d", "d"],
    ["n", "n"]]


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
    def __init__(self, x=0, y=0, z=0, thing_name='Thing',
                 model_file_location=None, facing='North', tags=None):
        self.name = thing_name
        if model_file_location:
            self.model_name = model_file_location
        else:
            self.model_name = 'catalog/terrain/basic/Floor1.gltf'
        self.facing = facing
        self.draw_at = [x, y, z]
        if tags:
            self.tags = tags
        else:
            self.tags = []
        self.instance = None


class GridTile(Thing3D):
    def __init__(self, x=0, y=0, z=0, floor=False, occupied_by=None):
        Thing3D.__init__(self, x=x, y=y, z=z)
        self.floor = floor
        self.occupied_by = occupied_by


class MapChunk:
    def __init__(self, chunk_id='Chunk 1', tiles=None, characters=None,
                 items=None, active=True, minimap_color=None):
        self.chunk_id = chunk_id
        if tiles:
            self.tiles = tiles
        else:
            self.tiles = {}
        if characters:
            self.characters = characters
        else:
            self.characters = {}
        if items:
            self.items = items
        else:
            self.items = {}
        self.active = active
        if minimap_color:
            self.minimap_color = minimap_color
        else:
            self.minimap_color = ['green', 'green1']


class LocationMap:
    def __init__(self, name='Menu', terrain_model_list=None, tiles_at=None, chunks=None):
        self.name = name
        self.terrain_model_list = terrain_model_list
        if tiles_at:
            self.tiles_at = tiles_at
        else:
            self.tiles_at = {'0,0': 'Chunk 1'}
        if chunks:
            self.chunks = chunks
        else:
            self.chunks = {'Chunk 1': MapChunk(tiles={'0,0': GridTile(0, 0, 0)})}


class GmPointer(Thing3D):
    def __init__(self, x=0, y=0, z=0, edit_chunk='Chunk 1'):
        Thing3D.__init__(self, x=x, y=y, z=z,
                         model_file_location='catalog/terrain/basic/pointer.gltf')
        self.edit_chunk = edit_chunk


class Character(Thing3D):
    def __init__(self, player='GM', stats=None, scores=None,
                 skills=None, campaign_data=None):
        Thing3D.__init__(self)
        self.player = player
        if stats:
            self.stats = stats
        else:
            self.stats = {
                'Monsters Slain': 0,
                'Creation Date': 1}
        if self.scores:
            self.scores = scores
        else:
            self.scores = {
                'Strength': 10,
                'Dexterity': 10}
        if self.skills:
            self.skills = skills
        else:
            self.skills = {}
        if self.campaign_data:
            self.campaign_data = campaign_data
        else:
            self.campaign_data = {
                'GM': 'Bob'}


class Player:
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