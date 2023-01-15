import platform
import os
import uiwin
import tkinter as tk
from tkinter import ttk
from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from direct.actor.Actor import Actor
from panda3d.core import WindowProperties, OrthographicLens, NodePath, AmbientLight, TextureStage, Vec3, LPoint3f
from pandac.PandaModules import TransparencyAttrib, TexGenAttrib
import simplepbr
import proto
from toolbag import *
import varlib


class CameraMan:
    def __init__(self, master=None, cam=None, looking_at=None):
        self.zoom_factor = 7
        self.cam = cam
        self.looking_at = looking_at
        self.offset = [0, 0]
        self.cm_location = [10, 10]
        self.cm_moving_to = [-10, 10]
        self.dir_id = "North-West"
        self.rotating = False
        self.view_angle = 7.5
        self.lens = OrthographicLens()
        self.change_zoom()

    def update(self):
        here_ = self.cm_location
        there_ = self.cm_moving_to
        if self.rotating:
            if here_[0] > there_[0]:
                here_[0] -= 1
            if here_[0] < there_[0]:
                here_[0] += 1
            if here_[1] > there_[1]:
                here_[1] -= 1
            if here_[1] < there_[1]:
                here_[1] += 1
            self.cam.setPos(here_[0], here_[1], self.view_angle)
            self.cam.lookAt(self.looking_at.instance)
        if here_ == there_:
            self.rotating = False

    def set_camera_position(self):
        if self.looking_at:
            x = self.cm_location[0]+self.offset[0]+self.looking_at.draw_at[0]
            y = self.cm_location[1]+self.offset[1]+self.looking_at.draw_at[1]
            self.cam.setPos(x, y, self.view_angle)

    def shift_offset(self, ckd=None):
        if ckd:
            d = varlib.directions[ckd]
            self.offset[0] += d[0]/10
            self.offset[1] += d[1]/10
            self.set_camera_position()

    def start_rotation(self, cko=None):
        self.rotating = True
        self.offset = [0, 0]
        t = self.looking_at.instance.getPos()
        self.cm_moving_to[0] = t[0]+cko[0]
        self.cm_moving_to[1] = t[1]+cko[1]
        self.dir_id = cko[2]

    def change_zoom(self, change=-1.0):
        z = self.zoom_factor
        self.zoom_factor += change
        z = self.zoom_factor
        self.lens.setFilmSize(2 * z, 1 * z)


class Pointer(proto.Thing3D):
    def __init__(self):
        proto.Thing3D.__init__(self)
        self.target = proto.Thing3D()
        self.selected = {
            'Chunk': 'Chunk 1',
            'This Tile': [0, 0],
            'That Tile': [0, 0]}

    def update(self):
        if self.moving:
            d = self.draw_at
            m = self.moving_to
            if d[0] < m[0]:
                d[0] += .1
            if d[0] > m[0]:
                d[0] -= .1
            if d[1] < m[1]:
                d[1] += .1
            if d[1] > m[1]:
                d[1] -= .1
            d[0] = round(d[0], 2)
            d[1] = round(d[1], 2)
            self.instance.setPos(d[0], d[1], d[2])
            if d[0] == m[0] and d[1] == m[1]:
                d[0] = int(d[0])
                d[1] = int(d[1])
                self.moving = False
                self.get_selected()

    def get_selected(self):
        f = varlib.directions[self.facing]
        this_ = self.selected['This Tile']
        that_ = self.selected['That Tile']
        this_[0] = self.draw_at[0]
        this_[1] = self.draw_at[1]
        that_[0] = self.draw_at[0]+f[0]
        that_[1] = self.draw_at[1]+f[1]

    def start_move(self, the_stage=None, ckd=None):
        self.get_selected()
        tiles_ = the_stage.chunks[self.selected['Chunk']].tiles
        if self.moving is False:
            if ckd:
                r = varlib.directions[ckd][2]
                self.instance.setH(r)
                self.facing = ckd
                self.get_selected()
                if self.tile_naming() in tiles_:
                    self.target.instance.hide()
                    self.moving = True
                    self.moving_to[0] = self.selected["That Tile"][0]
                    self.moving_to[1] = self.selected["That Tile"][1]
                else:
                    self.target.instance.show()

    def tile_naming(self, name_what='That Tile'):
        t_name = str(int(self.selected[name_what][0]))+','
        t_name += str(int(self.selected[name_what][1]))
        return t_name


class Theatre:
    def __init__(self, master=None):
        self.model_lib = {
            'Beings': {},
            'Tiles': {}}
        self.model_buffer = NodePath()
        self.the_stage = proto.LocationMap()
        self.pointer = Pointer()
        self.default_light = AmbientLight('Base Light')
        self.default_light.setColor((0.7, 0.7, 0.7, 1))
        self.lighting = render.attachNewNode(self.default_light)
        render.setLight(self.lighting)

    def update(self):
        self.pointer.update()

    def build_stage(self, aoa_window=None):
        self.add_chunk_nodes()
        self.add_tile_models_to_buffer(aoa_window)
        self.instance_tiles()
        self.add_pointer_model(aoa_window)
        self.pointer.get_selected()

    def add_pointer_model(self, aoa_window=None):
        fn = 'catalog/terrain/basic/pointer.gltf'
        self.model_lib['Beings']['Pointer'] = aoa_window.loader.loadModel(fn)
        self.model_lib['Beings']['Pointer'].reparentTo(self.model_buffer)
        self.pointer.instance = render.attachNewNode('Chunk 1')
        self.model_lib['Beings']['Pointer'].instanceTo(self.pointer.instance)
        self.pointer.instance.setTransparency(TransparencyAttrib.MAlpha)
        self.pointer.instance.setH(render, 180)
        fn = 'catalog/terrain/basic/pointer_target.gltf'
        self.model_lib['Beings']['Target'] = aoa_window.loader.loadModel(fn)
        self.model_lib['Beings']['Target'].reparentTo(self.model_buffer)
        self.pointer.target.instance = render.attachNewNode('Chunk 1')
        self.model_lib['Beings']['Target'].instanceTo(self.pointer.target.instance)
        self.pointer.target.instance.reparentTo(self.pointer.instance)
        self.pointer.target.instance.setTransparency(TransparencyAttrib.MAlpha)
        self.pointer.target.instance.setH(render, 180)

    def add_chunk_nodes(self):
        for i in self.the_stage.chunks:
            c = self.the_stage.chunks[i]
            c.instance = render.attachNewNode(c.chunk_id)

    def add_tile_models_to_buffer(self, aoa_window=None):
        m_list = self.the_stage.terrain_model_list
        for i in m_list:
            filename = "catalog/terrain/"+i+'.gltf'
            self.model_lib['Tiles'][i] = aoa_window.loader.loadModel(filename)
            self.model_lib['Tiles'][i].reparentTo(self.model_buffer)

    def instance_tiles(self):
        chunks = self.the_stage.chunks
        for c in chunks:
            for t in chunks[c].tiles:
                tile = chunks[c].tiles[t]
                group = chunks[c].chunk_id
                self.set_instance(tile, group)

    def new_tile(self, pointer=None):
        if pointer:
            if self.pointer.tile_naming() not in self.the_stage.tiles_at:
                if self.pointer.moving is False:
                    print('making a tile')
                    tn = self.pointer.tile_naming()
                    print('tile ('+tn+') Was Created')
                    t = self.the_stage.chunks[pointer.selected['Chunk']].tiles
                    tile = proto.GridTile(thing_id=tn)
                    st = pointer.selected['That Tile']
                    tile.draw_at = [st[0], st[1], 0]
                    t[tn] = tile
                    self.the_stage.tiles_at[tn] = pointer.selected['Chunk']
                    self.set_instance(t[tn], pointer.selected['Chunk'])

    def set_instance(self, thing_3d=None, render_group=None, library='Tiles'):
        thing_3d.instance = render.attachNewNode(render_group)
        self.model_lib[library][thing_3d.model_filename].instanceTo(thing_3d.instance)
        loc = thing_3d.draw_at
        thing_3d.instance.setPos(loc[0], loc[1], loc[2])
