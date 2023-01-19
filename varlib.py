
default_ui_icons = {
    'Map': 'usr/config/ui/Default/maptabicon.png',
    'Sheet': 'usr/config/ui/Default/stattabicon.png',
    'Props': 'usr/config/ui/Default/proptabicon.png',
    'Party': 'usr/config/ui/Default/grouptabicon.png',
    'Actions': 'usr/config/ui/Default/actiontabicon.png',
    'World': 'usr/config/ui/Default/worldtabicon.png',
    'Help': 'usr/config/ui/Default/helptabicon.png'}

default_ui_colors = {
    'Root BG': '#240e28',
    'Viewport BG': '#240e28',
    'TNotebook - BG': "#240e28",
    'TNotebook.Tab - BG': "#240e28",
    'TNotebook.Tab - FG': "white",
    'TNotebook.Tab - Selected BG': "#d8247c",
    'TNotebook.Tab - Selected FG': "black",
    'ChatSection - BG': "black",
    'ChatSection - FG': "#25a9f0",
    'InputSection - BG': "black",
    'InputSection - FG': "green",
    'SheetTab - BG': "black",
    'SheetTab - Text': "white",
    'MiniMap - BG': "#0c090d",
    'MapTab - BG': "black",
    'MapTab - Text': '#c96c9a',
    'PropTab - BG': "black",
    'PartyTab - BG': "black",
    'WorldTab - BG': "black",
    'HelpTab - BG': "black",
    'ActionTab - BG': "black"}

default_keyboard_bindings = [
    ["control", "control"],
    ['shift', 'shift'],
    ["arrow_up", "Move Camera Up"],
    ["arrow_down", "Move Camera Down"],
    ["arrow_left", "Move Camera Left"],
    ["arrow_right", "Move Camera Right"],
    ["space", "Reset Camera to Target"],
    ["page_up", "Zoom In"],
    ["page_down", "Zoom Out"],
    ["e", "Rotate Camera Clockwise"],
    ["q", "Rotate Camera Counter-Clockwise"],
    ["a", "Move Selected Left"],
    ["s", "Move Selected Down"],
    ["w", "Move Selected Up"],
    ["d", "Move Selected Right"],
    ["f", "Add New Floor Tile"],
    ["`", "Print Map Info"]]

default_terrain_tiles = [
    'basic/purp',
    'basic/stone',
    'basic/brick1',
    'basic/standardTile']

default_tile_atlas = {'0,0': 'Chunk 1'}

map_dirs = {
    "North": {
        "position": [-1, 0],
        "rotation": 90},
    "South": {
        "position": [+1, 0],
        "rotation": 90},
    "East": {
        "position": [0, +1],
        "rotation": 90},
    "West": {
        "position": [0, -1],
        "rotation": 90}}

cam_dirs = {
    "Order": ["North-West", "South-West",
              "South-East", "North-East"],
    "North-West": {
        "position": [10, 10],
        "Up": "North",
        "Down": "South",
        "Left": "West",
        "Right": "East"},
    "South-West": {
        "position": [-10, 10],
        "Up": "East",
        "Down": "West",
        "Left": "North",
        "Right": "South"},
    "South-East": {
        "position": [-10, -10],
        "Up": "South",
        "Down": "North",
        "Left": "East",
        "Right": "West"},
    "North-East": {
        "position": [10, -10],
        "Up": "West",
        "Down": "East",
        "Left": "South",
        "Right": "North"}}
