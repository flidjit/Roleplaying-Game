
default_ui_colors = {
    'Root BG': '#240e28',
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
    'MapTab - Text': "white",
    'PropTab - BG': "black"}


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
    'basic/standardTile',
    'basic/pointer',
    'basic/pointer_target']


directions = {
    "Button Directions": ["Up", "Down", "Left", "Right"],
    "North": [-1, 0, 180],
    "North-East": [-1, 0, 180],
    "East": [0, +1, 90],
    "South-East": [-1, 0, 180],
    "South": [+1, 0, 0],
    "South-West": [-1, 0, 180],
    "West": [0, -1, 270],
    "North-West": [-1, 0, 180]}


cam_keyboard_offsets = {
        "Cam North-West": {
            "Up": "North", "Down": "South",
            "Left": "West", "Right": "East",
            "Clockwise": [-10, 10, "South-West"],
            "Counter-Clockwise": [10, -10, "North-East"]},
        "Cam South-West": {
            "Up": "West", "Down": "East",
            "Left": "South", "Right": "North",
            "Clockwise": [-10, -10, "South-East"],
            "Counter-Clockwise": [10, 10, "North-West"]},
        "Cam South-East": {
            "Up": "South", "Down": "North",
            "Left": "East", "Right": "West",
            "Clockwise": [10, -10, "North-East"],
            "Counter-Clockwise": [-10, 10, "South-West"]},
        "Cam North-East": {
            "Up": "East", "Down": "West",
            "Left": "North", "Right": "South",
            "Clockwise": [10, 10, "North-West"],
            "Counter-Clockwise": [-10, -10, "South-East"]}}
