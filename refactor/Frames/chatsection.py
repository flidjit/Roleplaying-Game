import tkinter as tk


class ChatSection(tk.Frame):
    def __init__(self, master=None, aoa_window=None):
        tk.Frame.__init__(self, master=master)
        self.aoa_window = aoa_window

