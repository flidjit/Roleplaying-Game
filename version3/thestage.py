from panda3d.core import NodePath, TextureStage
from direct.showbase.ShowBase import ShowBase


class ModelDat:
    def __init__(self, model_path, render, x, y, z):
        self.model_path = model_path
        self.x = x
        self.y = y
        self.z = z
        self.node_path = None
        self.render = render


class Tile(ModelDat):
    def __init__(self, model_path, render, x, y, z, occupant=None):
        super().__init__(model_path, render, x, y, z)
        self.occupant = occupant


class Being(ModelDat):
    def __init__(self, model_path, render, x, y, z, character=None):
        super().__init__(model_path, render, x, y, z)
        self.character = character


class Chunk:
    def __init__(self, map_data):
        self.chunk_id = '1'
        b = Being(None, None, 1, 1, 1, None)
        t1 = Tile(None, None, 1, 1, 1, b)
        t2 = Tile(None, None, 1, 2, 1, None)
        self.tiles = {'1, 1': t1, '1, 2': t2}  # Added another tile for demonstration


class MapData:
    def __init__(self):
        self.name = 'Default Map'
        self.chunks = {}


class TheStage:
    def __init__(self, aoa_window=None):
        self.aoa_window = aoa_window
        self.map_data = MapData()
        self.models = {}
        self.textures = {}

    def load_model(self, tile=None, being=None):
        """
        Load a model based on the provided Tile or Being.

        Parameters:
        - tile (Tile): The Tile object representing the model to be loaded.
        - being (Being): The Being object representing the model to be loaded.
        """
        if tile:
            model_path = tile.model_path
            position = (tile.x, tile.y, tile.z)
        elif being:
            model_path = being.model_path
            position = (being.x, being.y, being.z)
        else:
            # Either tile or being should be provided
            return

        # Check if the model has been loaded before
        if model_path not in self.models:
            # Load the model using the loader
            model = self.aoa_window.loader.load_model(model_path)

            # Check if the model was loaded successfully
            if not model:
                print(f"Failed to load model: {model_path}")
                return

            # Create a NodePath for the model and set its position
            node_path = NodePath(model)
            node_path.set_pos(*position)

            # Reparent the NodePath to the render node
            node_path.reparent_to(self.aoa_window.render)

            # Store the loaded model in the dictionary for later reference
            self.models[model_path] = node_path

    def load_texture(self, model, texture_path):
        # Check if the texture has already been loaded
        if texture_path in self.textures:
            texture = self.textures[texture_path]
        else:
            # Load the texture using the loader from aoa_window
            texture = self.aoa_window.loader.load_texture(texture_path)

            # Check if the texture was loaded successfully
            if not texture:
                print(f"Failed to load texture: {texture_path}")
                return

            # Store the loaded texture in the dictionary for later reference
            self.textures[texture_path] = texture

        # Create a TextureStage to apply the texture
        texture_stage = TextureStage("texture_stage")
        model.set_texture(texture_stage, texture)

    def load_stage(self, map_data):
        # Iterate through the chunks in the map data
        for chunk_id, chunk_data in map_data.get('chunks', {}).items():
            # Create a new chunk
            new_chunk = Chunk(map_data=chunk_data)

            # Iterate through the tiles in the chunk
            for tile_id, tile_data in chunk_data.get('tiles', {}).items():
                x, y, z = tile_data.get('position', (0, 0, 0))
                model_path = tile_data.get('model_path', '')

                # Add a new tile to the chunk
                self.add_tile(chunk_id, x, y, z, model_path)

            # Iterate through the occupants in the chunk
            for occupant_id, occupant_data in chunk_data.get('occupants', {}).items():
                x, y, z = occupant_data.get('position', (0, 0, 0))
                model_path = occupant_data.get('model_path', '')

                # Add a new occupant to the chunk
                self.add_occupant(chunk_id, occupant_id, x, y, z, model_path)

    def unload_model(self, node_path):
        """
        Unload a model represented by the provided NodePath.

        Parameters:
        - node_path (NodePath): The NodePath representing the model to be unloaded.
        """
        if not node_path:
            return

        # Detach the NodePath from the scene graph
        node_path.detach_node()

        # Remove the model from the dictionary if it was loaded
        for model_path, loaded_node_path in list(self.models.items()):
            if loaded_node_path == node_path:
                del self.models[model_path]

        # Release the resources associated with the NodePath
        node_path.remove_node()

    def add_tile(self, chunk_id, x, y, z, model_path):
        """
        Add a new tile to the specified chunk.

        Parameters:
        - chunk_id (str): The ID of the chunk where the tile will be added.
        - x (float): The x-coordinate of the tile's position.
        - y (float): The y-coordinate of the tile's position.
        - z (float): The z-coordinate of the tile's position.
        - model_path (str): The file path to the 3D model for the tile.
        """
        # Check if the chunk exists in the dictionary
        if chunk_id not in self.map_data.chunks:
            self.map_data.chunks[chunk_id] = Chunk(map_data={})

        # Create a new Tile object
        new_tile = Tile(
            model_path=model_path, render=self.aoa_window.render,
            x=x, y=y, z=z)

        # Add the tile to the chunk
        tile_id = (x, y)
        self.map_data.chunks[chunk_id].tiles[tile_id] = new_tile

        # Load the model associated with the tile
        self.load_model(tile=new_tile)

    def add_occupant(self, chunk_id, occupant_id,
                     x, y, z, model_path):
        """
        Add a new occupant to the specified chunk.

        Parameters:
        - chunk_id (str): The ID of the chunk where the occupant will be added.
        - occupant_id (str): The ID of the occupant.
        - x (float): The x-coordinate of the occupant's position.
        - y (float): The y-coordinate of the occupant's position.
        - z (float): The z-coordinate of the occupant's position.
        - model_path (str): The file path to the 3D model for the occupant.
        """
        # Check if the chunk exists in the dictionary
        if chunk_id not in self.map_data.chunks:
            self.map_data.chunks[chunk_id] = Chunk(map_data={})

        # Create a new Being object
        new_occupant = Being(model_path=model_path,
                             render=self.aoa_window.render,
                             x=x, y=y, z=z)

        # Add the occupant to the chunk
        occupant_id = occupant_id
        self.map_data.chunks[chunk_id].occupants[occupant_id] = new_occupant

        # Load the model associated with the occupant
        self.load_model(being=new_occupant)

    def delete_tile(self, chunk_id, tile_id):
        """
        Delete an existing tile from the specified chunk.

        Parameters:
        - chunk_id (str): The ID of the chunk where the tile exists.
        - tile_id (tuple): The ID of the tile (e.g., (x, y)).
        """
        # Check if the chunk exists in the dictionary
        if chunk_id in self.map_data.chunks and tile_id in self.map_data.chunks[chunk_id].tiles:
            # Get the tile from the chunk
            tile = self.map_data.chunks[chunk_id].tiles[tile_id]

            # Unload the model associated with the tile
            self.unload_model(tile.node_path)

            # Remove the tile from the chunk
            del self.map_data.chunks[chunk_id].tiles[tile_id]

    def delete_occupant(self, chunk_id, occupant_id):
        """
        Delete an existing occupant from the specified chunk.

        Parameters:
        - chunk_id (str): The ID of the chunk where the occupant exists.
        - occupant_id (str): The ID of the occupant.
        """
        # Check if the chunk exists in the dictionary
        if chunk_id in self.map_data.chunks and occupant_id in self.map_data.chunks[chunk_id].occupants:
            # Get the occupant from the chunk
            occupant = self.map_data.chunks[chunk_id].occupants[occupant_id]

            # Unload the model associated with the occupant
            self.unload_model(occupant.node_path)

            # Remove the occupant from the chunk
            del self.map_data.chunks[chunk_id].occupants[occupant_id]

    def update(self):
        # Perform any necessary updates in the stage
        pass

