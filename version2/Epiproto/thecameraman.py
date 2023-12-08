from panda3d.core import LPoint3
from direct.showbase.ShowBase import ShowBase


class Cameraman:
    def __init__(self, base: ShowBase, render_node):
        self.base = base
        self.render = render_node
        self.camera_distance = 20.0
        self.camera_pivot = self.render.attachNewNode('camera_pivot')
        self.camera_pivot.setPos(0, 0, 0)

        self.camera = base.cam
        self.camera.reparentTo(self.camera_pivot)
        self.camera.setPos(0, -self.camera_distance, 0)
        self.camera.lookAt(self.camera_pivot)

        self.key_speed = 0.5
        self.rotation_speed = 90.0
        self.zoom_speed = 2.0

        self.base.accept("arrow_left", self.move_left)
        self.base.accept("arrow_right", self.move_right)
        self.base.accept("arrow_up", self.move_forward)
        self.base.accept("arrow_down", self.move_backward)
        self.base.accept("q", self.rotate_left)
        self.base.accept("e", self.rotate_right)

        self.base.taskMgr.add(self.update_camera_task, "update_camera_task")

    def move_forward(self):
        self.camera_pivot.setY(self.camera_pivot, self.key_speed)

    def move_backward(self):
        self.camera_pivot.setY(self.camera_pivot, -self.key_speed)

    def move_left(self):
        self.camera_pivot.setX(self.camera_pivot, -self.key_speed)

    def move_right(self):
        self.camera_pivot.setX(self.camera_pivot, self.key_speed)

    def rotate_left(self):
        self.camera_pivot.setH(self.camera_pivot.getH() + self.rotation_speed)

    def rotate_right(self):
        self.camera_pivot.setH(self.camera_pivot.getH() - self.rotation_speed)

    def center_on_object(self, object_pos: LPoint3):
        self.camera_pivot.setPos(object_pos.getX(), object_pos.getY(), 0)

    def zoom_in(self):
        self.camera_distance = max(self.camera_distance - self.zoom_speed, 1.0)
        self.camera.setPos(0, -self.camera_distance, 0)

    def zoom_out(self):
        self.camera_distance += self.zoom_speed
        self.camera.setPos(0, -self.camera_distance, 0)

    def update_camera_task(self, task):
        return task.cont