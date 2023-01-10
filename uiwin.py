import tkinter as tk
from tkinter import ttk
from proto import LocationMap, help_file


# ToDo: * Add Entity markers on the minimap.
#       * Switch between viewing local and regional on the minimap.


class ChatSection(tk.Text):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black', fg='#25a9f0',
                         highlightthickness=0, borderwidth=0)
        self.scroll_bar = tk.Scrollbar(self)
        self.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.yview)
        self.scroll_bar.place(x=790, y=0, width=8, height=130)
        self.say_in_chat()

    def say_in_chat(self, user_name='Bob', says='hello!'):
        self.insert('end', ' '+user_name+' says : '+says+'\n')


class InputSection(tk.Entry):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black', fg='green', highlightthickness=0)
        print('input your text here.')


class TabSection(ttk.Notebook):
    def __init__(self, master=None):
        super().__init__(master=master, width=350, height=546)
        self.map_tab_icon = tk.PhotoImage(file='Images/maptabicon.png')
        self.map_tab = MapTab(self)
        self.map_tab.grid()
        self.add(self.map_tab, image=self.map_tab_icon)
        self.sheet_tab_icon = tk.PhotoImage(file='Images/stattabicon.png')
        self.sheet_tab = SheetTab(self)
        self.sheet_tab.grid()
        self.add(self.sheet_tab, image=self.sheet_tab_icon)
        self.prop_tab_icon = tk.PhotoImage(file='Images/proptabicon.png')
        self.prop_tab = PropTab(self)
        self.prop_tab.grid()
        self.add(self.prop_tab, image=self.prop_tab_icon)
        self.party_tab_icon = tk.PhotoImage(file='Images/grouptabicon.png')
        self.party_tab = PartyTab(self)
        self.party_tab.grid()
        self.add(self.party_tab, image=self.party_tab_icon)
        self.action_tab_icon = tk.PhotoImage(file='Images/actiontabicon.png')
        self.action_tab = ActionTab(self)
        self.action_tab.grid()
        self.add(self.action_tab, image=self.action_tab_icon)
        self.world_tab_icon = tk.PhotoImage(file='Images/worldtabicon.png')
        self.world_tab = WorldTab(self)
        self.world_tab.grid()
        self.add(self.world_tab, image=self.world_tab_icon)
        self.help_tab_icon = tk.PhotoImage(file='Images/helptabicon.png')
        self.help_tab = HelpTab(self)
        self.help_tab.grid()
        self.add(self.help_tab, image=self.help_tab_icon)


class SheetTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        print('The character tab')


class MiniMap(tk.Canvas):
    def __init__(self, master=None):
        super().__init__(master=master, bg='#0c090d', height=300, width=300,
                         highlightthickness=0)
        self.map_squares = {}
        self.view_offset = [145, 145]

    def add_square(self, x=0, y=0, square_id='0,0', color=('green', 'blue')):
        vo = self.view_offset
        self.map_squares[square_id] = self.create_rectangle(
            x*10+vo[0], -y*10+vo[1], x*10+10+vo[0], -y*10+10+vo[1],
            fill=color[0], outline=color[1])


class MapTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        self.location_label = tk.Label(self, bg='black', fg='#c96c9a')
        self.location_label.place(x=25, y=5)
        self.minimap = MiniMap(self)
        self.minimap.place(x=25, y=25)
        self.xy_label = tk.Label(self, bg='black', fg='#c96c9a')
        self.xy_label.place(x=25, y=327)
        self.initialize_minimap()
        self.set_location_text()

    def set_location_text(self, x=0, y=0, location_name='Here', current_chunk_name='Chunk 1'):
        txt = 'Location: '+location_name
        self.location_label['text'] = txt
        txt = '( x:'+str(x)+' , y:'+str(y)+' )   Chunk id : '+current_chunk_name
        self.xy_label['text'] = txt

    def initialize_minimap(self, loc=LocationMap()):
        for i in loc.chunks:
            for j in loc.chunks[i].tiles:
                tile = loc.chunks[i].tiles[j]
                x = tile.draw_at[0]
                y = tile.draw_at[1]
                t_id = str(x)+','+str(y)
                c = loc.chunks[i].minimap_color
                self.minimap.add_square(x, y, t_id, c)


class PropTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        print('The prop tab')


class PartyTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        print('The party tab')


class ActionTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        print('The acton tab')


class WorldTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        print('The world tab')


class HelpTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        print('The help tab')