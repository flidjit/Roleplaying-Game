from epiproto import *
from Epiproto.theplayer import PlayerData
from Frames.viewport import *
from Frames.chatsection import *
from Frames.tabsection import *
from startup import *
import platform
import os

from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import WindowProperties


class AoaWindow(ShowBase):
    def __init__(self):
        ShowBase.__init__(self, windowType='none')

        # Initialize Tkinter
        self.startTk()
        self.root = self.tkRoot
        self.root['bg'] = 'black'
        self.root.geometry("1210x620")
        self.root.resizable(False, False)

        # Show start menu and load game
        self.the_player = StartMenu(self.root).show()
        self.load_game()

        # Initialize components
        self.tab_section = TabSection(self.root, self)
        self.chat_section = ChatSection(self.root, self)
        self.viewport = ViewPort(self.root, self)

        # Initialize Panda3D components
        self.the_stage = TheStage()
        self.the_cameraman = TheCameraman()

        # Set up task manager
        self.updateTask = taskMgr.add(self.update, "update")

    def initialize_window(self):
        # Initialize window properties
        props = WindowProperties()
        props.setParentWindow(self.viewport.winfo_id())
        props.setOrigin(0, 0)
        props.setSize(800, 400)
        base.openDefaultWindow(props=props)
        base.setBackgroundColor(0.007, 0, 0.007, 1)

    def load_game(self):
        print('Game loaded')  # Replace with actual game loading logic

    def update(self, task):
        # Update components
        self.root.update()
        self.the_player.update(self)
        self.the_stage.update(self)
        self.the_cameraman.update(self)
        return Task.cont


this = AoaWindow()
this.run()
