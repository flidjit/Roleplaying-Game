import varlib
from varlib import default_terrain_tiles, default_ui_colors, default_keyboard_bindings


class Player:
    def __init__(self):
        self.name = 'Player'
        self.handle = None
        self.email = 'ThisGuy@righthere.com'
        self.gm_mode = False
        self.my_campaigns = []
        self.my_characters = {}
        self.ui_colors = varlib.default_ui_colors
        self.tab_icons = {}
        self.key_config = varlib.default_keyboard_bindings
        self.key_map = {}
        self.control_mode = 'GM Standard'
        self.cursor = None


class Thing3D:
    def __init__(self, x=0, y=0, z=0, thing_name='Stone',
                 model_name=None, facing='North', tags=None):
        self.name = thing_name
        if model_name:
            self.model_name = model_name
        else:
            self.model_name = 'catalog/terrain/basic/stone.gltf'
        self.facing = facing
        self.draw_at = [x, y, z]
        self.moving = [False, [0, 0]]
        if tags:
            self.tags = tags
        else:
            self.tags = []
        self.instance = None


class GridTile(Thing3D):
    def __init__(self, x=0, y=0, z=0, floor=False, occupied_by=None):
        Thing3D.__init__(self, x=x, y=y, z=z,
                         model_name='catalog/terrain/basic/stone.gltf')
        self.floor = floor
        self.occupied_by = occupied_by


class MapChunk:
    def __init__(self, chunk_id='Chunk 1', display_name='Starting Area',
                 description='The place to start your game',
                 tiles=None, characters=None, items=None,
                 active=True, minimap_color=None):
        self.chunk_id = chunk_id
        self.instance = None
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
            self.terrain_model_list = default_terrain_tiles
        if tiles_at:
            self.tiles_at = tiles_at
        else:
            self.tiles_at = {'0,0': 'Chunk 1'}
        if chunks:
            self.chunks = chunks
        else:
            self.chunks = {'Chunk 1': MapChunk(tiles={'0,0': GridTile(0, 0, 0)})}


class Being(Thing3D):
    def __init__(self, owner_name='GM', character_name='character'):
        Thing3D.__init__(self, thing_name=character_name)
        self.owner_name = owner_name


