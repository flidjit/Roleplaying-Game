from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import OrthographicLens, WindowProperties
import simplepbr
import tkinter as tk


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


class MapChunk:
    def __init__(self):
        self.name = ''
        self.terrain_model_list = []
        self.terrain_models = {}
        self.character_list = []
        self.characters = {}
        self.grid = [[]]


class Thing3D:
    def __init__(self):
        self.name = 'Thing'
        self.model_name = ''
        self.facing = 0
        self.draw_at = [0, 0, 0]
        self.tags = []


class GridSquare(Thing3D):
    def __init__(self):
        Thing3D.__init__(self)
        self.terrain_type = "Impassible"
        self.occupied_by = None


class Character(Thing3D):
    def __init__(self):
        Thing3D.__init__(self)
        self.player = {}
        self.stats = {}
        self.scores = {}
        self.skills = {}


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        simplepbr.init()
        self.props = WindowProperties()
        self.props.setTitle("Ashes of Alexandria")
        self.props.setSize(800, 400)
        self.win.requestProperties(self.props)

        self.lens = OrthographicLens()
        self.zoom_multiplier = 5
        self.set_zoom()
        self.cam.node().setLens(self.lens)
        self.camera_target = [0, 0, 0]
        self.target_offset = [0, 0, 0]
        self.camera_direction_index = 1
        self.set_camera_position()
        self.cooldown = {"camera rotation": 0}

        self.scene = self.loader.loadModel("Images/models1.gltf")
        self.scene.reparentTo(self.render)
        self.scene.setScale(1, 1, 1)
        self.scene.setPos(0, 0, 0)

        self.keyMap = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "space": False,
            "control": False,
            "e": False,
            "q": False }
        self.accept("arrow_up", self.updateKeyMap, ["up", True])
        self.accept("arrow_up-up", self.updateKeyMap, ["up", False])
        self.accept("arrow_down", self.updateKeyMap, ["down", True])
        self.accept("arrow_down-up", self.updateKeyMap, ["down", False])
        self.accept("arrow_left", self.updateKeyMap, ["left", True])
        self.accept("arrow_left-up", self.updateKeyMap, ["left", False])
        self.accept("arrow_right", self.updateKeyMap, ["right", True])
        self.accept("arrow_right-up", self.updateKeyMap, ["right", False])
        self.accept("space", self.updateKeyMap, ["space", True])
        self.accept("space-up", self.updateKeyMap, ["space", False])
        self.accept("control", self.updateKeyMap, ["Control", True])
        self.accept("control-up", self.updateKeyMap, ["Control", False])
        self.accept("e", self.updateKeyMap, ["e", True])
        self.accept("e-up", self.updateKeyMap, ["e", False])
        self.accept("q", self.updateKeyMap, ["q", True])
        self.accept("q-up", self.updateKeyMap, ["q", False])
        self.updateTask = taskMgr.add(self.update, "update")

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def set_camera_position(self):
        t = [self.camera_target[0]+self.target_offset[0],
             self.camera_target[1]+self.target_offset[1],
             self.camera_target[2]+self.target_offset[2]]
        d = movement_data[movement_data["Shift Index"][self.camera_direction_index]]
        print(movement_data["Shift Index"][self.camera_direction_index])
        self.cam.setPosHpr(t[0]+d[0], t[1]+d[1], t[2]+7.5, d[2], -45, 0)

    def shift_camera_rotation_index(self, direction='Right'):
        if direction == 'Right':
            if self.camera_direction_index >= 1:
                self.camera_direction_index -= 1
            else:
                self.camera_direction_index = 3
        if direction == 'Left':
            if self.camera_direction_index <= 2:
                self.camera_direction_index += 1
            else:
                self.camera_direction_index = 0

    def set_zoom(self):
        zm = self.zoom_multiplier
        self.lens.setFilmSize(2*zm, 1*zm)

    def update(self, task):
        dt = globalClock.getDt()
        f = movement_data[movement_data["Shift Index"][self.camera_direction_index] + " Move"]
        if self.camera_direction_index == 0 or self.camera_direction_index == 2:
            if self.keyMap["up"]:
                self.target_offset[1] += f[0]
                self.set_camera_position()
            if self.keyMap["down"]:
                self.target_offset[1] += f[1]
                self.set_camera_position()
            if self.keyMap["left"]:
                self.target_offset[0] += f[2]
                self.set_camera_position()
            if self.keyMap["right"]:
                self.target_offset[0] += f[3]
                self.set_camera_position()
        else:
            if self.keyMap["up"]:
                self.target_offset[0] += f[0]
                self.set_camera_position()
            if self.keyMap["down"]:
                self.target_offset[0] += f[1]
                self.set_camera_position()
            if self.keyMap["left"]:
                self.target_offset[1] += f[2]
                self.set_camera_position()
            if self.keyMap["right"]:
                self.target_offset[1] += f[3]
                self.set_camera_position()

        if self.keyMap["space"]:
            self.target_offset[0] = 0
            self.target_offset[1] = 0
            self.set_camera_position()
        if self.keyMap["e"]:
            if self.cooldown["camera rotation"] == 0:
                self.shift_camera_rotation_index('Right')
                self.set_camera_position()
                self.cooldown["camera rotation"] = 100
        if self.keyMap["q"]:
            if self.cooldown["camera rotation"] == 0:
                self.shift_camera_rotation_index('Left')
                self.set_camera_position()
                self.cooldown["camera rotation"] = 100
        for i in self.cooldown:
            if self.cooldown[i] >= 1:
                self.cooldown[i] -= 1
        return task.cont


app = MyApp()
app.run()
