from proto import *


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
class Mob:
    def __init__(self, owner_name='gm'):
        self.core = Thing3D()
        self.owner_name = ''
        self.character = None
        self.owner_name = owner_name
        self.moving = False
        self.move_offset = []

    def update(self):
        if self.moving:
            if self.move_tick < 10:
                f = self.core.facing
                m_o = map_dirs[self.core.facing]["Position"]
                loc = self.core.map_loc
                x = loc[0]+t*m_o[f][0]/10
                y = loc[1]+t*m_o[f][1]/10
                z = 0
                self.core.instance.setPos(x, y, z)
                self.move_tick += 1
            else:
                self.moving = False
                self.move_tick = 1
                self.core.map_loc = self.get_new_location()
                self.core.instance.setPos(
                    self.core.map_loc[0],
                    self.core.map_loc[1],
                    self.core.map_loc[2])

    def walk_me(self, direction=None):
        if direction:
            self.core.facing = direction
        self.moving = True

    def get_new_location(self):
        d = map_dirs[self.core.facing]["position"]
        x = self.core.map_loc[0]+d[0]
        y = self.core.map_loc[1]+d[1]
        return [x, y]

    @staticmethod
    def get_tile_id(tile_location=None):
        x = tile_location[0]
        y = tile_location[1]
        t_name = str(x) + ',' + str(y)
        return t_name


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
class GmPointer(Mob):
    def __init__(self):
        Mob.__init__(self)
        self.edit_chunk = MapChunk()
        self.target = Thing3D()
        self.core.model_id = 'GM'

    def add_new_tile(self, theatre=None):
        t_loc = self.get_new_location()
        t_id = self.get_tile_id(t_loc)
        tiles = self.edit_chunk.tiles
        x = t_loc[0]
        y = t_loc[1]
        z = self.core.map_loc[2]
        if t_id not in tiles:
            tiles[t_id] = GridTile(x=x, y=y, z=z, thing_id=t_id)
        theatre.place_instance(tiles[t_id], self.edit_chunk.chunk_id)


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
class CameraMan:
    def __init__(self, cam=None, look_at=None):
        self.cam = cam
        self.lens = OrthographicLens()
        self.cam.node().setLens(self.lens)
        self.look_at = look_at
        self.rot_id = 0
        self.facing = "North-West"
        t = cam_dirs[self.facing]['position']
        self.map_location = [t[0], t[1], 10]
        self.traveling = False
        self.traveling_to = [0, 0, 0]
        self.zoom_factor = 33
        self.view_angle = 10
        self.zoom_out(1)

    def update(self):
        if self.traveling:
            ml = self.map_location
            tt = self.traveling_to
            if ml[0] < tt[0]:
                self.map_location[0] += 1
            elif ml[0] > tt[0]:
                self.map_location[0] -= 1
            if ml[1] < tt[1]:
                self.map_location[1] += 1
            elif ml[1] > tt[1]:
                self.map_location[1] -= 1
            if ml[0] == tt[0] and ml[1] == tt[1]:
                self.traveling = False
        self.follow()

    def focus(self, on=None):
        if on:
            self.look_at = on
        self.cam.lookAt(self.look_at.instance)

    def follow(self):
        if self.look_at:
            f_l = self.map_location
            self.cam.setPos(f_l[0], f_l[1], f_l[2])
            self.focus()

    def rotate(self, spin='Clockwise'):
        self.traveling = True
        self.shift_rotation_index(spin)
        o_s = cam_dirs[self.facing]["position"]
        self.traveling_to[0] = self.look_at.map_loc[0] + o_s[0]
        self.traveling_to[1] = self.look_at.map_loc[1] + o_s[1]
        self.traveling_to[2] = self.look_at.map_loc[2] + self.view_angle

    def shift_rotation_index(self, spin='Clockwise'):
        if spin == 'Clockwise':
            if self.rot_id < 3:
                self.rot_id += 1
            else:
                self.rot_id = 0
        elif spin == 'Counter-Clockwise':
            if self.rot_id > 0:
                self.rot_id -= 1
            else:
                self.rot_id = 3
        self.facing = cam_dirs["Order"][self.rot_id]
        print(self.facing)

    def zoom_in(self, speed=1):
        if self.zoom_factor > 30:
            self.zoom_factor -= speed
            z = self.zoom_factor
            self.lens.setFilmSize(.2 * z, .1 * z)
        else:
            self.zoom_factor = 26

    def zoom_out(self, speed=1):
        if self.zoom_factor < 90:
            self.zoom_factor += speed
            z = self.zoom_factor
            self.lens.setFilmSize(.2 * z, .1 * z)
        else:
            self.zoom_factor = 89

    def change_angle(self, change=-1.0):
        self.view_angle += change
        self.follow()
