from version2.toolkit import InputHandler


class PlayerData:
    def __init__(self):
        self.name = 'Player Name'
        self.email = 'thisone@there.com'
        self.ui_config = {}
        self.key_map = {}
        self.key_config = []


class ThePlayer:
    def __init__(self, aoa_window=None):
        self.data = PlayerData()
        self.is_gm = False
        self.current_universe = 'AOA'
        self.current_campaign = 'Beginner Campaign'
        self.current_character = 'Character Name'
        self.pc_party = {}
        self.cooldowns = {}
        self.aoa_window = aoa_window  # Set aoa_window as an instance variable
        self.initialize()

    def initialize(self):
        self.configure_keys()

    def update(self):
        for i in self.cooldowns:
            if self.cooldowns[i] >= 0:
                self.cooldowns[i] -= 1
        InputHandler.get_input(self.aoa_window)

    def configure_keys(self):
        k = self.data.key_config
        for i in range(len(k)):
            self.data.key_map[k[i][1]] = False
            self.aoa_window.accept(k[i][0], self.update_key_map, [k[i][1], True])
            self.aoa_window.accept(k[i][0] + '-up', self.update_key_map, [k[i][1], True])

    def update_key_map(self, control_name, control_state):
        self.data.key_map[control_name] = control_state

