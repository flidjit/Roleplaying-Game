from proto import *


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
class Mob:
    def __init__(self, owner_name='gm'):
        self.core = Thing3D()
        self.owner_name = ''
        self.character = None
        self.owner_name = owner_name
        self.traveling = False
        self.traveling_to = [0, 0]

    def update(self):
        self.first_task()
        if self.traveling:
            ml = self.core.map_loc
            tt = self.traveling_to
            if ml[0] < tt[0]:
                self.core.map_loc[0] = round(self.core.map_loc[0]+.05, 2)
            elif ml[0] > tt[0]:
                self.core.map_loc[0] = round(self.core.map_loc[0]-.05, 2)
            if ml[1] < tt[1]:
                self.core.map_loc[1] = round(self.core.map_loc[1]+.05, 2)
            elif ml[1] > tt[1]:
                self.core.map_loc[1] = round(self.core.map_loc[1]-.05, 2)
            if ml[0] == tt[0] and ml[1] == tt[1]:
                self.traveling = False
                self.core.map_loc[0] = int(self.core.map_loc[0])
                self.core.map_loc[1] = int(self.core.map_loc[1])
                self.core.map_loc[2] = int(self.core.map_loc[2])
            ml = self.core.map_loc
            self.core.instance.setPos(ml[0], ml[1], ml[2])
        self.final_task()

    def walk_me(self, direction=None, the_map=None):
        if direction:
            self.core.facing = direction
        t_id = self.get_tile_id(self.get_new_location())
        if t_id in the_map.tile_atlas:
            if not self.traveling:
                of = map_dirs[self.core.facing]["position"]
                self.traveling_to[0] = self.core.map_loc[0] + of[0]
                self.traveling_to[1] = self.core.map_loc[1] + of[1]
                self.traveling = True

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

    def first_task(self):
        pass

    def final_task(self):
        pass


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
class GmPointer(Mob):
    def __init__(self):
        Mob.__init__(self)
        self.edit_chunk = MapChunk()
        self.target = Thing3D()
        self.core.model_id = 'GM'
        self.tile_placer = None
        self.tile_placer_active = True

    def add_new_tile(self, theatre=None):
        if self.tile_placer_active:
            t_loc = self.get_new_location()
            t_id = self.get_tile_id(t_loc)
            tiles = self.edit_chunk.tiles
            x = t_loc[0]
            y = t_loc[1]
            z = self.core.map_loc[2]
            if t_id not in tiles:
                tiles[t_id] = GridTile(x=x, y=y, z=z, thing_id=t_id)
                ta = theatre.the_stage.tile_atlas
                ta[t_id] = self.edit_chunk.chunk_id
                print(str(t_id)+' added to atlas')
                theatre.place_instance(tiles[t_id], ta[t_id])

    def first_task(self):
        if self.traveling:
            if self.tile_placer_active:
                self.tile_placer_active = False

    def final_task(self):
        if not self.traveling:
            if not self.tile_placer_active:
                self.tile_placer_active = True


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
        self.cam.lookAt(self.look_at.core.instance)

    def follow(self):
        if self.look_at:
            f_l = [0, 0, 10]
            f_l[0] = self.map_location[0] + self.look_at.core.map_loc[0]
            f_l[1] = self.map_location[1] + self.look_at.core.map_loc[1]
            self.cam.setPos(f_l[0], f_l[1], f_l[2])
            self.focus()

    def rotate(self, spin='Clockwise'):
        if not self.look_at.traveling:
            self.traveling = True
            self.shift_rotation_index(spin)
            o_s = cam_dirs[self.facing]["position"]
            la_m = self.look_at.core.map_loc
            self.traveling_to[0] = la_m[0] + o_s[0]
            self.traveling_to[1] = la_m[1] + o_s[1]
            self.traveling_to[2] = la_m[2] + self.view_angle

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
