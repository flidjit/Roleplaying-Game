
class PlayerData:
    def __init__(self):
        self.name = 'Player Name'
        self.email = 'thisone@there.com'
        self.ui_config = {}
        self.key_map = {}
        self.key_config = []


class RenderedObject:
    def __init__(self):
        self.vector_ = [0, 0, 0]
        self.facing = 'North'
        self.chunk_family = 'Chunk Name'
        self.instance = None
        self.texture_1_name = 'Texture'
        self.tex_stage_1 = None
        self.texture_2_name = 'Texture'
        self.tex_stage_2 = None


class Character(RenderedObject):
    def __init__(self):
        RenderedObject.__init__(self)
        self.is_moving = False
        self.coming_from = [0, 0]
        self.heading_to = [0, 0]

        self.name = 'Character Name'
        self.owner = 'Player Name'
        self.description = {
            'Bio': 'Some Dude.',
            'Height': [5, 9],
            'Weight': 140,
            'Skin Color': 'Green',
            'Eye Color': 'Yellow',
            'Age': 20}
        self.power_level = 0
        self.ups = 50
        self.hp = [30, 30]
        self.ap = [6, 6]
        self.energy = {
            'EP': [10, 10]}
        self.defense = {
            'Body': 0,
            'Mind': 0,
            'Spirit': 0}
        self.resistances = {}
        self.weaknesses = {}
        self.status_effects = []
        self.loadout = {
            'Left': None,
            'Right': None}
        self.pack = []
        self.gear = {
            'Head': None,
            'Face': None,
            'Neck': None,
            'Back': None,
            'Shoulders': None,
            'Arms': None,
            'Wrists': None,
            'Hands': None,
            'Torso': None,
            'Waist': None,
            'Legs': None,
            'Knees': None,
            'Shins': None,
            'Feet': None}
        self.rings = {
            'Right': [],
            'Left': []}
        self.key_items = []
        self.skills = {}
        self.traits = {}
        self.techniques = {}
        self.card_list = {}


class Decoration(RenderedObject):
    def __init__(self):
        RenderedObject.__init__(self)


class Effect(RenderedObject):
    def __init__(self):
        RenderedObject.__init__(self)


class TargetPointer(RenderedObject):
    def __init__(self):
        RenderedObject.__init__(self)


class MapTile(RenderedObject):
    def __init__(self):
        RenderedObject.__init__(self)
        self.tile_id = '0,0'
        self.height_offset = 0


class MapData:
    def __init__(self):
        self.name = 'Map Name'
        self.description = 'A map of the location.'
        self.texture_list = []
        self.model_list = []
        self.chunks = {
            'Chunk Name': MapChunk()}
        self.non_player_characters = {}
        self.enemies = {}


class MapChunk:
    def __init__(self):
        self.name = 'Chunk Name'
        self.description = 'A chunk of the map.'
        self.visible = True
        self.tiles = {
            '0,0': MapTile()}
        self.decorations = {}

