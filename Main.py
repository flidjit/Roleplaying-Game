import tkinter as tk
import proto as pt
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import WindowProperties, OrthographicLens, NodePath


class GameWindow(ShowBase):
    def __init__(self):
        ShowBase.__init__(self, windowType='none')
        self.startTk()

        self.root = self.tkRoot
        self.image_frame = tk.Frame(self.root, width=800, height=400)
        self.image_frame.grid()
        self.text = tk.Text(self.root, height=5, bg='black', fg='white')
        self.text.grid(sticky='we')
        self.root.update()

        props = WindowProperties()
        props.setParentWindow(self.image_frame.winfo_id())
        props.setOrigin(0, 0)
        props.setSize(800, 400)
        self.win = base.makeDefaultPipe()
        base.openDefaultWindow(props=props)

        self.lens = OrthographicLens()
        self.zoom_multiplier = 5
        self.cam.node().setLens(self.lens)
        self.camera_target = [0, 0, 0]
        self.target_offset = [0, 0, 0]
        self.camera_direction_index = 1
        self.cooldown = {"camera rotation": 0}
        self.set_camera_position()
        self.set_zoom()

        self.current_map = pt.MapChunk()
        self.terrain_models = {}
        self.mod_lib = NodePath('model-library')
        self.instantiate_map()

        self.keyMap = {}
        self.configure_keys()
        self.updateTask = taskMgr.add(self.update, "update")

    def update_key_map(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def configure_keys(self):
        k = pt.keyboard_list
        for i in range(len(k)):
            self.keyMap[k[i][1]] = False
            self.accept(k[i][0], self.update_key_map, [k[i][1], True])
            self.accept(k[i][0]+'-up', self.update_key_map, [k[i][1], False])

    def instantiate_map(self):
        self.character = self.loader.loadModel("Images/models1.gltf")
        self.character.reparentTo(render)
        for y in range(20):
            for x in range(20):
                m_name = self.current_map.grid[x][y].model_name
                if m_name not in self.terrain_models:
                    self.terrain_models[m_name] = self.loader.loadModel(m_name)
                    self.terrain_models[m_name].reparentTo(self.mod_lib)
                self.current_map.grid[x][y].this_instance = render.attachNewNode('grid-square')
                self.current_map.grid[x][y].this_instance.setPos(x, y, 0)
                self.terrain_models[m_name].instanceTo(self.current_map.grid[x][y].this_instance)

    def set_camera_position(self):
        t = [self.camera_target[0]+self.target_offset[0],
             self.camera_target[1]+self.target_offset[1],
             self.camera_target[2]+self.target_offset[2]]
        d = pt.movement_data[pt.movement_data["Shift Index"][self.camera_direction_index]]
        print(pt.movement_data["Shift Index"][self.camera_direction_index])
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
        self.root.update()
        f = pt.movement_data[pt.movement_data["Shift Index"][self.camera_direction_index] + " Move"]
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


tkinter_window = GameWindow()
tkinter_window.run()
