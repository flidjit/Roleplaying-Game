import tkinter as tk
from tkinter import ttk
from varlib import default_ui_colors


class Compendium(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.config(bg='black')
        self.cast_btn = tk.Button(
            self, bg='black', fg='green', width=10, text='Cast')
        self.cast_btn.grid(column=0, row=0, sticky='we')
        self.beastiary_btn = tk.Button(
            self, bg='black', fg='green', width=10, text='Beastiary')
        self.beastiary_btn.grid(column=1, row=0, sticky='we')
        self.maps_btn = tk.Button(
            self, bg='black', fg='green', width=10, text='Geography')
        self.maps_btn.grid(column=2, row=0, sticky='we')
        self.timeline_btn = tk.Button(
            self, bg='black', fg='green', width=10, text='Timeline')
        self.timeline_btn.grid(column=3, row=0, sticky='we')
        self.lore_btn = tk.Button(
            self, bg='black', fg='green', width=10, text='Lore')
        self.lore_btn.grid(column=0, row=1, sticky='we')
        self.gallery_btn = tk.Button(
            self, bg='black', fg='green', width=10, text='Gallery')
        self.gallery_btn.grid(column=1, row=1, sticky='we')
        self.notes_btn = tk.Button(
            self, bg='black', fg='green', width=10, text='Notes')
        self.notes_btn.grid(column=2, row=1, sticky='we')
        self.grid(sticky='we')


class WorldTab(tk.Frame):
    def __init__(self, master=None,
                 colors=default_ui_colors):
        super().__init__(master=master)
        self.config(bg=colors['WorldTab - BG'])
        self.campaign_arc_name_lbl = tk.Label(
            self, justify=tk.LEFT,
            text="[Campaign Name]: [Arc Name]",
            bg='black', fg='light blue',
            font=("Times", 15, "bold"))
        self.campaign_arc_name_lbl.place(x=5, y=5)
        self.gm_name_lbl = tk.Label(
            self, justify=tk.LEFT,
            text="GM: [GM Name]",
            bg='black', fg='light blue',
            font=("Times", 12, "bold"))
        self.gm_name_lbl.place(x=5, y=27)
        self.date_lbl = tk.Label(
            self, justify=tk.LEFT,
            text="5:00AM - Monday - 91st day of Spring - 2023AD",
            bg='black', fg='light blue',
            font=("Times", 10, "bold"))
        self.date_lbl.place(x=5, y=74)
        self.weather_lbl = tk.Label(
            self, justify=tk.LEFT,
            text="75°F - Partly Cloudy - Humidity: Low - Wind: 5mph N",
            bg='black', fg='light blue',
            font=("Times", 10, "bold"))
        self.weather_lbl.place(x=5, y=94)
        self.compendium = Compendium(self)
        self.compendium.place(x=0, y=145, width=450, height=75)
        self.campaign_stats_lbl = tk.Label(
            self, justify=tk.LEFT,
            text="Session: 1 - Hours Played: 0.00 - Combat Encounters: 0"
                 "\n XP Gains: 0 - In-Game Time Played: 2years & 10days"
                 "\n Technology Level: 2 - Fantasy Level: 1",
            bg='black', fg='light blue',
            font=("Times", 10, "bold"))
        self.campaign_stats_lbl.place(x=5, y=245)
