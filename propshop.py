import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile, askopenfilename
from rp_proto import *
from copy import copy, deepcopy
import pickle


class Shop:
    def __init__(self):
        self.name = "A Shop"
        self.description = "No really. It's a shop."
        self.card_list = {}


class Shopping(tk.Toplevel):
    def __init__(self, master=None, gm_=True,
                 character=Character(), shop=Shop()):
        tk.Toplevel.__init__(self, master=master,
                             width=600, height=600,
                             bg='#2C2331')
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.character = character
        self.shop = shop

        self.bg_image = tk.PhotoImage(
            file='Scraps/CharacterSheet/UIsheet/shopimage.png')
        self.bg_i = tk.Label(self, image=self.bg_image)
        self.bg_i.place(x=0, y=0, width=600, height=600)

        self.card_display = NodeViewer(self)
        self.card_display.place(x=300, y=0)

        self.shop_name_i = tk.Label(
            self, bg='#2C2331', fg='white', text=shop.name)
        self.shop_name_i.place(x=10, y=10)
        self.shop_description_i = tk.Label(
            self, bg='#2C2331', fg='white', text=shop.description)
        self.shop_description_i.place(x=10, y=40)

        self.buy_butt = tk.Button(self, text='Buy')
        self.buy_butt.place(x=198, y=273, height=20, width=60)
        self.bt_cols = ('prop_name_', 'prop_cost_')
        self.buy_tree = ttk.Treeview(
            self, columns=self.bt_cols, show='headings')
        self.buy_tree.heading('prop_name_', text='Shop', anchor='w')
        self.buy_tree.column('prop_name_', minwidth=0, width=200,
                             stretch=tk.NO)
        self.buy_tree.heading('prop_cost_', text='$$', anchor='w')
        self.buy_tree.column('prop_cost_', minwidth=0, width=100)
        self.buy_tree.place(x=10, y=300, width=276, height=293)

        h = 293
        if gm_:
            h = 185

        self.sell_butt = tk.Button(self, text='Sell')
        self.sell_butt.place(x=348, y=273, height=20, width=60)
        self.st_cols = ('prop_name_', 'prop_cost_')
        self.sell_tree = ttk.Treeview(
            self, columns=self.bt_cols, show='headings')
        self.sell_tree.heading('prop_name_', text='Character', anchor='w')
        self.sell_tree.column('prop_name_', minwidth=0, width=200,
                              stretch=tk.NO)
        self.sell_tree.heading('prop_cost_', text='$$', anchor='w')
        self.sell_tree.column('prop_cost_', minwidth=0, width=100,
                              stretch=tk.NO)
        self.sell_tree.place(x=315, y=300, width=276, height=h)

        if gm_:
            self.new_shop_butt = tk.Button(self, text='New')
            self.new_shop_butt.place(x=320, y=510, height=20, width=50)
            self.save_shop_butt = tk.Button(
                self, text='Save', command=self.save_shop)
            self.save_shop_butt.place(x=375, y=510, height=20, width=50)
            self.load_shop_butt = tk.Button(
                self, text='Load', command=self.load_shop)
            self.load_shop_butt.place(x=430, y=510, height=20, width=50)
            self.merge_shop_butt = tk.Button(
                self, text='Merge', command=self.load_shop)
            self.merge_shop_butt.place(x=485, y=510, height=20, width=50)
            self.new_card_butt = tk.Button(
                self, text='New', command=self.new_card)
            self.new_card_butt.place(x=320, y=559, height=20, width=50)
            self.del_card_butt = tk.Button(self, text='Delete')
            self.del_card_butt.place(x=375, y=559, height=20, width=50)
            self.edit_card_butt = tk.Button(self, text='Edit')
            self.edit_card_butt.place(x=430, y=559, height=20, width=50)

    def save_shop(self):
        filename = 'Catalog/Prop Shop/'+self.shop.name+'.shop'
        s_file = open(filename, 'wb')
        pickle.dump(self.shop, s_file)
        s_file.close()

    def load_shop(self):
        filename = askopenfilename(
            title='Open a Shop File', initialdir='Catalog/Prop Shop/',
            filetypes=[('Shop Files', '*.shop')])
        file = open(filename, 'rb')
        self.shop = pickle.load(file)
        file.close()

    def new_card(self):
        crd = NodeEditor().show()
        self.shop.card_list[crd.dat['Name']] = crd
        self.make_shop_list()
        self.card_display.show_node(crd)

    def make_shop_list(self):
        for i in self.buy_tree.get_children():
            self.buy_tree.delete(i)
        lst = self.shop.card_list
        num = 0
        for i in lst:
            val = [lst[i].dat['Name'],
                   lst[i].dat['Credit Cost']]
            print(val)
            self.buy_tree.insert(parent='', id=str(num), index='end',
                                 values=val)
            num += 1
        for i in lst:
            print(i)
            print('N:'+lst[i].dat['Name'])

    def show(self):
        self.deiconify()
        self.wait_window()
        return deepcopy(self.character)


class NodeEditor(tk.Toplevel):
    def __init__(self, master=None, card=Node()):
        tk.Toplevel.__init__(self, master=master,
                             width=540, height=660,
                             bg='#2C2331')
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.save_and_close)

        self.card = card

        self.name_l = tk.Label(
            self, bg='#2C2331', fg='green', text='Name:', justify='left')
        self.name_l.place(x=15, y=0, width=75, height=15)
        self.name_entry_i = tk.Entry(self, bg='black', fg='pink')
        self.name_entry_i.place(x=15, y=15, width=260, height=30)

        self.cost_l = tk.Label(
            self, bg='#2C2331', fg='green', text='Cost:', justify='left')
        self.cost_l.place(x=290, y=0, width=75, height=15)
        self.cost_entry_i = tk.Entry(self, bg='black', fg='pink')
        self.cost_entry_i.place(x=290, y=15, width=80, height=30)

        self.type_l = tk.Label(
            self, bg='#2C2331', fg='green', text='Type:', justify='left')
        self.type_l.place(x=380, y=0, width=90, height=15)
        self.type_val = [
            'Melee Weapon', 'Ranged Weapon', 'Tool', 'Attire',
            'Consumable', 'Prop Mod', 'Technique Mod']
        self.type_entry_i = ttk.Combobox(self, values=self.type_val)
        self.type_entry_i.place(x=380, y=18, width=150, height=25)

        self.placement_l = tk.Label(
            self, bg='#2C2331', fg='green', text='Placement:', justify='left')
        self.placement_l.place(x=380, y=50, width=90, height=15)
        self.placement_val = [
            'Pack', 'At-Hand', 'Head', 'Face', 'Neck', 'Wrists',
            'Hands', 'Back', 'Torso', 'Waist', 'Legs', 'Feet', 'Finger']
        self.placement_cbox_i = ttk.Combobox(self, values=self.placement_val)
        self.placement_cbox_i.place(x=380, y=68, width=150, height=25)

        self.description_l = tk.Label(
            self, bg='#2C2331', fg='green', text='Description:', justify='left')
        self.description_l.place(x=220, y=90, width=75, height=15)
        self.description_text_i = tk.Text(
            self, bg='black', fg='pink', height=5)
        self.description_text_i.place(x=220, y=105, width=305)

        self.tech_level_l = tk.Label(
            self, bg='#2C2331', fg='green', text='Technology Level:', justify='left')
        self.tech_level_l.place(x=20, y=110, width=120, height=15)
        self.tech_level_sp_i = ttk.Spinbox(self, from_=0, to=5, width=2)
        self.tech_level_sp_i.place(x=155, y=110)

        self.fant_level_l = tk.Label(
            self, bg='#2C2331', fg='green', text='Fantasy Level:', justify='left')
        self.fant_level_l.place(x=20, y=150, width=120, height=15)
        self.fant_level_sp_i = ttk.Spinbox(self, from_=0, to=5, width=2)
        self.fant_level_sp_i.place(x=155, y=150)

        self.ammo_per_clip_l = tk.Label(
            self, bg='#2C2331', fg='green', text='Ammo per Clip:', justify='left')
        self.ammo_per_clip_l.place(x=20, y=190, width=120, height=15)
        self.ammo_per_clip_sp_i = ttk.Spinbox(self, from_=0, to=99, width=2)
        self.ammo_per_clip_sp_i.place(x=155, y=190)

        self.clips_per_day_l = tk.Label(
            self, bg='#2C2331', fg='green', text='Clips per Day:', justify='left')
        self.clips_per_day_l.place(x=20, y=230, width=120, height=15)
        self.clips_per_day_sp_i = ttk.Spinbox(self, from_=0, to=99, width=2)
        self.clips_per_day_sp_i.place(x=155, y=230)

        self.techniques_l = tk.Label(
            self, bg='#2C2331', fg='green', text='Techniques:', justify='left')
        self.techniques_l.place(x=10, y=270, width=75, height=15)
        self.techniques_text_i = tk.Text(
            self, bg='black', fg='pink', height=10)
        self.techniques_text_i.place(x=10, y=285, width=300)

        self.quirks_l = tk.Label(
            self, bg='#2C2331', fg='green', text='Quirks:', justify='left')
        self.quirks_l.place(x=320, y=270, width=75, height=15)
        self.quirks_text_i = tk.Text(
            self, bg='black', fg='pink', height=10)
        self.quirks_text_i.place(x=320, y=285, width=210)

        self.grid()

    def save_and_close(self, *args):
        self.card.dat['Name'] = self.name_entry_i.get()
        self.card.dat['Credit Cost'] = self.cost_entry_i.get()
        self.card.dat['Description'] = self.description_text_i.get('0.0', 'end')
        self.card.dat['Technology Level'] = self.tech_level_sp_i.get()
        self.card.dat['Fantasy Level'] = self.fant_level_sp_i.get()
        self.card.dat['Placement'] = self.placement_cbox_i.get()
        self.card.dat['Type'] = self.type_entry_i.get()
        self.grab_release()
        self.destroy()

    def show(self, *args):
        self.deiconify()
        self.wait_window()
        return deepcopy(self.card)


class NodeViewer(tk.Canvas):
    def __init__(self, master=None, node=Node()):
        tk.Canvas.__init__(
            self, master=master,
            width=300, height=250,
            highlightthickness=0, borderwidth=0)
        self.bg_image = tk.PhotoImage(
            file='Scraps/CharacterSheet/UIsheet/cardimage.png')
        self.bg_i = self.create_image(
            0, 0, anchor='nw', image=self.bg_image)

        f_loc = 'Scraps/CharacterSheet/UIsheet/gearicons/'
        self.placement_icons = {
            'Back': tk.PhotoImage(
                file=f_loc+'backgear.png'),
            'Face': tk.PhotoImage(
                file=f_loc+'facegear.png'),
            'Finger': tk.PhotoImage(
                file=f_loc+'fingergear.png'),
            'Feet': tk.PhotoImage(
                file=f_loc+'footgear.png'),
            'Hands': tk.PhotoImage(
                file=f_loc+'handgear.png'),
            'Head': tk.PhotoImage(
                file=f_loc+'headgear.png'),
            'Legs': tk.PhotoImage(
                file=f_loc+'leggear.png'),
            'Neck': tk.PhotoImage(
                file=f_loc+'neckgear.png'),
            'Pack': tk.PhotoImage(
                file=f_loc+'packgear.png'),
            'Torso': tk.PhotoImage(
                file=f_loc+'torsogear.png'),
            'Waist': tk.PhotoImage(
                file=f_loc+'waistgear.png'),
            'Wrist': tk.PhotoImage(
                file=f_loc+'wristgear.png'),
            'At-Hand': tk.PhotoImage(
                file=f_loc+'athandgear.png')}
        ico = self.placement_icons['At-Hand']
        self.placement_i = self.create_image(
            230, -10, anchor='nw', image=ico)

        self.name_i = self.create_text(
            10, 6, fill='pink', anchor='nw',
            text=node.dat['Name'])
        self.type_i = self.create_text(
            10, 27, fill='pink', anchor='nw',
            text=node.dat['Type'])
        cost = str(node.dat['Credit Cost'])+'.00'
        self.cost_i = self.create_text(
            205, 45, fill='lime green', anchor='nw',
            text=cost)
        self.tech_lev_i = self.create_text(
            240, 60, fill='grey', anchor='nw',
            text=node.dat['Technology Level'])
        self.fant_lev_i = self.create_text(
            277, 60, fill='grey', anchor='nw',
            text=node.dat['Fantasy Level'])

        self.description_i = tk.Text(
            self, bg='black', fg='green',
            highlightthickness=0, borderwidth=0)
        self.description_i.place(x=8, y=160, width=284, height=84)

        self.gains_i = tk.Text(
            self, bg='black', fg='green',
            highlightthickness=0, borderwidth=0)
        self.gains_i.place(x=8, y=160, width=284, height=84)

    def show_node(self, node=Node()):
        self.itemconfig(
            self.name_i, text=node.dat['Name'])
        self.itemconfig(
            self.type_i, text=node.dat['Type'])
        c = str(node.dat['Credit Cost'])+'.00'
        self.itemconfig(
            self.cost_i, text=c)
        self.itemconfig(
            self.tech_lev_i, text=node.dat['Technology Level'])
        self.itemconfig(
            self.fant_lev_i, text=node.dat['Fantasy Level'])

        self.description_i.delete('0.0', 'end')
        self.description_i.insert('end', node.dat['Description'])

        self.gains_i.delete('0.0', 'end')
        q = node.dat['Quirk Gains']
        if q:
            t = 'Quirk Gains: \n'
            for i in q:
                t += '   '+q[i]+'\n'
            self.gains_i.insert('end', t)
