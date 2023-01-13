import toolbag
import varlib
from backstage import *


class AoaWindow(ShowBase):
    def __init__(self):
        ShowBase.__init__(self, windowType='none')
        self.startTk()
        self.root = self.tkRoot
        self.root['bg'] = '#240e28'
        self.root.geometry("1210x620")
        self.root.resizable(False, False)
        self.image_frame = uiwin.ViewPort(self.root)  # !*!
        self.chat_output = uiwin.ChatSection(self.root)  # !*!
        self.text_input = uiwin.InputSection(self.root)  # !*!
        self.tab_frame = uiwin.TabSection(self.root)  # !*!
        self.root.update()
        props = WindowProperties()
        props.setParentWindow(self.image_frame.winfo_id())
        props.setOrigin(0, 0)
        props.setSize(800, 400)
        self.win = base.makeDefaultPipe()
        base.openDefaultWindow(props=props)
        base.setBackgroundColor(0.007, 0, 0.007, 1)
        self.you = proto.Player()  # !*!
        self.configure_keys()
        self.theatre = Theatre(self)  # !*!
        self.camera_man = CameraMan(self, self.cam)  # !*!
        self.cool_downs = {
            "Map Info": 0}
        self.cam.node().setLens(self.camera_man.lens)
        simplepbr.init()
        self.ttk_style = ttk.Style()
        Director.style_this(self.you.ui_colors, self)
        self.updateTask = taskMgr.add(self.update, "update")
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        print(os.name+' - '+platform.machine())
        print(base.win.gsg.driver_renderer)
        print(platform.system()+' ('+platform.release()+')')

        self.theatre.build_stage(self)
        self.camera_man.looking_at = self.theatre.the_stage.chunks['Chunk 1'].tiles['0,0'].instance
        self.cam.lookAt(self.camera_man.looking_at)

    def update_key_map(self, control_name, control_state):
        self.you.key_map[control_name] = control_state

    def configure_keys(self):
        k = self.you.key_config
        for i in range(len(k)):
            self.you.key_map[k[i][1]] = False
            self.accept(k[i][0], self.update_key_map, [k[i][1], True])
            self.accept(k[i][0]+'-up', self.update_key_map, [k[i][1], False])

    def update(self, task):
        self.root.update()
        self.camera_man.update()
        self.theatre.pointer.update()
        if self.you.control_mode == 'GM Standard':
            self.keyboard_input_gm_standard()
        for i in self.cool_downs:
            if self.cool_downs[i] > 0:
                self.cool_downs[i] -= 1
        return task.cont

    def keyboard_input_gm_standard(self):
        d = varlib.directions
        cko = varlib.cam_keyboard_offsets["Cam "+self.camera_man.dir_id]
        for i in d["Button Directions"]:
            key = 'Move Camera '+i
            ckd = cko[i]
            if self.you.key_map[key]:
                self.camera_man.shift_offset(ckd)
        for i in d["Button Directions"]:
            key = 'Move Selected '+i
            ckd = cko[i]
            if self.you.key_map[key]:
                self.theatre.pointer.start_move(self.theatre.the_stage, ckd)
        if not self.camera_man.rotating:
            if self.you.key_map["Rotate Camera Clockwise"]:
                self.camera_man.start_rotation(cko["Clockwise"])
            if self.you.key_map["Rotate Camera Counter-Clockwise"]:
                self.camera_man.start_rotation(cko["Counter-Clockwise"])
        if self.you.key_map["Print Map Info"]:
            if self.cool_downs['Map Info'] == 0:
                txt = toolbag.GetInfo.draw_map_info(self.you, self.theatre)
                self.chat_output.insert('end', txt+'\n')
                self.cool_downs['Map Info'] = 100


testing = AoaWindow()
testing.run()
