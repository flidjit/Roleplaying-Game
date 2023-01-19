import toolbag
from uiwin import *


# ToDo:
#   * Swaps tile instances
#   * Minimap Works
#   * Saves/Loads Maps


class AoaWindow(ShowBase):
    def __init__(self):
        ShowBase.__init__(self, windowType='none')
        self.startTk()
        self.you = Player()  # !*!
        col = self.you.ui_colors
        ico = self.you.ui_icons
        self.ttk_style = ttk.Style()
        self.root = self.tkRoot
        self.root['bg'] = col['Root BG']
        self.root.geometry("1210x620")
        self.root.resizable(False, False)
        self.image_frame = uiwin.ViewPort(self.root, col)  # !*!
        self.chat_output = uiwin.ChatSection(self.root, col)  # !*!
        self.text_input = uiwin.InputSection(self.root, col)  # !*!
        self.tab_frame = uiwin.TabSection(self.root, col, ico)  # !*!
        self.root.update()
        props = WindowProperties()
        props.setParentWindow(self.image_frame.winfo_id())
        props.setOrigin(0, 0)
        props.setSize(800, 400)
        self.win = base.makeDefaultPipe()
        base.openDefaultWindow(props=props)
        base.setBackgroundColor(0.007, 0, 0.007, 1)
        self.debugging = True
        self.configure_keys()
        self.theatre = Theatre(self.cam, self.loader)  # !*!
        simplepbr.init()
        self.updateTask = taskMgr.add(self.update, "update")
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        print(os.name+' - '+platform.machine())
        print(base.win.gsg.driver_renderer)
        print(platform.system()+' ('+platform.release()+')')

        self.theatre.build_stage()

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
        self.theatre.update()
        self.keyboard_input()
        return task.cont

    def keyboard_input(self):
        t = self.theatre
        cam_man = t.the_cameraman
        star = t.the_star
        tool = toolbag.DeBug
        k = self.you.key_map
        # -----------------------------------
        if k["Rotate Camera Clockwise"]:
            if t.timers['Rotate Cam'] == 0:
                cam_man.rotate("Clockwise")
                t.timers['Rotate Cam'] = 60
        # -----------------------------------
        if k["Rotate Camera Counter-Clockwise"]:
            if t.timers['Rotate Cam'] == 0:
                cam_man.rotate("Counter-Clockwise")
                t.timers['Rotate Cam'] = 60
        # -----------------------------------
        if k["Zoom In"]:
            cam_man.zoom_in(2)
        # -----------------------------------
        if k["Zoom Out"]:
            cam_man.zoom_out(2)
        # -----------------------------------
        c_dir = t.the_cameraman.facing
        # -----------------------------------
        if k['Move Selected Left']:
            m_dir = cam_dirs[c_dir]["Left"]
            t.the_cast[star].walk_me(m_dir)
        # -----------------------------------
        if k['Move Selected Right']:
            m_dir = cam_dirs[c_dir]["Right"]
            t.the_cast[star].walk_me(m_dir)
        # -----------------------------------
        if k['Move Selected Up']:
            m_dir = cam_dirs[c_dir]["Down"]
            t.the_cast[star].walk_me(m_dir)
        # -----------------------------------
        if k['Move Selected Down']:
            m_dir = cam_dirs[c_dir]["Up"]
            t.the_cast[star].walk_me(m_dir)
        # -----------------------------------
        if k['Add New Floor Tile']:
            if t.gm_mode:
                t.the_cast[star].add_new_tile(t)
        # -----------------------------------
        if k["Print Map Info"]:
            if self.debugging:
                if t.timers['Map Info'] == 0:
                    txt = tool.draw_map_info(self.you, self.theatre)
                    self.chat_output.say_in_chat(
                        user_name='System Core', emote='message', text='\n'+txt)
                    t.timers['Map Info'] = 100


testing = AoaWindow()
testing.run()
