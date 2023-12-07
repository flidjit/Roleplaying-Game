
class Character:
    def __init__(self, name, stats=None, fonts=None, colors=None, locations=None):
        self.name = name
        self.stats = stats or {}  # Stats dictionary
        self.fonts = fonts or {}  # Fonts dictionary
        self.colors = colors or {}  # Colors dictionary
        self.locations = locations or {}  # Screen locations dictionary

    def get_character_sheet_info(self):
        # Return a dictionary with information for rendering on the character sheet
        sheet_info = {
            "Name": {"value": self.name, "font": self.fonts.get("Name"), "color": self.colors.get("Name"),
                     "location": self.locations.get("Name")},
            "Stats": {},
        }

        # Include stats in the "Stats" section
        for stat_name, stat_value in self.stats.items():
            sheet_info["Stats"][stat_name] = {
                "value": stat_value,
                "font": self.fonts.get(stat_name),
                "color": self.colors.get(stat_name),
                "location": self.locations.get(stat_name),
            }

        return sheet_info


class CampaignData:
    def __init__(self):
        self.universe = 'AOA'
        self.name = 'Default Campaign'
        self.gm_name = 'GM'
        self.invited_players = ['player1']
        self.description = 'An example'
        self.technology_level = 0
        self.fantasy_level = 0