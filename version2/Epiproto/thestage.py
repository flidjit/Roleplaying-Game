from panda3d.core import NodePath
from direct.showbase.ShowBase import ShowBase


class Tile:
    def __init__(self, model_path, position, render):
        self.model_path = model_path
        self.position = position
        self.node_path = None
        self.render = render
        self.load_model()

    def load_model(self):
        # Check if a model path is provided
        if self.model_path:
            # Load the 3D model with the option to flatten
            self.node_path = self.render.attach_new_node(f'Tile_{id(self)}')
            model = self.render.loader.load_model(self.model_path)
            model.reparent_to(self.node_path)

            # Set the initial position
            self.node_path.set_pos(self.position)

    def get_node_path(self):
        return self.node_path


class Occupant:
    def __init__(self, model_path, position, render):
        self.model_path = model_path
        self.position = position
        self.node_path = None
        self.render = render
        self.load_model()

    def load_model(self):
        # Check if a model path is provided
        if self.model_path:
            # Load the 3D model with the option to flatten
            self.node_path = self.render.attach_new_node(f'Occupant_{id(self)}')
            model = self.render.loader.load_model(self.model_path)
            model.reparent_to(self.node_path)

            # Set the initial position
            self.node_path.set_pos(self.position)

    def get_node_path(self):
        return self.node_path


class Chunk:
    def __init__(self, map_data):
        self.tiles = {}
        self.occupants = {}
        self.load_from_map_data(map_data)

    def load_from_map_data(self, map_data):
        for tile_data in map_data.get('tiles', []):
            tile = Tile(model_path=tile_data.get('model_path'), position=tile_data.get('position'), render=base.render)
            self.tiles[tile_data.get('id')] = tile

        for occupant_data in map_data.get('occupants', []):
            occupant = Occupant(model_path=occupant_data.get('model_path'), position=occupant_data.get('position'), render=base.render)
            self.occupants[occupant_data.get('id')] = occupant


class Stage:
    def __init__(self, base):
        self.base = base
        self.chunks = {}  # Dictionary to store chunks

    def load_tile_model(self, tile):
        # Load the 3D model and apply texture to create a NodePath
        model = self.base.loader.load_model(tile.model_path)
        texture = self.base.loader.load_texture(tile.texture_path)
        model.set_texture(texture)

        # Set the position of the model based on the tile's position
        model.set_pos(tile.position[0], tile.position[1], tile.height)

        # Attach the model to the render node
        tile.node_path = NodePath(model)
        tile.node_path.reparent_to(self.base.render)

    def load_occupant_model(self, occupant):
        # Load the 3D model for the occupant
        model = self.base.loader.load_model(occupant.model_path)

        # Set the position of the model based on the occupant's position
        model.set_pos(occupant.position[0], occupant.position[1], 0)

        # Attach the model to the render node
        occupant.node_path = NodePath(model)
        occupant.node_path.reparent_to(self.base.render)

    def unload_model(self, node_path):
        # Remove the node and release associated resources
        if node_path:
            node_path.remove_node()

    def add_tile(self, chunk_id, tile_id, tile):
        # Add a new tile to the specified chunk
        if chunk_id not in self.chunks:
            self.chunks[chunk_id] = Chunk()

        self.chunks[chunk_id].tiles[tile_id] = tile
        self.load_tile_model(tile)

    def add_occupant(self, chunk_id, occupant_id, occupant):
        # Add a new occupant to the specified chunk
        if chunk_id not in self.chunks:
            self.chunks[chunk_id] = Chunk()

        self.chunks[chunk_id].occupants[occupant_id] = occupant
        self.load_occupant_model(occupant)

    def edit_tile(self, chunk_id, tile_id, new_tile):
        # Edit an existing tile in the specified chunk
        if chunk_id in self.chunks and tile_id in self.chunks[chunk_id].tiles:
            # Remove the old tile
            old_tile = self.chunks[chunk_id].tiles[tile_id]
            self.unload_model(old_tile.node_path)

            # Add the new tile
            self.chunks[chunk_id].tiles[tile_id] = new_tile
            self.load_tile_model(new_tile)

    def delete_tile(self, chunk_id, tile_id):
        # Delete an existing tile from the specified chunk
        if chunk_id in self.chunks and tile_id in self.chunks[chunk_id].tiles:
            tile = self.chunks[chunk_id].tiles[tile_id]
            self.unload_model(tile.node_path)
            del self.chunks[chunk_id].tiles[tile_id]

    def delete_occupant(self, chunk_id, occupant_id):
        # Delete an existing occupant from the specified chunk
        if chunk_id in self.chunks and occupant_id in self.chunks[chunk_id].occupants:
            occupant = self.chunks[chunk_id].occupants[occupant_id]
            self.unload_model(occupant.node_path)
            del self.chunks[chunk_id].occupants[occupant_id]

    def update(self):
        # Perform any necessary updates in the stage
        pass
