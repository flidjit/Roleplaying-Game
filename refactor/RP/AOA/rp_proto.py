class Card:
    def __init__(self, name_='<Card Name>',
                 description_='<Card Description>',
                 placement_='<Placement>',
                 type_='<Type>',
                 credit_cost_=0,
                 parent_=None,
                 tech_level_=0,
                 fantasy_level_=0,
                 ammo_=None,
                 clips_=None,
                 quirk_gains_=None,
                 stat_gains_=None,
                 technique_gains_=None,
                 character_mods_=None,
                 technique_mods_=None,
                 parent_mods_=None,
                 sub_nodes_=None):
        self.dat = {
            'Name': name_,
            'Description': description_,
            'Placement': placement_,
            'Type': type_,
            'Credit Cost': credit_cost_,
            'Parent': parent_,
            'Technology Level': tech_level_,
            'Fantasy Level': fantasy_level_,
            'Ammo': ammo_,
            'Clips': clips_,
            'Quirk Gains': quirk_gains_,
            'Stat Gains': stat_gains_,
            'Technique Gains': technique_gains_,
            'Character Mod': character_mods_,
            'Technique Mod': technique_mods_,
            'Parent Mod': parent_mods_,
            'Sub-Nodes': sub_nodes_}


class StatusEffect:
    def __init__(self):
        self.name = 'Stun'
        self.description = ''
        self.tokens = 0
        self.dc = 14


class Technique:
    def __init__(self, name_='', description_='', requires_='',
                 ap_cost_=0, ammo_cost_=0, per_day_=None, per_combat_=None,
                 energy_cost_=None, tohit_roll_=None, target_='self',
                 range_=5, is_melee_=True, damage_roll_=None,
                 inflict_effect_=None):
        self.dat = {
            'Name': name_,
            'Description': description_,
            'Requires': requires_,
            'AP Cost': ap_cost_,
            'Ammo Cost': ammo_cost_,
            'Per Day Uses': per_day_,
            'Per Combat Uses': per_combat_,
            'Energy Cost': energy_cost_,
            'ToHit Roll': tohit_roll_,  # string"(C)+4+[Sword] VS (B)"
            'Target': target_,
            'Range': range_,
            'Is Melee': is_melee_,
            'Damage Roll': damage_roll_,  # string"1d6+5<Slash>"
            'Inflict Effect': inflict_effect_}


punch = Technique(
    name_='Punch', description_='Hit a guy with your fist.', requires_='Fist',
    ap_cost_=2, tohit_roll_='(C)+1 VS (B)', target_='Single Enemy',
    range_=5, damage_roll_='1d4[Bash]')


fist = Card(
    name_='Fist', description_='A bare hand crumpled up into a ball.',
    placement_='At Hand', type_='Melee Weapon')


class Character:
    def __init__(self):
        self.dat = {
            'Player': 'Bobby',
            'Email': '',
            'Name': 'Bobbitha',
            'Sex': 'Male',
            'Credits': 0,
            'Power Level': 0,
            'HP': [25, 30],
            'Body': {
                'Bonus': +2,
                'Energy': [2, 3]},
            'Mind': {
                'Bonus': +3,
                'Energy': [2, 3]},
            'Spirit': {
                'Bonus': +4,
                'Energy': [2, 3]},
            'AP': [6, 6],
            'Instinct': +0,
            'Status Effects': ['Stun (8) DC:15', 'Bleed (8) DC:15'],
            'Resistances': ['Slash DR:5', 'Pierce DR:10'],
            'Weaknesses': ['Bash x2'],
            'Quirks': ['Juggling +4', 'Sword Master +3'],
            'Loadout': {
                'Left': "Fist",
                'Right': "Fist"},
            'Gear': {
                'Pack': {},
                'At Hand': {"Fist": fist},
                'Head': None,
                'Face': None,
                'Neck': None,
                'Wrists': None,
                'Hands': None,
                'Back': None,
                'Torso': None,
                'Waist': None,
                'Legs': None,
                'Feet': None,
                'Finger': []},
            'Techniques': {'Punch': punch},
            'Deck': {},
            'Notes': []}

