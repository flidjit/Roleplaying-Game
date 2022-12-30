import tkinter

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties


class Tkinter_window(ShowBase):
    def __init__(self):
        ShowBase.__init__(self, windowType='none')
        self.startTk()

        self.frame = self.tkRoot
        self.image_frame = tkinter.Frame(self.frame, width=800, height=400)
        self.image_frame.grid()
        self.text = tkinter.Text(self.frame, height=5)
        self.text.grid(sticky='we')
        self.frame.update()

        props = WindowProperties()
        props.setParentWindow(self.image_frame.winfo_id())
        props.setOrigin(0, 0)
        props.setSize(800, 400)

        self.win = base.makeDefaultPipe()
        base.openDefaultWindow(props=props)

        scene = self.loader.loadModel("environment")
        scene.reparentTo(render)


tkinter_window = Tkinter_window()
tkinter_window.run()