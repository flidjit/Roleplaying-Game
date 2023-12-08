import tkinter as tk


class ChatSection(tk.Frame):
    def __init__(self, master=None, aoa_window=None):
        super().__init__(master)
        self.aoa_window = aoa_window
        self.bg = 'black'

