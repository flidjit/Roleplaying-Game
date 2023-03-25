from backstage import *
from rp_frames import *


# ToDo: * Add Entity markers on the minimap.
#       * Switch between viewing local and regional on the minimap.

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


class ViewPort(tk.Frame):
    def __init__(self, master=None,
                 colors=default_ui_colors):
        super().__init__(master=master)
        self.config(bg=colors['Viewport BG'])
        self.place(x=0, y=0, width=800, height=400)


class ChatSection(tk.Text):
    def __init__(self, master=None,
                 colors=default_ui_colors):
        super().__init__(master=master, state=tk.DISABLED,
                         highlightthickness=0, borderwidth=0)
        self.config(bg=colors['ChatSection - BG'])
        self.config(fg=colors['ChatSection - FG'])
        self.scroll_bar = tk.Scrollbar(self)
        self.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.yview)
        self.scroll_bar.place(x=790, y=0, width=8, height=130)
        self.place(x=0, y=440, width=800, height=133)

    def say_in_chat(self, user_name='Bob', emote='says',
                    text='hello!'):
        self["state"] = tk.NORMAL
        self.insert('end', '    '+user_name+' '+emote+' : '+text+'\n')
        self.see(tk.END)
        self["state"] = tk.DISABLED


class InputSection(tk.Entry):
    def __init__(self, master=None,
                 colors=default_ui_colors):
        super().__init__(master=master, highlightthickness=0)
        self.config(bg=colors['InputSection - BG'])
        self.config(fg=colors['InputSection - FG'])
        self.place(x=0, y=580, width=800, height=20)


class TabSection(ttk.Notebook):
    def __init__(self, master=None,
                 colors=default_ui_colors,
                 icons=default_ui_icons):
        super().__init__(master=master, width=450, height=600)
        self.map_tab_icon = tk.PhotoImage(file=icons['Map'])
        self.map_tab = MapTab(self, colors)
        self.map_tab.grid()
        self.add(self.map_tab, image=self.map_tab_icon)
        self.sheet_tab_icon = tk.PhotoImage(file=icons['Sheet'])
        self.sheet_tab = CSheet1(self)
        self.sheet_tab.grid()
        self.add(self.sheet_tab, image=self.sheet_tab_icon)
        self.prop_tab_icon = tk.PhotoImage(file=icons['Props'])
        self.prop_tab = PropTab(self, colors)
        self.prop_tab.grid()
        self.add(self.prop_tab, image=self.prop_tab_icon)
        self.party_tab_icon = tk.PhotoImage(file=icons['Party'])
        self.party_tab = PartyTab(self, colors)
        self.party_tab.grid()
        self.add(self.party_tab, image=self.party_tab_icon)
        self.action_tab_icon = tk.PhotoImage(file=icons['Actions'])
        self.action_tab = ActionTab(self, colors)
        self.action_tab.grid()
        self.add(self.action_tab, image=self.action_tab_icon)
        self.world_tab_icon = tk.PhotoImage(file=icons['World'])
        self.world_tab = WorldTab(self, colors)
        self.world_tab.grid()
        self.add(self.world_tab, image=self.world_tab_icon)
        self.help_tab_icon = tk.PhotoImage(file=icons['Help'])
        self.help_tab = HelpTab(self, colors)
        self.help_tab.grid()
        self.add(self.help_tab, image=self.help_tab_icon)
        self.place(x=807, y=0)


class MiniMap(tk.Canvas):
    def __init__(self, master=None,
                 colors=default_ui_colors):
        super().__init__(master=master, height=300, width=300,
                         highlightthickness=0)
        self.config(bg=colors['MiniMap - BG'])
        self.map_squares = {}
        self.view_offset = [145, 145]

    def add_square(self, x=0, y=0, square_id='0,0',
                   color=('green', 'blue')):
        vo = self.view_offset
        self.map_squares[square_id] = self.create_rectangle(
            x*10+vo[0], -y*10+vo[1], x*10+10+vo[0], -y*10+10+vo[1],
            fill=color[0], outline=color[1])


class MapTab(tk.Frame):
    def __init__(self, master=None,
                 colors=default_ui_colors):
        super().__init__(master=master)
        self.config(bg=colors['MapTab - BG'])
        self.location_label = tk.Label(self, justify=tk.LEFT)
        self.location_label.config(bg=colors['MapTab - BG'])
        self.location_label.config(bg=colors['MapTab - Text'])
        self.location_label.place(x=25, y=5)
        self.minimap = MiniMap(self, colors)
        self.minimap.place(x=25, y=25)
        self.xy_label = tk.Label(self, justify=tk.LEFT)
        self.xy_label.config(bg=colors['MapTab - BG'])
        self.xy_label.config(fg=colors['MapTab - Text'])
        self.xy_label.place(x=25, y=327)
        self.texid_lbl = tk.Label(self, justify=tk.LEFT, text='Tile Texture:')
        self.texid_lbl.config(bg='black')
        self.texid_lbl.config(fg='white')
        self.texid_lbl.place(x=20, y=350)
        self.texture_id_box = ttk.Combobox(self)
        self.texture_id_box['state'] = 'readonly'
        self.texture_id_box.place(x=120, y=350, width=200, height=20)
        self.new_texture_button = tk.Button(
            self, text='Add Texture', bg='black', fg='white')
        self.new_texture_button.place(x=120, y=380, width=200, height=20)
        self.initialize_minimap()
        self.set_location_text()

    def set_location_text(self, txt_1='Location: ',
                          txt_2='Vector:'):
        self.location_label['text'] = txt_1
        self.xy_label['text'] = txt_2

    def initialize_minimap(self, loc=LocationMap()):
        for i in loc.chunks:
            for j in loc.chunks[i].tiles:
                tile = loc.chunks[i].tiles[j]
                x = tile.map_loc[0]
                y = tile.map_loc[1]
                t_id = str(x)+','+str(y)
                c = loc.chunks[i].minimap_color
                self.minimap.add_square(x, y, t_id, c)


class PropTab(tk.Frame):
    def __init__(self, master=None,
                 colors=default_ui_colors):
        super().__init__(master=master)
        self.config(bg=colors['PropTab - BG'])


class PartyTab(tk.Frame):
    def __init__(self, master=None,
                 colors=default_ui_colors):
        super().__init__(master=master)
        self.config(bg=colors['PartyTab - BG'])


class ActionTab(tk.Frame):
    def __init__(self, master=None,
                 colors=default_ui_colors):
        super().__init__(master=master)
        self.config(bg=colors['ActionTab - BG'])


class WorldTab(tk.Frame):
    def __init__(self, master=None,
                 colors=default_ui_colors):
        super().__init__(master=master)
        self.config(bg=colors['WorldTab - BG'])


class HelpTab(tk.Frame):
    def __init__(self, master=None,
                 colors=default_ui_colors):
        super().__init__(master=master)
        self.config(bg=colors['HelpTab - BG'])
