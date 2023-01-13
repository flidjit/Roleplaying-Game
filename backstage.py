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
import protorefactor as proto
from toolbag import *
import varlib



class CameraMan:
    def __init__(self, master=None, cam=None, looking_at=None):
        self.zoom_factor = 6
        self.cam = cam
        self.looking_at = looking_at
        self.offset = [0, 0]
        self.cm_location = [10, 10]
        self.cm_moving_to = [-10, 10]
        self.dir_id = "North-West"
        self.there_target = proto.Thing3D()
        self.rotating = False
        self.view_angle = 7.5
        self.lens = OrthographicLens()
        self.change_zoom()
        self.set_camera_position()

    def update(self):
        if self.rotating:
            if self.cm_location[0] > self.cm_moving_to[0]:
                self.cm_location[0] -= 1
            if self.cm_location[0] < self.cm_moving_to[0]:
                self.cm_location[0] += 1
            if self.cm_location[1] > self.cm_moving_to[1]:
                self.cm_location[1] -= 1
            if self.cm_location[1] < self.cm_moving_to[1]:
                self.cm_location[1] += 1
            self.cam.setPos(self.cm_location[0], self.cm_location[1], self.view_angle)
            self.cam.lookAt(self.looking_at)
        if self.cm_location == self.cm_moving_to:
            self.rotating = False

    def set_camera_position(self):
        x = self.cm_location[0]+self.offset[0]
        y = self.cm_location[1]+self.offset[1]
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
        t = self.looking_at.getPos()
        self.cm_moving_to[0] = t[0]+cko[0]
        self.cm_moving_to[1] = t[1]+cko[1]
        self.dir_id = cko[2]

    def change_zoom(self, change=-1.0):
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
        if self.moving[0]:
            if self.draw_at[0] < self.moving[1][0]:
                self.draw_at[0] += 0.1
            if self.draw_at[0] > self.moving[1][0]:
                self.draw_at[0] -= 0.1
            if self.draw_at[1] < self.moving[1][1]:
                self.draw_at[1] += 0.1
            if self.draw_at[1] > self.moving[1][1]:
                self.draw_at[1] -= 0.1
        loc = self.draw_at
        self.instance.setPos(loc[0], loc[1], loc[2])

    def get_selected(self):
        f = varlib.directions[self.facing]
        self.selected['This Tile'][0] = self.draw_at[0]
        self.selected['This Tile'][1] = self.draw_at[1]
        self.selected['That Tile'][0] = self.draw_at[0]+f[0]
        self.selected['That Tile'][1] = self.draw_at[1]+f[1]
        print(self.selected['That Tile'])

    def start_move(self, the_stage=None, ckd=None):
        self.get_selected()
        if ckd:
            print(ckd)
            r = varlib.directions[ckd][2]
            self.instance.setH(r)
            self.facing = ckd


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

    def build_stage(self, aoa_window=None):
        self.add_chunk_nodes()
        self.add_tile_models_to_buffer(aoa_window)
        self.instance_tiles()
        self.add_pointer_model(aoa_window)
        self.pointer.get_selected()

    def add_pointer_model(self, aoa_window=None):
        m_list = self.the_stage.terrain_model_list
        self.model_lib['Beings']['Pointer'] = aoa_window.loader.loadModel(m_list['Pointer'])
        self.model_lib['Beings']['Pointer'].reparentTo(self.model_buffer)
        self.pointer.instance = render.attachNewNode('Chunk 1')
        self.model_lib['Beings']['Pointer'].instanceTo(self.pointer.instance)
        self.pointer.instance.setTransparency(TransparencyAttrib.MAlpha)
        self.pointer.instance.setH(render, 180)
        self.model_lib['Beings']['Target'] = aoa_window.loader.loadModel(m_list['Target'])
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
            self.model_lib['Tiles'][i] = aoa_window.loader.loadModel(m_list[i])
            self.model_lib['Tiles'][i].reparentTo(self.model_buffer)

    def instance_tiles(self):
        chunks = self.the_stage.chunks
        for c in chunks:
            for t in chunks[c].tiles:
                tile = chunks[c].tiles[t]
                group = chunks[c].chunk_id
                tid = tile.name
                tile.instance = render.attachNewNode(group)
                self.model_lib['Tiles'][tid].instanceTo(tile.instance)
                loc = tile.draw_at
                tile.instance.setPos(loc[0], loc[1], loc[2])

