import random

class OOPHairNode:
    HAIR_COLORS = [
        " ", "Black", "Brown", "Blonde", "Red", "White", "Gray", "Blue", "Green", "Pink", "Purple", "Orange", "Yellow",
        "Teal", "Cyan", "Magenta", "Maroon", "Turquoise", "Lavender", "Beige", "Gold", "Silver", "Bronze", "Copper",
        "Indigo", "Violet", "Lilac", "Burgundy", "Olive", "Peach", "Coral", "Mint", "Azure", "Amber", "Charcoal",
        "Navy", "Sky Blue", "Lime", "Mustard", "Rose", "Periwinkle", "Salmon", "Emerald", "Sapphire", "Ruby", "Platinum"
    ]

    HAIR_STYLES = [
        "Short", "Long", "Curly", "Straight", "Wavy", "Bald", "Ponytail", "Braided", "Bun", "Spiky", "Undercut"
    ]

    def __init__(self):
        self.name = "Hair"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "style": (cls.HAIR_STYLES,),
                "main_color": (cls.HAIR_COLORS, {"default": "Black"}),
            },
            "optional": {
                "optional_color": (cls.HAIR_COLORS, {"default": " "}),
                "randomize": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("OOP_HAIR",)
    FUNCTION = "generate_hair"
    CATEGORY = "Object-Oriented Prompting"

    def generate_hair(self, main_color, style, optional_color="", randomize=False):
        if randomize:
            main_color = random.choice(self.HAIR_COLORS[1:])
            style = random.choice(self.HAIR_STYLES)
            optional_color = random.choice(self.HAIR_COLORS)

        return (f"color:{main_color}{optional_color.strip()}, style:{style}",)

    @classmethod
    def IS_CHANGED(cls, main_color, style, optional_color, randomize):
        if randomize:
            return random.getrandbits(32)  # Forces re-evaluation every time

NODE_CLASS_MAPPINGS = {
    "OOPHairNode": OOPHairNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPHairNode": "OOP Hair 🦰"
}
