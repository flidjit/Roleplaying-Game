import tkinter as tk
from tkinter import ttk

from Epiproto.theplayer import ThePlayer, PlayerData
import importlib as il


class StartMenu(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        self.geometry("900x600")
        self.title("MetaLink")
        self.resizable(width=False, height=False)

        self.bg_image = tk.PhotoImage(file="bg1.png")
        self.splash_canvas = tk.Canvas(
            self, bg='black', width=900, height=600,
            highlightthickness=0, borderwidth=0)
        self.splash_canvas.place(x=0, y=0)
        self.draw_background()

        self.button_1 = None
        self.button_2 = None
        self.back_button = None
        self.item_list = None
        self.selected_item = None
        self.universes = ['AOA']
        self.universe_combobox = None
        self.selected_universe = None
        self.add_mode_buttons()
        # noinspection PyUnresolvedReferences
        self.universe_combobox.current(0)
        # noinspection PyUnresolvedReferences
        self.universe_combobox.update()

        self.grid()

        self.player = ThePlayer()

    def draw_background(self):
        self.splash_canvas.create_image(
            0, 0, image=self.bg_image, anchor='nw')
        self.splash_canvas.create_text(
            10, 10, text='- MetaLink -', fill='black',
            font=('Currier', 50), anchor='nw')
        self.splash_canvas.create_text(
            6, 6, text='- MetaLink -', fill='red',
            font=('Currier', 50), anchor='nw')

    def add_mode_buttons(self):
        universe_list = tk.StringVar()
        self.universe_combobox = ttk.Combobox(
            self, font=('Courier', 15),
            textvariable=universe_list)
        self.universe_combobox['values'] = self.universes
        self.universe_combobox.current(0)
        self.universe_combobox.update()
        self.universe_combobox.place(
            x=500, y=400, width=200)
        self.button_1 = tk.Button(
            self, bg='black', fg='green',
            font=('Courier', 25),
            text='PC', width=15,
            command=self.pc_mode_selected)
        self.button_1.place(x=500, y=450)
        self.button_2 = tk.Button(
            self, bg='black', fg='green',
            font=('Courier', 25),
            text='GM', width=15,
            command=self.gm_mode_selected)
        self.button_2.place(x=500, y=520)

    def add_pc_operation_buttons(self):
        self.button_1 = tk.Button(
            self, bg='black', fg='green',
            font=('Currier', 25),
            text='New Character', width=15)
        self.button_1.place(x=500, y=450)
        self.button_2 = tk.Button(
            self, bg='black', fg='green',
            font=('Currier', 25),
            text='Load Character', width=15)
        self.button_2.place(x=500, y=520)
        self.back_button = tk.Button(
            self, bg='black', fg='purple',
            font=('Currier', 10),
            text=' << Back ', width=10,
            command=self.back_button_selected)
        self.back_button.place(x=500, y=400)
        self.item_list = tk.Listbox(
            self, fg="yellow", bg="grey",
            font=("Helvetica", 12))
        self.item_list.place(
            x=50, y=400, height=200, width=400)

    def add_gm_operation_buttons(self):
        self.button_1 = tk.Button(
            self, bg='black', fg='green',
            font=('Currier', 25),
            text='New Campaign', width=15)
        self.button_1.place(x=500, y=450)
        self.button_2 = tk.Button(
            self, bg='black', fg='green',
            font=('Currier', 25),
            text='Load Campaign', width=15)
        self.button_2.place(x=500, y=520)
        self.back_button = tk.Button(
            self, bg='black', fg='purple',
            font=('Currier', 10),
            text=' << Back ', width=10,
            command=self.back_button_selected)
        self.back_button.place(x=500, y=400)
        self.item_list = tk.Listbox(
            self, fg="yellow", bg="grey",
            font=("Helvetica", 12))
        self.item_list.place(
            x=50, y=400, height=200, width=400)

    def new_campaign_selected(self):
        print('New Campaign!')

    def pc_mode_selected(self):
        self.player.is_gm = False
        self.selected_universe = self.universe_combobox.get()
        self.universe_combobox.destroy()
        self.button_1.destroy()
        self.button_2.destroy()
        self.add_pc_operation_buttons()

    def gm_mode_selected(self):
        self.player.is_gm = True
        self.selected_universe = self.universe_combobox.get()
        self.universe_combobox.destroy()
        self.button_1.destroy()
        self.button_2.destroy()
        self.add_gm_operation_buttons()

    def back_button_selected(self):
        self.button_1.destroy()
        self.button_2.destroy()
        self.back_button.destroy()
        self.item_list.destroy()
        self.add_mode_buttons()
        self.universe_combobox.current(0)
        self.universe_combobox.update()

    def show(self):
        self.wait_window()
        return self.player
