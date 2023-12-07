import tkinter as tk
from tkinter import ttk
from varlib import default_ui_colors
from refactor.proto import MapData

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
        self.location_label = tk.Label(
            self, justify=tk.LEFT,
            bg=colors['MapTab - BG'],
            fg=colors['MapTab - Text'])
        self.location_label.place(x=25, y=5)
        self.minimap = MiniMap(self, colors)
        self.minimap.place(x=25, y=25)
        self.xy_label = tk.Label(
            self, justify=tk.LEFT,
            bg=colors['MapTab - BG'],
            fg=colors['MapTab - Text'])
        self.xy_label.place(x=25, y=327)
        self.texid_lbl = tk.Label(
            self, justify=tk.LEFT, text='Tile Texture:',
            bg='black', fg='white')
        self.texid_lbl.place(x=20, y=350)
        self.texture_id_box = ttk.Combobox(self)
        self.texture_id_box['state'] = 'readonly'
        self.texture_id_box.place(x=120, y=350, width=200, height=20)
        self.new_texture_button = tk.Button(
            self, text='Add Texture', bg='black', fg='white')
        self.new_texture_button.place(x=120, y=380, width=200, height=20)
        self.initialize_minimap()
        self.set_location_text()

    def set_location_text(
            self, txt_1='Location: ', txt_2='Vector:'):
        self.location_label['text'] = txt_1
        self.xy_label['text'] = txt_2

    def initialize_minimap(self, map_data=None):
        map_data = map_data or MapData()
        for i in map_data.chunks:
            for j in map_data.chunks[i].tiles:
                tile = map_data.chunks[i].tiles[j]
                x, y = tile.map_loc
                t_id = f"{x},{y}"
                c = map_data.chunks[i].minimap_color
                self.minimap.add_square(x, y, t_id, c)

