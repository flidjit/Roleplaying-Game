import tkinter as tk
from tkinter import ttk


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
        self.verb_tab = VerbTab(self)
        self.verb_tab.grid()
        self.add(self.verb_tab, text='Verbs')


class CharacterTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        print('The character tab')


class MiniMap(tk.Canvas):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black', height=300, width=300)
        print('a minimap')


class MapTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        self.minimap = MiniMap(self)
        self.minimap.place(x=25, y=25)
        print('The character tab')


class VerbTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        print('The character tab')


class EquipmentTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        print('The character tab')
