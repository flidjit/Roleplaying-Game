import platform
import os
import proto as pt
import uiwin as uw
import tkinter as tk
from tkinter import ttk
from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from direct.actor.Actor import Actor
from panda3d.core import WindowProperties, OrthographicLens, NodePath, AmbientLight
from pandac.PandaModules import TransparencyAttrib
import simplepbr


# ToDo: * On Windows OS the models are rotated 90 degrees on one axis.
#       * Add compass art.
#       * Cursor functionality.
#       * Try to put groups of tile models into one gltf file.
#       * Scroll to zoom


class GameWindow(ShowBase):
    def __init__(self):
        ShowBase.__init__(self, windowType='none')
        # ____________________________________________________________
        # variable placeholders.
        self.gm_mode = True
        self.entity = {}
        self.cursor = None
        self.zoom_level = 8
        self.current_chunk = 'Chunk1'
        self.cooldown = {"camera rotation": 0, "cursor movement": 0}
        # ____________________________________________________________
        # tkinter stuff.
        self.startTk()
        self.root = self.tkRoot
        self.root['bg'] = 'black'
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
        # panda3D stuff.
        props = WindowProperties()
        props.setParentWindow(self.image_frame.winfo_id())
        props.setOrigin(0, 0)
        props.setSize(800, 400)
        self.win = base.makeDefaultPipe()
        base.openDefaultWindow(props=props)
        self.lens = OrthographicLens()
        self.cam.node().setLens(self.lens)
        self.move_to_location = [0, 0, 0]
        self.selector_location = [0, 0, 0]
        self.camera_target = [0, 0, 0]
        self.target_offset = [0, 0, 0]
        self.camera_direction_index = 2
        self.set_camera_position()
        self.set_zoom(1)
        self.current_map = pt.LocationMap()
        self.model_lib = {}
        self.node_lib = {'Model Buffer': NodePath('model-buffer')}
        self.instantiate_map()
        simplepbr.init()
        self.ambient_light = AmbientLight('ambient light')
        self.ambient_light.setColor((0.7, 0.7, 0.7, 1))
        self.ambient_light_node = render.attachNewNode(self.ambient_light)
        render.setLight(self.ambient_light_node)
        self.keyMap = {}
        self.configure_keys()
        self.updateTask = taskMgr.add(self.update, "update")
        # ____________________________________________________________
        # user system information.
        print(os.name+' - '+platform.machine())
        print(base.win.gsg.driver_renderer)
        print(platform.system()+' ('+platform.release()+')')

    def update_key_map(self, control_name, control_state):
        # add a key to the key map
        self.keyMap[control_name] = control_state

    def configure_keys(self):
        # add all the keys from the key map list
        k = pt.keyboard_list
        for i in range(len(k)):
            self.keyMap[k[i][1]] = False
            self.accept(k[i][0], self.update_key_map, [k[i][1], True])
            self.accept(k[i][0]+'-up', self.update_key_map, [k[i][1], False])

    def add_tile(self, x=0, y=0, z=0, chunk='Chunk1'):
        # create a new tile at the given location which belongs to the given group.
        id_xy = str(x)+','+str(y)
        if id_xy not in self.current_map.chunk_locations:
            self.current_map.chunks[chunk].tiles[id_xy] = GridTile(x, y, z)
            self.current_map.chunk_locations[id_xy] = chunk
            self.add_static_model(self.current_map.chunks[chunk].tiles[id_xy], chunk)

    def add_static_model(self, thing_3d=pt.Thing3D(), render_group='Chunk1'):
        # add the model to the library if it isn't there already, and draw an instance.
        # of it at the proper location.
        if thing_3d.model_name not in self.model_lib:
            self.model_lib[thing_3d.model_name] = self.loader.loadModel(thing_3d.model_name)
            self.model_lib[thing_3d.model_name].reparentTo(self.node_lib['Model Buffer'])
        thing_3d.instance = render.attachNewNode(render_group)
        loc = thing_3d.draw_at
        thing_3d.instance.setPos(loc[0], loc[1], loc[2])
        thing_3d.instance.setH(render, pt.movement_data[thing_3d.facing][2])
        self.model_lib[thing_3d.model_name].instanceTo(thing_3d.instance)

    def add_entity_model(self, thing_3d=pt.Thing3D()):


    def instantiate_map(self):
        # Draw the current map for the first time.
        if self.gm_mode:
            self.cursor = pt.Thing3D(model_name='catalog/terrain/basic/pointer.gltf')
            self.add_static_model(self.cursor, "Chunk1")
            self.cursor.instance.setTransparency(TransparencyAttrib.MAlpha)
            self.cursor.instance.setH(render, pt.movement_data[self.cursor.facing][2])
        for c in self.current_map.chunks:
            for s in self.current_map.chunks[c].tiles:
                group = self.current_map.chunks[c].chunk_id
                self.add_static_model(self.current_map.chunks[c].tiles[s], group)

    def set_camera_position(self):
        t = [self.camera_target[0]+self.target_offset[0],
             self.camera_target[1]+self.target_offset[1],
             self.camera_target[2]+self.target_offset[2]]
        d = pt.movement_data[pt.movement_data["Shift Index"][self.camera_direction_index]]
        self.cam.setPosHpr(t[0]+d[0], t[1]+d[1], t[2]+7.5, d[2], -45, 0)

    def shift_camera_rotation_index(self, direction='Right'):
        # Shift through the camera rotation indexes.
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

    def set_zoom(self, change=1):
        # Change how close the camera is.
        self.zoom_level += change
        z = self.zoom_level
        self.lens.setFilmSize(2*z, 1*z)

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
        if self.keyMap['w']:
            if self.cooldown["cursor movement"] == 0:
                self.cursor.instance.setH(render, pt.movement_data["North"][2])
                self.cooldown["cursor movement"] = 10
        if self.keyMap['s']:
            if self.cooldown["cursor movement"] == 0:
                self.cursor.instance.setH(render, pt.movement_data["South"][2])
                self.cooldown["cursor movement"] = 10
        if self.keyMap['d']:
            if self.cooldown["cursor movement"] == 0:
                self.cursor.instance.setH(render, pt.movement_data["East"][2])
                self.cooldown["cursor movement"] = 10
        if self.keyMap['a']:
            if self.cooldown["cursor movement"] == 0:
                self.cursor.instance.setH(render, pt.movement_data["West"][2])
                self.cooldown["cursor movement"] = 10
        for i in self.cooldown:
            if self.cooldown[i] >= 1:
                self.cooldown[i] -= 1
        return task.cont


tkinter_window = GameWindow()
tkinter_window.run()
