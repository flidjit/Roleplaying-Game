

class Character:
    def __init__(self, player_name='gm', character_name='character',
                 stats=None, scores=None, props=None,
                 skills=None, traits=None, techniques=None,
                 campaign_data=None):
        self.player_name = player_name
        if stats:
            self.stats = stats
        else:
            self.stats = {
                'Monsters Slain': 0,
                'Creation Date': 1}
        if self.scores:
            self.scores = scores
        else:
            self.scores = {
                'HP': [30, 30],
                'Energy': {'EP': [10, 10]},
                'AP': [6, 6],
                'Defense': 10,
                'Attack': None,
                'UPs': 0,
                'Power Level': 0}
        if self.techniques:
            self.techniques = techniques
        else:
            self.techniques = {}
        if self.skills:
            self.skills = skills
        else:
            self.skills = {}
        if self.traits:
            self.traits = traits
        else:
            self.traits = {}
        if props:
            self.props = props
        else:
            self.props = {}
        if self.campaign_data:
            self.campaign_data = campaign_data
        else:
            self.campaign_data = {
                'gm': 'Bob'}


class Prop:
    def __init__(self):
        self.name = 'A prop.'
        self.up_cost = 0
        self.technology_level = 1
        self.fantasy_level = 1
        self.tags = []
        self.requires = {'HP': None, 'EP': None, 'Power Level': None,
                         'Skill': [None, 0], 'Trait': [None, 0]}
        self.add_traits = {}
        self.add_skills = {}
        self.upgrades = []
        self.techniques = []
        self.trigger_execute_ = {'Purchase': None}


class Armor(Prop):
    def __init__(self):
        Prop.__init__(self)
        self.equip_location = ''


class Weapon(Prop):
    def __init__(self):
        Prop.__init__(self)
        self.required_hands = 1


class Motivate:

    @staticmethod
    def meets_prop_requirements(a_character=Character(), prop=Prop()):
        can_buy = True
        r = prop.requires
        c = a_character
        if r['Power Level']:
            if r['Power Level'] > c.scores['Power Level'][1]:
                can_buy = False
        if r['HP']:
            if r['HP'] > c.scores['HP'][1]:
                can_buy = False
        if r['EP']:
            if r['EP'] > c.scores['Energy']['EP'][1]:
                can_buy = False
        if r['Skill'][0]:
            if r['Skill'][0] not in c.skills:
                can_buy = False
                if r['Skill'][1] > c.skills[r['Skill'][0]]:
                    can_buy = False
        if r['Trait'] not in c.traits:
            can_buy = False
        return can_buy

    @staticmethod
    def valid_prop_list_from_shop_list(a_character=Character(), prop_list=None):
        temp_list = []
        for i in prop_list:
            if Motivate.meets_prop_requirements(a_character, prop_list[i]):
                temp_list.append(prop_list[i])
        return temp_list

    @staticmethod
    def buy_prop(a_character=Character(), prop=Prop()):
        a_character.scores['UPs'] -= prop.up_cost
        a_character.scores['Power Level'] += prop.up_cost
        a_character.props[prop.name] = prop
        x = a_character.props[prop.name].trigger_execute_['Purchase']
        if x:
            exec(x)
