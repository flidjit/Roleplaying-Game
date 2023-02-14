import toolbag
from uiwin import *


# ToDo:
#   * Bug: Camera rotation is weird.
#   * Bug: DeBug is broken. (Ironic)
#   * Swaps tile instances
#   * Minimap Works
#   * Saves/Loads Maps
#   * Has at least 2 sets of tiles.
#   * Has a button to pause/start all game activity.
#   * Mob has AI during update.
#   * Has Turn-based system, passes control to players or AI.
#   * Has an activity mode, where control is paused except a
#       continue button, and a series of actions take place,
#       to create cut-scenes, and conversations.

# Control States:
#   1) the player is in combat but cannot move or take an action
#       but can look at stats, roll dice, use the chat, etc.
#   2) the player is in combat and can move with a measurement tool
#       and take actions as well as the other stuff.
#   3) the player is not in combat and can move around the map freely.
#   4) the player is not in combat and can not move without permission.
#   5) a cut-scene is taking place, and nobody can do anything. In
#       single-player mode, the player has access to the enter
#       button to progress events, but in multiplayer, the gm
#       has a more in-depth control over activities. Also in
#       multiplayer mode, the players can still click ok,
#       but progress does not take place until all players or the
#       gm have done so.
#   6) gm powers are turned on. the gm cursor replaces the controlled
#       character, and states can be turned on and off at will.

# The game starts up and...
#   If this is the first time the player is loading the program,
# they will see a prompt welcoming them, and asking
# for their name and email address. Then maybe you get to pick
# some options like your colors and icons, and gm cursor.
#   Next you are spawned into a room with a large computer, and we are
# greeted by a guide. The guide tells you a little-bit about the game
# and then tells you how to move, at which point he tells you to follow
# and leaves the room.
#   The player eventually follows the guide into the next room, which
# is much smaller, and tells the player how to edit maps. The player
# is given some time to edit this room, which will be considered
# something like a 'bed-room' for the player. This is where you
# will spawn when the game loads up from now on.
#   You leave the room eventually, and the guide now takes you over
# to the single-player mode area and tells you how to play.
#   After this sequence is over the guide goes to the multi-player
# area and waits for the player to make their way over to there before
# the tutorial continues.
#   The player starts out controlling a non-descript model, but
# once a single player character is created, that is the model
# that the player will walk around the options house.
#   Single-player mode is a tactical strategy rpg, where the player
# controls a hand-full of characters.
#   Multiplayer mode is a campaign-builder when GM powers are turned on,
# and anyone can play with making a campaign. A player cannot load up
# a campaign without a gm to host it, but they can view campaign notes
# and party character sheets. THE END.


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
        self.base_build()
        self.debugging = True
        self.configure_keys()
        self.theatre = Theatre(self.cam, self.loader)  # !*!
        self.updateTask = taskMgr.add(self.update, "update")
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        print(self.get_local_info())
        self.theatre.build_stage()

    def base_build(self):
        props = WindowProperties()
        props.setParentWindow(self.image_frame.winfo_id())
        props.setOrigin(0, 0)
        props.setSize(800, 400)
        self.win = base.makeDefaultPipe()
        base.openDefaultWindow(props=props)
        base.setBackgroundColor(0.007, 0, 0.007, 1)

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
            t.the_cast[star].walk_me(m_dir, t.the_stage)
        # -----------------------------------
        if k['Move Selected Right']:
            m_dir = cam_dirs[c_dir]["Right"]
            t.the_cast[star].walk_me(m_dir, t.the_stage)
        # -----------------------------------
        if k['Move Selected Up']:
            m_dir = cam_dirs[c_dir]["Down"]
            t.the_cast[star].walk_me(m_dir, t.the_stage)
        # -----------------------------------
        if k['Move Selected Down']:
            m_dir = cam_dirs[c_dir]["Up"]
            t.the_cast[star].walk_me(m_dir, t.the_stage)
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

    @staticmethod
    def get_local_info():
        text_ = os.name+' - '+platform.machine()+'\n'
        text_ += base.win.gsg.driver_renderer+'\n'
        text_ += platform.system()+' ('+platform.release()+')\n'
        text_ += 'Texture limit: '+str(base.win.getGsg().getMaxTextureStages())+'\n'
        return text_


testing = AoaWindow()
testing.run()
