import platform
import os
import proto as pt
import uiwin as uw
import tkinter as tk
from tkinter import ttk
from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from direct.actor.Actor import Actor
from panda3d.core import WindowProperties, OrthographicLens, NodePath, AmbientLight, TextureStage
from pandac.PandaModules import TransparencyAttrib, TexGenAttrib
import simplepbr


# ToDo: * BUG: On Windows OS the models are rotated 90 degrees on one axis.
#       * Delete tile.
#       * New Chunk.
#       * Turn on/off visibility to chunks/characters.
#       * Edit tile.
#       * Save maps.
#       * Load character models.
#       * Add characters to the map.
#       * Smooth movement.
#       * Campaign structure.
#       * World map: user provided image with a measurement tool for travel, and movable markers.
#       * World map generator.
#       * Modes: Single Player, Multiplayer [Player, GM]
#       * Triggers for single player, and turning on/off characters and chunks automatically.
#       * tile types: Door, Ramp/Stairs, Floor, Mud/Water, Difficult Terrain
#       * object types: Container, Furniture, Fence/Wall/, Decorations
#       * Support for vehicles/Mounts.
#       * Support for larger characters/objects.
#       * Background parented to the camera.
#       * Add compass art parented to the camera.
#       * Combat System.


class GameWindow(ShowBase):
    def __init__(self):
        ShowBase.__init__(self, windowType='none')
        # ____________________________________________________________
        # default variables.
        self.gm_mode = True
        self.entity = {}
        self.control_entity = 'GM'
        self.control_chunk = 'Chunk 1'
        self.cursor = None
        self.zoom_level = 6
        self.cooldown = {"camera rotation": 0, "cursor movement": 0}
        # ____________________________________________________________
        # tkinter stuff.
        self.startTk()
        self.ttk_style = ttk.Style()
        self.ttk_style.configure('TNotebook.Tab', background="#240e28")
        self.ttk_style.configure('TNotebook', background="#240e28")
        self.ttk_style.configure('TNotebook', tabmargines=[0, 0, 0, 0])
        self.ttk_style.configure('TNotebook.Tab', padding=[0, 0])
        self.ttk_style.map('TNotebook.Tab', background=[('selected', "#d8247c")])
        self.ttk_style.map('TNotebook.Tab', foreground=[('selected', "black")])
        self.ttk_style.configure('TNotebook.Tab', foreground="white")
        self.root = self.tkRoot
        self.root['bg'] = '#240e28'
        self.root.geometry("1210x620")
        self.root.resizable(False, False)
        self.image_frame = tk.Frame(self.root, width=800, height=400)
        self.image_frame.place(x=20, y=20)
        self.chat_output = uw.ChatSection(self.root)
        self.chat_output.place(x=20, y=440, width=800, height=133)
        self.text_input = uw.InputSection(self.root)
        self.text_input.place(x=20, y=580, width=800, height=20)
        self.tab_frame = uw.TabSection(self.root)
        self.tab_frame.place(x=840, y=20)
        self.root.update()
        # ____________________________________________________________
        # panda3D stuff.
        props = WindowProperties()
        props.setParentWindow(self.image_frame.winfo_id())
        props.setOrigin(0, 0)
        props.setSize(800, 400)
        self.win = base.makeDefaultPipe()
        base.openDefaultWindow(props=props)
        base.setBackgroundColor(0.007, 0, 0.007, 1)
        self.lens = OrthographicLens()
        self.cam.node().setLens(self.lens)
        self.move_to_location = [0, 0, 0]
        self.camera_target = [0, 0, 0]
        self.camera_target_offset = [0, 0, 0]
        self.camera_direction_index = 2
        self.current_map = pt.LocationMap()
        self.model_lib = {}
        self.texture_lib = {}
        self.tex_stage = TextureStage('Textures')  # !@%
        self.tex_stage.setMode(TextureStage.MReplace)
        self.prepare_tile_textures()  # !@%
        self.node_lib = {'Model Buffer': NodePath('model-buffer')}
        self.instantiate_map()
        simplepbr.init()
        self.ambient_light = AmbientLight('ambient light')
        self.ambient_light.setColor((0.7, 0.7, 0.7, 1))
        self.ambient_light_node = render.attachNewNode(self.ambient_light)
        render.setLight(self.ambient_light_node)
        self.keyMap = {}
        self.configure_keys()
        self.set_camera_position()
        self.set_zoom(1)
        self.updateTask = taskMgr.add(self.update, "update")
        # ____________________________________________________________
        # user system information.
        print(os.name+' - '+platform.machine())
        print(base.win.gsg.driver_renderer)
        print(platform.system()+' ('+platform.release()+')')
        self.swap_tile_texture(
            self.current_map.chunks['Chunk 1'].tiles['0,0'].instance)  # !@%

    def prepare_tile_textures(self):  # !@%
        t = pt.basic_tile_textures
        for i in t:
            self.texture_lib[i] = loader.loadTexture(t[i])

    def swap_tile_texture(self, tile=None, texture_name='Purple'):  # !@%
        if tile:
            tile.setTexGen(self.tex_stage, 1)
            tile.clearTexture(self.tex_stage)
            tile.setTexture(self.tex_stage, self.texture_lib[texture_name])

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

    def add_tile(self, x=1, y=0, z=0, chunk='Chunk 1'):  # !@%
        # create a new tile at the given location which belongs to the given group.
        id_xy = str(x)+','+str(y)
        # !!Need to load animated models so I can use the GM pointer to reference the tile to change.
        if id_xy not in self.current_map.tiles_at:
            self.current_map.chunks[chunk].tiles[id_xy] = pt.GridTile(x, y, z)
            self.current_map.tiles_at[id_xy] = chunk
            self.add_static_instance(self.current_map.chunks[chunk].tiles[id_xy], chunk)

    def gm_add_tile(self):  # !@%
        move = pt.movement_data
        gm = self.entity['GM']
        x = gm.draw_at[0] + move[gm.facing][1]
        y = gm.draw_at[1] + move[gm.facing][0]
        z = gm.draw_at[2]
        tid = str(x)+','+str(y)
        if tid not in self.current_map.tiles_at:
            col = self.current_map.chunks[self.control_chunk].minimap_color
            self.tab_frame.map_tab.minimap.add_square(x=x, y=y, square_id=tid, color=col)
            self.add_tile(x=x, y=y, z=z, chunk=self.control_chunk)
            print('created new tile at: ('+tid+') in chunk: '+self.control_chunk)

    def add_static_instance(self, thing_3d=pt.Thing3D(), render_group='Chunk 1'):
        # add the model to the library if it isn't there already, and draw an instance.
        # of it at the proper location.
        thing_3d.instance = render.attachNewNode(render_group)
        loc = thing_3d.draw_at
        thing_3d.instance.setPos(loc[0], loc[1], loc[2])
        thing_3d.instance.setH(render, pt.movement_data[thing_3d.facing][2])
        self.model_lib[thing_3d.model_name].instanceTo(thing_3d.instance)

    def add_gm_pointer(self):
        self.entity['GM'] = pt.GmPointer()
        self.add_static_instance(self.entity['GM'], "Chunk 1")
        self.entity['GM'].instance.setTransparency(TransparencyAttrib.MAlpha)
        self.entity['GM'].instance.setH(render, pt.movement_data[self.entity['GM'].facing][2])

    def face_this_towards(self, facing='North'):
        # I'm going to have to give this the same treatment as the camera
        # rotation IE: indexing based on camera direction.
        self.entity[self.control_entity].facing = facing
        instance = self.entity[self.control_entity].instance
        if instance:
            instance.setH(render, pt.movement_data[facing][2])
            self.cooldown["cursor movement"] = 10

    def move_this_towards(self, moving='North'):
        ta = self.current_map.tiles_at
        e = self.entity[self.control_entity]
        move = pt.movement_data
        x = e.draw_at[0] + move[moving][1]
        y = e.draw_at[1] + move[moving][0]
        z = e.draw_at[2]
        tid = str(x)+','+str(y)
        instance = self.entity[self.control_entity].instance
        if tid in ta:
            if instance:
                self.camera_target = [x, y, z]
                self.camera_target_offset = [0, 0, 0]
                self.set_camera_position()
                instance.setPos(x, y, z)
                e.draw_at = [x, y, z]

    def instantiate_map(self):
        # Draw the current map for the first time.
        self.prepare_tile_textures()
        for i in self.current_map.terrain_model_list:
            m = self.current_map.terrain_model_list[i]
            self.model_lib[m] = self.loader.loadModel(m)
            self.model_lib[m].reparentTo(self.node_lib['Model Buffer'])
        if self.gm_mode:
            self.add_gm_pointer()
        for c in self.current_map.chunks:
            for s in self.current_map.chunks[c].tiles:
                group = self.current_map.chunks[c].chunk_id
                self.add_static_instance(self.current_map.chunks[c].tiles[s], group)
                self.current_map.chunks[c].tiles[s].instance.set_shader_auto(True)

    def set_camera_position(self):
        t = [self.camera_target[0] + self.camera_target_offset[0],
             self.camera_target[1] + self.camera_target_offset[1],
             self.camera_target[2] + self.camera_target_offset[2]]
        d = pt.movement_data[pt.movement_data["Shift Index"][self.camera_direction_index]]
        self.cam.setPosHpr(t[0]+d[0], t[1]+d[1], t[2]+5.5, d[2], -35, 0)

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

    def set_zoom(self, change=1.0):
        # Change how close the camera is.
        self.zoom_level += change
        z = self.zoom_level
        self.lens.setFilmSize(2*z, 1*z)

    def update(self, task):
        self.root.update()
        f = pt.movement_data[pt.movement_data["Shift Index"][self.camera_direction_index] + " Move"]
        if self.camera_direction_index == 0 or self.camera_direction_index == 2:
            # figure out a different way to do this.
            if self.keyMap["up"]:
                self.camera_target_offset[1] += f[0]
                self.set_camera_position()
            if self.keyMap["down"]:
                self.camera_target_offset[1] += f[1]
                self.set_camera_position()
            if self.keyMap["left"]:
                self.camera_target_offset[0] += f[2]
                self.set_camera_position()
            if self.keyMap["right"]:
                self.camera_target_offset[0] += f[3]
                self.set_camera_position()
        else:
            if self.keyMap["up"]:
                self.camera_target_offset[0] += f[0]
                self.set_camera_position()
            if self.keyMap["down"]:
                self.camera_target_offset[0] += f[1]
                self.set_camera_position()
            if self.keyMap["left"]:
                self.camera_target_offset[1] += f[2]
                self.set_camera_position()
            if self.keyMap["right"]:
                self.camera_target_offset[1] += f[3]
                self.set_camera_position()
        if self.keyMap["space"]:
            self.camera_target_offset[0] = 0
            self.camera_target_offset[1] = 0
            self.set_camera_position()
        if self.cooldown["camera rotation"] == 0:
            if self.keyMap["e"]:
                self.shift_camera_rotation_index('Right')
                self.set_camera_position()
                self.cooldown["camera rotation"] = 100
            if self.keyMap["q"]:
                self.shift_camera_rotation_index('Left')
                self.set_camera_position()
                self.cooldown["camera rotation"] = 100
        if self.cooldown["cursor movement"] == 0:
            if self.keyMap['w']:
                self.face_this_towards('North')
                self.move_this_towards('North')
            if self.keyMap['s']:
                self.face_this_towards('South')
                self.move_this_towards('South')
            if self.keyMap['d']:
                self.face_this_towards('East')
                self.move_this_towards('East')
            if self.keyMap['a']:
                self.face_this_towards('West')
                self.move_this_towards('West')
        if self.keyMap['f']:
            self.gm_add_tile()
        if self.keyMap['page up']:
            if self.zoom_level < 10:
                self.set_zoom(.2)
        if self.keyMap['page down']:
            if self.zoom_level > 3:
                self.set_zoom(-.2)
        for i in self.cooldown:
            if self.cooldown[i] >= 1:
                self.cooldown[i] -= 1
        return task.cont


tkinter_window = GameWindow()
tkinter_window.run()
