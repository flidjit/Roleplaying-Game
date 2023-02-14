from varlib import *
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
from toolbag import *


class Player:
    def __init__(self):
        self.name = 'Player'
        self.handle = None
        self.email = 'ThisGuy@righthere.com'
        self.gm_mode = False
        self.my_campaigns = []
        self.my_characters = {}
        self.ui_colors = default_ui_colors
        self.ui_icons = default_ui_icons
        self.key_config = default_keyboard_bindings
        self.key_map = {}
        self.control_mode = 'gm Standard'


class Thing3D:
    def __init__(self, x=0, y=0, z=0, thing_id='Pointer',
                 model_id=None, facing='North', tags=None):
        self.thing_id = thing_id
        if model_id:
            self.model_id = model_id
        else:
            self.model_id = 'basicfloor'
        self.facing = facing
        self.map_loc = [x, y, z]
        self.chunk_family = None
        self.instance = None
        self.base_ts = None
        self.add_ts = None
        if tags:
            self.tags = tags
        else:
            self.tags = []


class GridTile(Thing3D):
    def __init__(self, x=0, y=0, z=0, thing_id='0,0',
                 is_floor=False, occupied_by=None):
        Thing3D.__init__(self, x=x, y=y, z=z, thing_id=thing_id,
                         model_id='basicfloor')
        self.is_floor = is_floor
        self.floor_height = 0
        self.occupied_by = occupied_by


class MapChunk:
    def __init__(self, chunk_id='Chunk 1', display_name='Starting Area',
                 description='The place to start your game',
                 tiles=None, mobs=None,
                 active=True, minimap_color=None):
        self.chunk_id = chunk_id
        self.instance = None
        self.display_name = display_name
        self.description = description
        if tiles:
            self.tiles = tiles
        else:
            self.tiles = {}
        if mobs:
            self.mobs = mobs
        else:
            self.mobs = {}
        self.active = active
        if minimap_color:
            self.minimap_color = minimap_color
        else:
            self.minimap_color = ['green', 'green1']


class LocationMap:
    def __init__(self, map_id='Menu',
                 terrain_model_list=None,
                 tile_texture_list=None,
                 tile_atlas=default_tile_atlas,
                 chunks=None):
        self.map_id = map_id
        self.tile_atlas = tile_atlas
        if tile_texture_list:
            self.tile_texture_list = tile_texture_list
        else:
            self.tile_texture_list = []
        if terrain_model_list:
            self.terrain_model_list = terrain_model_list
        else:
            self.terrain_model_list = []
        if chunks:
            self.chunks = chunks
        else:
            self.chunks = {'Chunk 1': MapChunk(tiles={'0,0': GridTile(0, 0, 0)})}
