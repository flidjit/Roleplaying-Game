import pickle
from tools import TBag


class PlayerData:
    def __init__(self):
        self.name = 'Player Name'
        self.email = 'thisone@there.com'
        self.male_gender = True
        self.machine_data = {
            "OS": None,
            "Machine": None,
            "System": None,
            "Release": None,
            "OpenGL Version": None,
            "Vendor": None,
            "Renderer": None}


class ThePlayer:
    """
    * keyboard input, and camera movement.
    * Character party objects in pc_party.
    * Cool-downs for input and such.
    """
    def __init__(self, aoa_window=None,
                 player_data=PlayerData()):
        self.aoa_window = aoa_window
        self.data = player_data
        self.is_gm = False
        self.current_rps = 'AOARP'
        self.current_campaign = 'Beginner Campaign'
        self.current_character = 'Character Name'
        self.pc_party = {}
        self.npc_sidebar = {}
        self.cooldowns = {}
        self.cam = None
        self.cursor_3D = None
        self.key_map = {}
        self.key_config = []
        self.initialize()

    def initialize(self):
        self.configure_keys()

    def update(self):
        for i in self.cooldowns:
            if self.cooldowns[i] >= 0:
                self.cooldowns[i] -= 1
        keys = self.key_map
        for i in keys:
            print('key check:'+i)

    def configure_keys(self):
        k = self.key_config
        for i in range(len(k)):
            self.key_map[k[i][1]] = False
            self.aoa_window.accept(k[i][0], self.update_key_map, [k[i][1], True])
            self.aoa_window.accept(k[i][0] + '-up', self.update_key_map, [k[i][1], True])

    def update_key_map(self, control_name, control_state):
        self.key_map[control_name] = control_state

    def save_player_data(self):
        print('save the damned data')

