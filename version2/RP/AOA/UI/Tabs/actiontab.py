import tkinter as tk
from tkinter import ttk
from varlib import default_ui_colors


class ActionTab(tk.Frame):
    def __init__(self, master=None,
                 colors=default_ui_colors):
        super().__init__(master=master)
        self.config(bg=colors['ActionTab - BG'])
        self.todo = tk.Label(
            self, justify=tk.LEFT,
            text="Available techniques and actions",
            bg='black', fg='light blue',
            font=("Times", 12, "bold"))
        self.todo.place(x=20, y=20)