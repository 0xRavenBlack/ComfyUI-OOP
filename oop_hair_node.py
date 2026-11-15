import random
from .oop_shared import NO_VALUE, format_pairs, random_value


class OOPHairNode:
    HAIR_COLORS = [
        NO_VALUE, "Black", "Brown", "Blonde", "Red", "White", "Gray", "Blue", "Green", "Pink", "Purple", "Orange", "Yellow",
        "Teal", "Cyan", "Magenta", "Maroon", "Turquoise", "Lavender", "Beige", "Gold", "Silver", "Bronze", "Copper",
        "Indigo", "Violet", "Lilac", "Burgundy", "Olive", "Peach", "Coral", "Mint", "Azure", "Amber", "Charcoal",
        "Navy", "Sky Blue", "Lime", "Mustard", "Rose", "Periwinkle", "Salmon", "Emerald", "Sapphire", "Ruby", "Platinum"
    ]

    HAIR_STYLES = [
        NO_VALUE, "Short", "Long", "Curly", "Straight", "Wavy", "Bald", "Ponytail", "Braided", "Bun", "Spiky", "Undercut"
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "style": (cls.HAIR_STYLES, {"default": "Short"}),
                "main_color": (cls.HAIR_COLORS, {"default": "Black"}),
            },
            "optional": {
                "optional_color": (cls.HAIR_COLORS, {"default": NO_VALUE}),
                "randomize": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("OOP_HAIR",)
    FUNCTION = "generate_hair"
    CATEGORY = "Object-Oriented Prompting"
    DESCRIPTION = "Hair section of an object-oriented prompt: one colour, or two colours separated by a space, plus the style. A blank option leaves that pair out of the prompt."
    OUTPUT_TOOLTIPS = ("The hair section, ready to link into OOP Person or OOP Node.",)

    def generate_hair(self, style, main_color, optional_color=NO_VALUE, randomize=False):
        if randomize:
            main_color = random_value(self.HAIR_COLORS)
            style = random_value(self.HAIR_STYLES)
            optional_color = random_value(self.HAIR_COLORS)
        color = f"{main_color} {optional_color.strip()}".strip()
        return (format_pairs([("color", color), ("style", style)]),)

    @classmethod
    def IS_CHANGED(cls, style, main_color, optional_color, randomize):
        if randomize:
            return random.getrandbits(32)  # Forces re-evaluation every time

NODE_CLASS_MAPPINGS = {
    "OOPHairNode": OOPHairNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPHairNode": "OOP Hair 🦰"
}
