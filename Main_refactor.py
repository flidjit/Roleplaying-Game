from epiproto_refactor import *
from uielements_refactor import *

from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import WindowProperties


class AoaWindow(ShowBase):
    def __init__(self):
        ShowBase.__init__(self, windowType='none')
        self.root = None
        self.initialize_()
        self.updateTask = taskMgr.add(self.update, "update")

        self.tab_section = TabSection(root, self)
        self.chat_section = ChatSection(root, self)
        self.viewport = ViewPort(root, self)

        self.the_player = ThePlayer(self)
        self.the_stage = TheStage()
        self.the_cameraman = TheCameraman()

    def initialize_(self):
        self.startTk()
        self.root = self.tkRoot
        self.root['bg'] = 'black'
        self.root.geometry("1210x620")
        self.root.resizable(False, False)
        props = WindowProperties()
        props.setParentWindow(self.viewport.winfo_id())
        props.setOrigin(0, 0)
        props.setSize(800, 400)
        self.win = base.makeDefaultPipe()
        base.openDefaultWindow(props=props)
        base.setBackgroundColor(0.007, 0, 0.007, 1)

    def update(self, task):
        self.root.update()
        self.the_player.update(self)
        self.the_stage.update(self)
        self.the_cameraman.update(self)
        return task.count
