import tkinter as tk


class SheetTab(tk.Frame):
    def __init__(self, master=None, rpg_system=None):
        super().__init__(master=master)
        self.rpg_system = rpg_system
        self.character_attributes = rpg_system.get_character_attributes()

        self.create_widgets()
        self.update_character_data()

    def create_widgets(self):
        # Create labels and entry fields dynamically based on character attributes
        for i, attribute in enumerate(self.character_attributes):
            tk.Label(self, text=f"{attribute}:").grid(row=i, column=0)
            tk.Entry(self, state='readonly').grid(row=i, column=1)

    def update_character_data(self):
        # Retrieve character data from the RPG system and update the sheet
        character_name = self.rpg_system.get_selected_character_name()
        character = self.rpg_system.get_character(character_name)

        if character:
            # Update entry fields with character data
            for i, attribute in enumerate(self.character_attributes):
                attribute_value = getattr(character, attribute, "")
                entry_widget = self.nametowidget(self.winfo_children()[i*2 + 1])  # Find the corresponding entry widget
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, str(attribute_value))
        else:
            # Handle the case where the character is not found
            print("Character not found.")
