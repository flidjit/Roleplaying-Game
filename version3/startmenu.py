import tkinter as tk
from tkinter import ttk
from theplayer import ThePlayer, PlayerData


class StartMenu(tk.Toplevel):
    def __init__(self, master=None, player=ThePlayer()):
        super().__init__(master=master, bg='black')
        self.geometry("900x600")
        self.title("MetaLink")
        self.resizable(width=False, height=False)

        self.bg_image = tk.PhotoImage(file="rec/img/bg1.png")
        self.splash_canvas = tk.Canvas(
            self, bg='black', width=900, height=600,
            highlightthickness=0, borderwidth=0)
        self.splash_canvas.place(x=0, y=0)
        self.draw_background()

        self.button_1 = None
        self.button_2 = None
        self.universes = ['AOARP']
        self.universe_combobox = None
        self.add_mode_buttons()
        # noinspection PyUnresolvedReferences
        self.universe_combobox.current(0)
        # noinspection PyUnresolvedReferences
        self.universe_combobox.update()

        self.grid()

        self.player = ThePlayer()
        self.new_player_check()
        self.load_player_data()

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
            text='PC Mode', width=15,
            command=self.pc_mode_selected)
        self.button_1.place(x=500, y=450)
        self.button_2 = tk.Button(
            self, bg='black', fg='green',
            font=('Courier', 25),
            text='GM Mode', width=15,
            command=self.gm_mode_selected)
        self.button_2.place(x=500, y=520)

    def pc_mode_selected(self):
        self.player.is_gm = False
        self.player.current_rps = self.universe_combobox.get()
        self.destroy()

    def gm_mode_selected(self):
        self.player.is_gm = True
        self.player.current_rps = self.universe_combobox.get()
        self.destroy()

    def load_player_data(self):
        print('load the player data')

    def new_player_check(self):
        print('if there is no player.pdat, user inputs data in a popup')

    def show(self):
        self.wait_window()
        return self.player

