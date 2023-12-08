import tkinter as tk
from tkinter import ttk


class CampaignData:
    def __init__(self):
        self.universe = 'AOA'
        self.name = 'Default Campaign'
        self.gm_name = 'GM'
        self.invited_players = ['player1']
        self.description = 'An example'
        self.technology_level = 0
        self.fantasy_level = 0


class CampaignCreator(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master, bg='black')
        self.geometry("300x300")
        self.title('New Campaign')
        self.resizable(width=False, height=False)

