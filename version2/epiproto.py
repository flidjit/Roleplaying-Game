from proto import *
from toolkit import InputHandler, MobHandler
from panda3d.core import NodePath, OrthographicLens


class TheStage:
    def __init__(self):
        self.data = MapData()
        self.model_library = {}
        self.node_library = {}
        self.hidden_buffer = NodePath()

    def update(self, aoa_window=None):
        MobHandler.motivate_mobs(aoa_window)

    def build_texture_library(self):
        print('build the texture library')

    def build_model_library(self):
        print('build the model library')

    def build_node_library(self):
        print('build chunk nodes')

    def place_instance(self):
        print('place an instance')

    def change_texture(self):
        print('change a texture')

    def build_map(self):
        print('build the map')


class TheCameraman:
    def __init__(self, cam=None):
        self.cam = cam
        self.lens = OrthographicLens()
        self.cam.node().setLens(self.lens)
        self.focused_on = None
        self.facing = "North-West"
        self.traveling = False
        self.shift_offset = [0, 0]
        self.zoom_factor = 33
        self.view_angle = 10

    def update(self, aoa_window=None):
        print('update')

    def follow(self):
        print('follow')

    def rotate(self):
        print('rotate')

    def zoom(self):
        print('zoom')

    def angle(self):
        print('set_angle')


class ThePlayer:
    def __init__(self, aoa_window=None):
        self.data = PlayerData()
        self.is_gm = False
        self.current_universe = 'AOA'
        self.current_campaign = 'Beginner Campaign'
        self.current_character = 'Character Name'
        self.pc_party = {}
        self.cooldowns = {}
        self.initialize_(aoa_window)

    def initialize_(self, aoa_window=None):
        self.configure_keys(aoa_window)

    def update(self, aoa_window=None):
        for i in self.cooldowns:
            if self.cooldowns[i] >= 0:
                self.cooldowns[i] -= 1
        InputHandler.get_input(aoa_window)

    def configure_keys(self, aoa_window=None):
        k = self.data.key_config
        for i in range(len(k)):
            self.data.key_map[k[i][1]] = False
            aoa_window.accept(k[i][0], self.update_key_map, [k[i][1], True])
            aoa_window.accept(k[i][0]+'-up', self.update_key_map, [k[i][1], True])

    def update_key_map(self, control_name, control_state):
        self.data.key_map[control_name] = control_state
