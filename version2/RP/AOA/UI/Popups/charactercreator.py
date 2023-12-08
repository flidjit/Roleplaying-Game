import tkinter as tk
from tkinter import ttk


class AOACharacter:
    def __init__(self):
        self.name = 'Bob'
        self.name = 'Character Name'
        self.owner = 'Player Name'
        self.description = {
            'Bio': 'Some Dude.',
            'Height': [5, 9],
            'Weight': 140,
            'Skin Color': 'Green',
            'Eye Color': 'Yellow',
            'Age': 20}
        self.power_level = 0
        self.credits = 50
        self.hp = [30, 30]
        self.ap = [6, 6]
        self.instinct = +0
        self.Triad = {
            'Body': [+4, 7, 7],
            'Mind': [+4, 7, 7],
            'Spirit': [+4, 7, 7]}
        self.resistances = []
        self.weaknesses = []
        self.status_effects = []
        self.loadout = {
            'Left': None,
            'Right': None}
        self.pack = []
        self.gear = {
            'Head': None,
            'Face': None,
            'Neck': None,
            'Back': None,
            'Shoulders': None,
            'Arms': None,
            'Wrists': None,
            'Hands': None,
            'Torso': None,
            'Waist': None,
            'Legs': None,
            'Knees': None,
            'Shins': None,
            'Feet': None}
        self.rings = {
            'Right': [],
            'Left': []}
        self.key_items = []
        self.quirks = {}
        self.techniques = {}
        self.card_list = {}