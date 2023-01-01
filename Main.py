import tkinter as tk
from tkinter import ttk
import proto as pt
import uiwin as uw
from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import WindowProperties, OrthographicLens, NodePath, AmbientLight
from pandac.PandaModules import TransparencyAttrib
import simplepbr


class GameWindow(ShowBase):
    def __init__(self):
        ShowBase.__init__(self, windowType='none')
        self.startTk()
        self.root = self.tkRoot
        self.root['bg'] = 'black'
        self.gm_mode = True
        # ____________________________________________________________
        self.image_frame = tk.Frame(self.root, width=800, height=400)
        self.image_frame.grid(column=0, row=0)
        self.chat_output = uw.ChatSection(self.root)
        self.chat_output.grid(column=0, row=1, sticky='we')
        self.text_input = uw.InputSection(self.root)
        self.text_input.grid(column=0, row=2, sticky='we')
        self.tab_frame = uw.TabSection(self.root)
        self.tab_frame.grid(column=1, row=0, rowspan=3, sticky='ns')
        self.root.update()
        # ____________________________________________________________
        props = WindowProperties()
        props.setParentWindow(self.image_frame.winfo_id())
        props.setOrigin(0, 0)
        props.setSize(800, 400)
        self.win = base.makeDefaultPipe()
        base.openDefaultWindow(props=props)
        # ____________________________________________________________
        self.lens = OrthographicLens()
        self.cam.node().setLens(self.lens)
        self.selector_location = [0, 0, 0]
        self.camera_target = [0, 0, 0]
        self.target_offset = [0, 0, 0]
        self.camera_direction_index = 2
        self.cooldown = {"camera rotation": 0}
        self.set_camera_position()
        self.set_zoom(4)
        # ____________________________________________________________
        self.current_map = pt.LocationMap()
        self.model_lib = {}
        self.node_lib = {'Model Buffer': NodePath('model-buffer')}
        self.instantiate_map()
        # ____________________________________________________________
        simplepbr.init()
        self.ambient_light = AmbientLight('ambient light')
        self.ambient_light.setColor((0.7, 0.7, 0.7, 1))
        self.ambient_light_node = render.attachNewNode(self.ambient_light)
        render.setLight(self.ambient_light_node)
        # ____________________________________________________________
        self.keyMap = {}
        self.configure_keys()
        self.updateTask = taskMgr.add(self.update, "update")

    def update_key_map(self, control_name, control_state):
        self.keyMap[control_name] = control_state

    def configure_keys(self):
        k = pt.keyboard_list
        for i in range(len(k)):
            self.keyMap[k[i][1]] = False
            self.accept(k[i][0], self.update_key_map, [k[i][1], True])
            self.accept(k[i][0]+'-up', self.update_key_map, [k[i][1], False])

    def instantiate_map(self):
        # fix the janky node structure.
        self.character = self.loader.loadModel("catalog/terrain/basic/pointer.gltf")
        self.character.setTransparency(TransparencyAttrib.MAlpha)
        self.character.reparentTo(render)
        for c in self.current_map.chunks:
            for s in self.current_map.chunks[c].tiles:
                m_name = self.current_map.chunks[c].tiles[s].model_name
                if m_name not in self.model_lib:
                    self.model_lib[m_name] = self.loader.loadModel(m_name)
                    self.model_lib[m_name].reparentTo(self.node_lib['Model Buffer'])
                self.current_map.chunks[c].tiles[s].instance = render.attachNewNode('grid-square')
                dl = self.current_map.chunks[c].tiles[s].draw_at
                self.current_map.chunks[c].tiles[s].instance.setPos(dl[0], dl[1], dl[2])
                self.model_lib[m_name].instanceTo(self.current_map.chunks[c].tiles[s].instance)

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

    def set_zoom(self, multiplier=4):
        self.lens.setFilmSize(2*multiplier, 1*multiplier)

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
