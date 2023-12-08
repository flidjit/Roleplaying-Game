"""
* ttk style
* all game rules including how characters interact.
* can include outside packages and modify
    the AOA window in many ways.
* builds the tab_section on the AOAWindow
* may add elements to the player's keyboard input.
"""


class TheSystem:
    name = "Ashes of Alexandria"
    directory_name = "AOARP"
    description = "A custom RP system."

    def __init__(self, aoa_window=None):
        self.aoa_window = aoa_window

    def update(self):
        pass

