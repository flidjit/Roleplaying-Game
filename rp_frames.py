import tkinter as tk
from tkinter import ttk
from rp_proto import *
from propshop import *


class CSheet1(tk.Canvas):
    def __init__(self, master=None):
        tk.Canvas.__init__(self, master=master)
        self.character = Character()
        self.config(bg='black', width=450, height=600,
                    borderwidth=0, highlightthickness=0)
        self.c_sheet_img = tk.PhotoImage(
            file='Scraps/CharacterSheet/UIsheet/page_1.png')
        self.bg_1 = self.create_image(
            0, 0, anchor='nw', image=self.c_sheet_img)

        self.name_i = self.create_text(
            16, 16, anchor='nw', text="Character Name",
            fill='pink', font=("Times", 15, "bold"))
        self.power_level_i = self.create_text(
            380, 26, anchor='center', text="344",
            fill='pink', font=("courier", 15, "bold"))
        self.credits_i = self.create_text(
            335, 44, anchor='nw', text="$ 100.00",
            fill='green', font=("courier", 10, "bold"))
        self.instinct_i = self.create_text(
            399, 236, anchor='center', text="12",
            fill='yellow', font=("courier", 15, "bold"))
        self.hp_cur_i = self.create_text(
            80, 90, anchor='center', text='66',
            fill='white', font=("courier", 18, "bold"))
        self.hp_max_i = self.create_text(
            128, 96, anchor='center', text='66',
            fill='white', font=("courier", 18, "bold"))
        self.h_bar = self.create_line(
            169, 89, 369, 89, fill='white', width=2)

        self.b_bonus_i = self.create_text(
            60, 132, anchor='center', text="5",
            fill='lime green', font=("courier", 15, "bold"))
        self.b_def_i = self.create_text(
            109, 132, anchor='center', text="15",
            fill='lime green', font=("courier", 15, "bold"))
        self.b_ep_cur_i = self.create_text(
            160, 128, anchor='center', text="666",
            fill='black', font=("courier", 12, "bold"))
        self.b_ep_max_i = self.create_text(
            195, 135, anchor='center', text="666",
            fill='black', font=("courier", 12, "bold"))
        self.b_bar = self.create_line(
            233, 128, 433, 128, fill='lime green', width=2)

        self.m_bonus_i = self.create_text(
            60, 164, anchor='center', text="5",
            fill='sky blue', font=("courier", 15, "bold"))
        self.m_def_i = self.create_text(
            109, 164, anchor='center', text="15",
            fill='sky blue', font=("courier", 15, "bold"))
        self.m_ep_cur_i = self.create_text(
            160, 159, anchor='center', text="666",
            fill='black', font=("courier", 12, "bold"))
        self.m_ep_max_i = self.create_text(
            195, 166, anchor='center', text="666",
            fill='black', font=("courier", 12, "bold"))
        self.m_bar = self.create_line(
            233, 159, 433, 159, fill='sky blue', width=2)

        self.s_bonus_i = self.create_text(
            60, 196, anchor='center', text="5",
            fill='pink', font=("courier", 15, "bold"))
        self.s_def_i = self.create_text(
            109, 194, anchor='center', text="15",
            fill='pink', font=("courier", 15, "bold"))
        self.s_ep_cur_i = self.create_text(
            160, 189, anchor='center', text="666",
            fill='black', font=("courier", 12, "bold"))
        self.s_ep_max_i = self.create_text(
            195, 197, anchor='center', text="666",
            fill='black', font=("courier", 12, "bold"))
        self.s_bar = self.create_line(
            233, 191, 433, 191, fill='pink', width=2)

        self.status_effect_list = tk.Variable(value=None)
        self.status_effect_list_i = tk.Listbox(
            self, bg='#2C2331', fg='yellow',
            borderwidth=0, highlightthickness=0, relief='flat',
            listvariable=self.status_effect_list)  # #2C2331
        self.status_effect_list_i.place(x=17, y=267, width=180, height=86)

        self.quirk_list = tk.Variable(value=None)
        self.quirk_list_i = tk.Listbox(
            self, bg='#2C2331', fg='pink', borderwidth=0,
            highlightthickness=0, relief='flat',
            listvariable=self.quirk_list)  # #2C2331
        self.quirk_list_i.place(x=245, y=268, width=180, height=245)

        self.resistance_list = tk.Variable(value=None)
        self.resistance_list_i = tk.Listbox(
            self, bg='#2C2331', fg='sky blue', borderwidth=0,
            highlightthickness=0, relief='flat',
            listvariable=self.resistance_list)  # #2C2331
        self.resistance_list_i.place(x=17, y=370, width=180, height=63)

        self.weakness_list = tk.Variable(value=None)
        self.weakness_list_i = tk.Listbox(
            self, bg='#2C2331', fg='orange', borderwidth=0,
            highlightthickness=0, relief='flat',
            listvariable=self.weakness_list)  # #2C2331
        self.weakness_list_i.place(x=17, y=450, width=180, height=63)

        self.left_hand_i = tk.Text(
            self, bg='#2C2331', fg='white', borderwidth=0,
            highlightthickness=0, relief='flat',
            font=("courier", 10, "normal"))
        self.left_hand_i.place(x=15, y=536, width=195, height=50)
        self.right_hand_i = tk.Text(
            self, bg='#2C2331', fg='white', borderwidth=0,
            highlightthickness=0, relief='flat',
            font=("courier", 10, "normal"))
        self.right_hand_i.place(x=239, y=536, width=195, height=50)

        self.shop_button = tk.Button(
            self, bg='black', fg='green', text='shop',
            command=self.open_shop)
        self.shop_button.place(x=390, y=75, height=25, width=45)

        self.character_to_sheet()
        self.place(x=0, y=0)

    def open_shop(self, *args):
        self.character = Shopping(
            self, character=self.character, gm_=True).show()

    def character_to_sheet(self, *args):
        c = self.character
        self.itemconfig(self.name_i, text=c.dat['Name'])
        self.itemconfig(self.power_level_i, text=c.dat['Power Level'])
        t = '$ '+str(c.dat['Credits'])+'.00'
        self.itemconfig(self.credits_i, text=t)
        self.itemconfig(self.instinct_i, text=c.dat['Instinct'])
        self.itemconfig(self.hp_cur_i, text=c.dat['HP'][0])
        self.itemconfig(self.hp_max_i, text=c.dat['HP'][1])
        self.itemconfig(self.b_bonus_i, text=c.dat['Body']['Bonus'])
        self.itemconfig(self.m_bonus_i, text=c.dat['Mind']['Bonus'])
        self.itemconfig(self.s_bonus_i, text=c.dat['Spirit']['Bonus'])
        self.itemconfig(self.b_def_i, text=str(10+c.dat['Body']['Bonus']))
        self.itemconfig(self.m_def_i, text=str(10+c.dat['Mind']['Bonus']))
        self.itemconfig(self.s_def_i, text=str(10+c.dat['Spirit']['Bonus']))
        self.itemconfig(self.b_ep_cur_i, text=c.dat['Body']['Energy'][0])
        self.itemconfig(self.m_ep_cur_i, text=c.dat['Mind']['Energy'][0])
        self.itemconfig(self.s_ep_cur_i, text=c.dat['Spirit']['Energy'][0])
        self.itemconfig(self.b_ep_max_i, text=c.dat['Body']['Energy'][1])
        self.itemconfig(self.m_ep_max_i, text=c.dat['Mind']['Energy'][1])
        self.itemconfig(self.s_ep_max_i, text=c.dat['Spirit']['Energy'][1])
        print(c.dat['HP'][0])
        print(c.dat['HP'][1])
        l = int(c.dat['HP'][0]) / int(c.dat['HP'][1]) * 200
        self.coords(self.h_bar, 169, 89, 169+l, 89)
        l = int(c.dat['Body']['Energy'][0]) / int(c.dat['Body']['Energy'][1]) * 200
        self.coords(self.b_bar, 233, 128, 233+l, 128)
        l = int(c.dat['Mind']['Energy'][0]) / int(c.dat['Mind']['Energy'][1]) * 200
        self.coords(self.m_bar, 233, 159, 233+l, 159)
        l = int(c.dat['Spirit']['Energy'][0]) / int(c.dat['Spirit']['Energy'][1]) * 200
        self.coords(self.s_bar, 233, 191, 233+l, 191)
        self.quirk_list.set(value=c.dat['Quirks'])
        self.status_effect_list.set(value=c.dat['Status Effects'])
        self.resistance_list.set(value=c.dat['Resistances'])
        self.weakness_list.set(value=c.dat['Weaknesses'])
        lh = self.get_loadout(c, 'Left')
        self.left_hand_i.insert(0.0, lh)
        lh = self.get_loadout(c, 'Right')
        self.right_hand_i.insert(0.0, lh)

    def get_loadout(self, c=None, hand=None):
        nm = c.dat['Loadout'][hand]
        p = None
        if nm in c.dat['Gear']['Pack']:
            p = c.dat['Gear']['Pack'][nm]
        if nm in c.dat['Gear']['At Hand']:
            p = c.dat['Gear']['At Hand'][nm]
        t = p.dat['Name']+'\n'+p.dat['Description']
        return t

