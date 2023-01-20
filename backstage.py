from epiproto import *


class Theatre:
    def __init__(self, cam=None, loader=None):
        self.model_library = {
            'Beings': {},
            'Tiles': {}}
        self.loader = loader
        self.hidden_buffer = NodePath()
        self.the_stage = LocationMap()
        self.the_cast = {'GM': GmPointer()}
        self.the_star = 'GM'
        self.gm_mode = True
        self.the_cameraman = CameraMan(
            cam=cam, look_at=self.the_cast[self.the_star])
        self.the_lighting = AmbientLight('Base Light')
        self.the_lighting.setColor((0.7, 0.7, 0.7, 1))
        self.lighting = render.attachNewNode(self.the_lighting)
        render.setLight(self.lighting)
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
        self.instantiate_tiles()
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
            self.place_instance(self.the_cast['GM'].core, chunk, 'Beings')

    def get_tile_types(self):
        if self.loader:
            model_list = self.the_stage.terrain_model_list
            for i in model_list:
                filename = "Catalog/Terrain/"+i+'.gltf'
                self.model_library['Tiles'][i] = self.loader.loadModel(filename)
                self.model_library['Tiles'][i].reparentTo(self.hidden_buffer)

    def instantiate_tiles(self):
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
