import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from rp_proto import *
from copy import deepcopy
import pickle


class CardEditor(tk.Toplevel):
    def __init__(self, master=None, card=Card()):
        tk.Toplevel.__init__(self, master=master,
                             width=540, height=660,
                             bg='#2C2331')
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.save_and_close)
        self.fonts = {
            'Title': ("Times", 10, "bold"),
            'Sub-Title': ("Courier", 8, "bold"),
            'Numbers': ("FreeMono", 8, "bold"),
            'Description': ("Sans", 10, "normal")}
        self.colors = {
            'Background': '#18121b',
            'Text 1': 'white',
            'Text 2': 'grey',
            'Text 3': 'lime green'}

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
            'Mod', 'Weapon', 'Tool', 'Attire', 'Consumable', 'Book',
            'Trinket', 'Phenotype', 'Companion', 'Vehicle']
        self.type_entry_i = ttk.Combobox(self, values=self.type_val)
        self.type_entry_i.place(x=380, y=18, width=150, height=25)

        self.placement_l = tk.Label(
            self, bg='#2C2331', fg='green', text='Placement:', justify='left')
        self.placement_l.place(x=380, y=50, width=90, height=15)
        self.placement_val = [
            'Special', 'Pack', 'At Hand', 'Head', 'Face', 'Neck', 'Wrists',
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


class CardView(tk.Canvas):
    def __init__(self, master=None, card=Card()):
        tk.Canvas.__init__(
            self, master=master,
            width=249, height=340,
            highlightthickness=0, borderwidth=0,
            background='#18121b')
        self.bg_image = tk.PhotoImage(
            file='Scraps/CharacterSheet/UIsheet/poker-card.png')
        self.bg_i = self.create_image(
            0, 0, anchor='nw', image=self.bg_image)
        self.fonts = {
            'Title': ("Times", 10, "bold"),
            'Sub-Title': ("Courier", 8, "bold"),
            'Numbers': ("FreeMono", 8, "bold"),
            'Description': ("Sans", 10, "normal")}
        self.colors = {
            'Background': '#18121b',
            'Text 1': 'white',
            'Text 2': 'grey',
            'Text 3': 'lime green'}

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
            'Wrists': tk.PhotoImage(
                file=f_loc+'wristgear.png'),
            'At Hand': tk.PhotoImage(
                file=f_loc+'athandgear.png')}
        ico = self.placement_icons['At Hand']
        self.placement_i = self.create_image(
            165, 10, anchor='nw', image=ico)

        self.name_i = self.create_text(
            30, 30, anchor='nw',
            fill=self.colors['Text 1'],
            text=card.dat['Name'],
            font=self.fonts['Title'])
        self.type_i = self.create_text(
            30, 54, anchor='nw',
            fill=self.colors['Text 2'],
            text=card.dat['Type'],
            font=self.fonts['Sub-Title'])
        cost = '$ ' + str(card.dat['Credit Cost']) + '.00'
        self.cost_i = self.create_text(
            150, 73, anchor='nw',
            fill=self.colors['Text 1'],
            text=cost,
            font=self.fonts['Numbers'])
        self.tech_lev_i = self.create_text(
            45, 69, anchor='nw',
            fill=self.colors['Text 2'],
            text='TL: '+str(card.dat['Technology Level']),
            font=self.fonts['Numbers'])
        self.fant_lev_i = self.create_text(
            97, 69, anchor='nw',
            fill=self.colors['Text 2'],
            text='FL: '+str(card.dat['Fantasy Level']),
            font=self.fonts['Numbers'])

        self.description_i = tk.Text(
            self, highlightthickness=0, borderwidth=0,
            bg='black',
            fg=self.colors['Text 3'],
            font=self.fonts['Description'])
        self.description_i.place(x=38, y=174, width=172, height=130)
        self.grid()

    def display_card(self, card=Card()):
        self.itemconfig(
            self.name_i, text=card.dat['Name'])
        self.itemconfig(
            self.type_i, text=card.dat['Type'])
        c = str(card.dat['Credit Cost']) + '.00'
        self.itemconfig(
            self.cost_i, text=c)
        self.itemconfig(
            self.tech_lev_i, text=card.dat['Technology Level'])
        self.itemconfig(
            self.fant_lev_i, text=card.dat['Fantasy Level'])
        img = self.placement_icons[card.dat['Placement']]
        self.itemconfig(
            self.placement_i, image=img)

        self.description_i.delete('0.0', 'end')
        self.description_i.insert('0.0', card.dat['Description'])


class DeckView(tk.Canvas):
    def __init__(self, master=None, gm_=True):
        tk.Canvas.__init__(
            self, master=master, bg='black',
            width=249, height=540, highlightthickness=0,
            borderwidth=0)
        self.card_i = CardView(self)
        self.card_i.place(x=0, y=0)

        self.sell_butt = tk.Button(self, text='< SELL')
        self.sell_butt.place(x=170, y=310, width=60, height=20)

        self.deck_tree = ttk.Treeview(
            self, columns='prop_name_', show='headings')
        self.deck_tree.heading('prop_name_', text='<Character Name>', anchor='w')
        self.deck_tree.column('prop_name_', minwidth=0, width=249,
                              stretch=tk.NO)
        self.deck_tree.place(x=0, y=340, width=249, height=200)
        self.grid()

    def get_selected_(self):
        selected = self.deck_tree.focus()
        return self.deck_tree.item(selected)['values'][0]

    def display_card(self, card=Card()):
        self.card_i.display_card(card=card)

    def pupulate_list_(self, deck=None):
        print('populate the treeview')


class Shop:
    def __init__(self):
        self.name = "A Shop"
        self.description = "No really. It's a shop."
        self.card_list = {}


class ShopView(tk.Canvas):
    def __init__(self, master=None, gm_=True):
        tk.Canvas.__init__(
            self, master=master, bg='#18121b',
            width=249, height=540, highlightthickness=0, borderwidth=0)

        self.description_i = tk.Text(
            self, bg='black', fg='lime green',
            highlightthickness=0, borderwidth=0)
        self.description_i.place(x=10, y=10, width=229, height=200)

        self.buy_butt = tk.Button(self, text='BUY >')
        self.buy_butt.place(x=170, y=225, width=60, height=20)

        if gm_:
            self.gm_options = GMShopOptions(self)
            self.gm_options.place(x=0, y=248, width=249, height=90)
        self.shop_tree = ttk.Treeview(
            self, columns='prop_name_', show='headings')
        self.shop_tree.heading('prop_name_', text='<Shop Name>', anchor='w')
        self.shop_tree.column('prop_name_', minwidth=0, width=249,
                              stretch=tk.NO)
        y = 250
        h = 290
        if gm_:
            y = 340
            h = 200
        self.shop_tree.place(x=0, y=y, width=249, height=h)
        self.grid()

    def get_selected_(self):
        selected = self.shop_tree.focus()
        return self.shop_tree.item(selected)['values'][0]

    def populate_list_(self, shop=Shop()):
        for i in shop.card_list:
            name = shop.card_list[i].dat['Name']
            self.shop_tree.insert(
                '', tk.END, iid=name, values=[name])

    @staticmethod
    def save_shop_(shop=Shop()):
        filename = 'Catalog/Prop Shop/'+shop.name+'.shop'
        s_file = open(filename, 'wb')
        pickle.dump(shop, s_file)
        s_file.close()

    @staticmethod
    def load_shop_():
        filename = askopenfilename(
            title='Open a Shop File', initialdir='Catalog/Prop Shop/',
            filetypes=[('Shop Files', '*.shop')])
        file = open(filename, 'rb')
        shop = pickle.load(file)
        file.close()
        return shop


class GMShopOptions(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(
            self, master=master, bg='black',
            width=249, height=100, highlightthickness=0, borderwidth=0)
        self.new_shop_butt = tk.Button(self, text='New')
        self.new_shop_butt.place(x=10, y=10, height=20, width=50)
        self.save_shop_butt = tk.Button(self, text='Save')
        self.save_shop_butt.place(x=65, y=10, height=20, width=50)
        self.load_shop_butt = tk.Button(self, text='Load')
        self.load_shop_butt.place(x=120, y=10, height=20, width=50)
        self.merge_shop_butt = tk.Button(self, text='Merge')
        self.merge_shop_butt.place(x=175, y=10, height=20, width=50)
        self.new_card_butt = tk.Button(self, text='New')
        self.new_card_butt.place(x=10, y=35, height=20, width=50)
        self.del_card_butt = tk.Button(self, text='Delete')
        self.del_card_butt.place(x=65, y=35, height=20, width=50)
        self.edit_card_butt = tk.Button(self, text='Edit')
        self.edit_card_butt.place(x=120, y=35, height=20, width=50)


class Shopping(tk.Toplevel):
    def __init__(self, master=None, gm_=True,
                 shop=Shop(), character=Character()):
        tk.Toplevel.__init__(
            self, master=master, bg='#18121b')
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.shop = shop
        self.shop_view = ShopView(self, gm_)
        self.shop_view.grid(row=0, column=0, padx=10, pady=10)

        self.character = character
        self.deck_view = DeckView(self)
        self.deck_view.grid(row=0, column=1, padx=10, pady=10)

        self.grid()
        self.bind_actions()

    def bind_actions(self):
        self.shop_view.shop_tree.bind(
            "<<TreeviewSelect>>", self.display_shop_card)
        self.deck_view.deck_tree.bind(
            "<<TreeviewSelect>>", self.display_deck_card)
        self.shop_view.gm_options.new_shop_butt.configure(
            command=self.new_shop_)
        self.shop_view.gm_options.load_shop_butt.configure(
            command=self.load_shop_)
        self.shop_view.gm_options.save_shop_butt.configure(
            command=self.save_shop_)
        self.shop_view.gm_options.merge_shop_butt.configure(
            command=self.merge_shop_)
        self.shop_view.gm_options.new_card_butt.configure(
            command=self.new_card_)
        self.shop_view.gm_options.del_card_butt.configure(
            command=self.delete_card_)
        self.shop_view.gm_options.edit_card_butt.configure(
            command=self.edit_card_)
        self.shop_view.buy_butt.configure(
            command=self.buy_)
        self.shop_view.buy_butt.configure(
            command=self.sell_)

    def display_deck_card(self, *args):
        selected_card = self.deck_view.get_selected_()
        card = self.character.dat['Deck'][selected_card]
        self.deck_view.display_card(card=card)

    def display_shop_card(self, *args):
        selected_card = self.shop_view.get_selected_()
        card = self.shop.card_list[selected_card]
        self.deck_view.display_card(card=card)

    def new_shop_(self, *args):
        print('a new shop')
        self.refresh_shop_list_()

    def save_shop_(self, *args):
        self.shop_view.save_shop_(self.shop)

    def load_shop_(self, *args):
        self.shop = self.shop_view.load_shop_()
        self.refresh_shop_list_()

    def edit_shop_(self, *args):
        print('edit the shop name/description.')

    def merge_shop_(self, *args):
        print('Merge 2 shops.')
        self.refresh_shop_list_()

    def new_card_(self, *args):
        crd = CardEditor().show()
        self.shop.card_list[crd.dat['Name']] = crd
        self.refresh_shop_list_()

    def delete_card_(self, *args):
        print('delete a card.')
        self.refresh_shop_list_()

    def edit_card_(self, *args):
        self.refresh_shop_list_()

    def refresh_shop_list_(self, *args):
        self.shop_view.populate_list_(self.shop)

    def refresh_deck_list_(self, *args):
        self.deck_view.pupulate_list_(
            self.character.dat['Deck'])

    def buy_(self):
        print('buy selected card.')

    def sell_(self):
        print('sell selected card.')

    def done_(self):
        print('confirm purchase')

    def cancel_(self):
        print('cancel purchase')

    def show(self):
        self.deiconify()
        self.wait_window()
        return deepcopy(self.character)


