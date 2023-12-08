import tkinter as tk
from tkinter import ttk
import importlib

from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import WindowProperties

from theplayer import PlayerData, ThePlayer
from thestage import TheStage
from thechat import ChatSection
from startmenu import StartMenu


style = ttk.Style()
style.theme_use('alt')
style.configure(
    'Treeview.Heading', background='black', foreground='white',
    highlightthickness=0, borderwidth=0)
style.configure(
    'Treeview', fieldbackground='black', foreground='green')
style.configure(
    'TNotebook.Tab', background='lime green', padding=0)
style.configure(
    'TNotebook', background='#2C2331', boarderwidth=0)


class AoaWindow(ShowBase):
    def __init__(self):
        ShowBase.__init__(self, windowType='none')

        # Initialize Tkinter
        self.startTk()
        self.ttk_style = style
        self.root = self.tkRoot
        self.root['bg'] = 'black'
        self.root.geometry("1280x620")
        self.root.resizable(False, False)
        # Show start menu and load game data
        self.the_player = ThePlayer(self)
        self.the_player = StartMenu(self.root, self.the_player).show()
        self.the_stage = TheStage(self)
        self.the_system = None
        # Initialize window components
        self.chat_section = ChatSection(self.root, self)
        self.viewport = tk.Frame(self.root, bg='red')
        self.tab_section = tk.Frame(self.root, bg='green')
        # load the_system and tab_section.
        self.load_rpsystem()
        # place the widgets on the form.
        self.chat_section.place(x=10, y=440, width=800, height=140)
        self.tab_section.place(x=820, y=10, width=450, height=600)
        self.viewport.place(x=10, y=10, width=800, height=400)
        self.initialize_window()
        # Set up task manager
        self.updateTask = taskMgr.add(self.update, "update")

    def initialize_window(self):
        # Initialize window properties
        props = WindowProperties()
        self.root.update()
        props.setParentWindow(self.viewport.winfo_id())
        props.setOrigin(0, 0)
        props.setSize(800, 400)
        # Open Panda3D window with specified properties
        self.openDefaultWindow(props=props)
        # Set background color
        self.setBackgroundColor(0.007, 0, 0.007, 1)

    def load_rpsystem(self):
        imp = "RPS."+self.the_player.current_rps
        thesystem = importlib.import_module(imp+".thesystem")
        self.the_system = thesystem.TheSystem()

    def update(self, task):
        # Update components
        self.root.update()
        self.the_player.update()
        self.the_system.update()
        self.the_stage.update()
        return task.cont


this = AoaWindow()
this.root.mainloop()
