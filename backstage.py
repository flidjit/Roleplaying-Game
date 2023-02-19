from epiproto import *


class Theatre:
    def __init__(self, cam=None, loader=None):
        self.model_library = {
            'Beings': {},
            'Tiles': {}}
        self.texture_library = {}
        self.loader = loader
        self.hidden_buffer = NodePath()
        self.the_stage = LocationMap()
        self.the_cast = {'GM': GmPointer()}
        self.the_star = 'GM'
        self.the_cameraman = CameraMan(
            cam=cam, look_at=self.the_cast[self.the_star])
        self.gm_mode = True
        self.timers = {"Map Info": 0,
                       "Rotate Cam": 0}

    def update(self):
        for i in self.the_cast:
            self.the_cast[i].update()
        self.the_cameraman.update()
        self.count_down()

    def count_down(self):
        for i in self.timers:
            if self.timers[i] > 0:
                self.timers[i] -= 1

    def build_stage(self):
        self.add_chunk_nodes()
        self.get_tile_types()
        self.instantiate_stage()
        self.add_gm()

    def add_chunk_nodes(self):
        for i in self.the_stage.chunks:
            c = self.the_stage.chunks[i]
            c.instance = render.attachNewNode(c.chunk_id)

    def add_gm(self, chunk='Chunk 1'):
        if self.loader:
            filename = "Catalog/Objects/gm_selector.gltf"
            self.model_library["Beings"]["GM"] = self.loader.loadModel(filename)
            self.model_library["Beings"]["GM"].reparentTo(self.hidden_buffer)
            self.place_instance(self.the_cast['GM'].thing_base, chunk, 'Beings')

    def get_tile_types(self):
        filename = "Catalog/Terrain/basicfloor.bam"
        self.model_library['Tiles']['basicfloor'] = self.loader.loadModel(filename)
        self.model_library['Tiles']['basicfloor'].reparentTo(self.hidden_buffer)
        if self.loader:
            model_list = self.the_stage.terrain_model_list
            for i in model_list:
                filename = "Catalog/Terrain/special/"+i+'.bam'
                self.model_library['Tiles'][i] = self.loader.loadModel(filename)
                self.model_library['Tiles'][i].reparentTo(self.hidden_buffer)

    def get_textures_(self):
        texture_list = self.the_stage.tile_texture_list
        if self.loader:
            for i in texture_list:
                filename = "Catalog/Terrain/tiletex/"+i+'.png'
                self.texture_library[i] = self.loader.loadTexture(filename)

    def instantiate_stage(self):
        chunks = self.the_stage.chunks
        for c in chunks:
            for t in chunks[c].tiles:
                tile = chunks[c].tiles[t]
                group = chunks[c].chunk_id
                self.place_instance(tile, group)

    def place_instance(self, thing_3d=None, render_group='Chunk 1',
                       library='Tiles'):
        thing_3d.instance = render.attachNewNode(render_group)
        self.model_library[library][thing_3d.model_id].instanceTo(thing_3d.instance)
        loc = thing_3d.map_loc
        thing_3d.instance.setPos(loc[0], loc[1], loc[2])

    def change_texture(self, thing_3d=None, tex_name=None):
        if thing_3d:
            if tex_name:
                ts = thing_3d.instance.findTextureStage(tex_name)
                thing_3d.instance.setTexture(ts, self.texture_library[tex_name], 1)
