
default_ui_colors = {
            'Root BG': '#240e28',
            'TNotebook - BG': "#240e28",
            'TNotebook.Tab - BG': "#240e28",
            'TNotebook.Tab - FG': "white",
            'TNotebook.Tab - Selected BG': "#d8247c",
            'TNotebook.Tab - Selected FG': "black",
            'ChatSection - BG': "black",
            'ChatSection - FG': "#25a9f0",
            'InputSection - BG': "black",
            'InputSection - FG': "green",
            'SheetTab - BG': "black",
            'SheetTab - Text': "white",
            'MiniMap - BG': "#0c090d",
            'MapTab - BG': "black",
            'MapTab - Text': "white",
            'PropTab - BG': "black"}


keyboard_list = [
    ["control", "control"], ['shift', 'shift'],
    ["arrow_up", "up"], ["arrow_down", "down"],
    ["arrow_left", "left"], ["arrow_right", "right"],
    ["space", "space"],
    ["page_up", "page up"], ["page_down", "page down"],
    ["e", "e"], ["q", "q"],
    ["a", "a"], ["s", "s"], ["w", "w"], ["d", "d"],
    ["f", "f"]]


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


basic_terrain = {
    'Purple': 'catalog/terrain/basic/purp.gltf',
    'Stone': 'catalog/terrain/basic/stone.gltf',
    'Brick': 'catalog/terrain/basic/brick1.gltf',
    'Floor': 'catalog/terrain/basic/standardTile.gltf',
    'Pointer': 'catalog/terrain/basic/pointer.gltf'}


class Thing3D:
    def __init__(self, x=0, y=0, z=0, thing_name='Floor',
                 model_file_location=None, facing='North', tags=None):
        self.name = thing_name
        if model_file_location:
            self.model_file_location = model_file_location
        else:
            self.model_file_location = 'catalog/terrain/basic/stone.gltf'
        self.facing = facing
        self.draw_at = [x, y, z]
        if tags:
            self.tags = tags
        else:
            self.tags = []
        self.instance = None


class GridTile(Thing3D):
    def __init__(self, x=0, y=0, z=0, floor=False, occupied_by=None):
        Thing3D.__init__(self, x=x, y=y, z=z,
                         model_file_location='catalog/terrain/basic/stone.gltf')
        self.floor = floor
        self.occupied_by = occupied_by


class MapChunk:
    def __init__(self, chunk_id='Chunk 01', display_name='Starting Area',
                 description='The place to start your game',
                 tiles=None, characters=None, items=None,
                 active=True, minimap_color=None):
        self.chunk_id = chunk_id
        self.display_name = display_name
        self.description = description
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
    def __init__(self, name='Menu', terrain_model_list=None,
                 terrain_texture_list=None, tiles_at=None, chunks=None):
        self.name = name
        if terrain_model_list:
            self.terrain_model_list = terrain_model_list
        else:
            self.terrain_model_list = basic_terrain
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
    def __init__(self, player_name='GM', character_name='character',
                 stats=None, scores=None, props=None,
                 skills=None, traits=None, techniques=None,
                 campaign_data=None):
        Thing3D.__init__(self, thing_name=character_name)
        self.player_name = player_name
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
                'HP': [30, 30],
                'Energy': {'EP': [10, 10]},
                'AP': [6, 6],
                'Defense': 10,
                'Attack': None,
                'UPs': 0,
                'Power Level': 0}
        if self.techniques:
            self.techniques = techniques
        else:
            self.techniques = {}
        if self.skills:
            self.skills = skills
        else:
            self.skills = {}
        if self.traits:
            self.traits = traits
        else:
            self.traits = {}
        if props:
            self.props = props
        else:
            self.props = {}
        if self.campaign_data:
            self.campaign_data = campaign_data
        else:
            self.campaign_data = {
                'GM': 'Bob'}


class Player:
    def __init__(self):
        self.name = 'Player'
        self.handle = None
        self.email = 'ThisGuy@righthere.com'
        self.gm_mode = False
        self.my_campaigns = []
        self.my_characters = []
        self.selected = {
            'Character to Use:': None,
            'Chunk to Edit': None,
            'Tile to Place': None}
        self.ui_colors = default_ui_colors
        self.key_config = keyboard_list
        self.key_map = {}
        self.control_mode = 'GM Standard'
        self.cursor = None


