import tkinter as tk
from tkinter import ttk
from proto import LocationMap, helpfile


class ChatSection(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        self.chat = tk.Text(self, bg='black', fg='white', height=8, width=90, wrap='word')
        self.scroll_bar = tk.Scrollbar(self)
        self.chat.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.chat.yview)
        self.chat.grid(column=0, row=0)
        self.scroll_bar.grid(column=1, row=0, sticky='ns')
        self.say_in_chat()
        self.say_in_chat()

    def say_in_chat(self, user_name='Bob', says='hello!'):
        self.chat.insert('end', ' '+user_name+' says : '+says+'\n')


class InputSection(tk.Entry):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black', fg='green')
        print('input your text here.')


class TabSection(ttk.Notebook):
    def __init__(self, master=None):
        super().__init__(master=master, width=350, height=550)
        self.map_tab = MapTab(self)
        self.map_tab.grid()
        self.add(self.map_tab, text='Map')
        self.character_tab = CharacterTab(self)
        self.character_tab.grid()
        self.add(self.character_tab, text='Stats')
        self.equipment_tab = EquipmentTab(self)
        self.equipment_tab.grid()
        self.add(self.equipment_tab, text='Gear')
        self.help_tab = HelpTab(self)
        self.help_tab.grid()
        self.add(self.help_tab, text='Help')


class CharacterTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        print('The character tab')


class MiniMap(tk.Canvas):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black', height=300, width=300)
        self.map_squares = {}
        self.view_offset = [145, 145]

    def add_square(self, x=0, y=0, square_id='0,0', color=('green', 'red')):
        vo = self.view_offset
        self.map_squares[square_id] = self.create_rectangle(
            x*10+vo[0], -y*10+vo[1], x*10+10+vo[0], -y*10+10+vo[1], fill=color[0], outline=color[1])


class MapTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        self.location_label = tk.Label(self, bg='black', fg='pink')
        self.location_label.place(x=25, y=5)
        self.minimap = MiniMap(self)
        self.minimap.place(x=25, y=25)
        self.xy_label = tk.Label(self, bg='black', fg='pink')
        self.xy_label.place(x=25, y=327)
        self.set_location_text()
        self.initialize_minimap()

    def set_location_text(self, x=0, y=0, location_name='Here', chunk_name=''):
        txt = 'Location: '+location_name
        self.location_label['text'] = txt
        txt = '( x:'+str(x)+' , y:'+str(y)+' )   Chunk id : '+chunk_name
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
        self.set_location_text(location_name=loc.name, chunk_name=self.get_chunk_name())

    def get_chunk_name(self, loc=LocationMap(), cursor_location='0,0'):
        return loc.chunk_locations[cursor_location]

class EquipmentTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        print('The character tab')


class HelpTab(tk.Text):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black', fg='white')
        for i in helpfile:
            self.insert('end', i)
        print('The character tab')

