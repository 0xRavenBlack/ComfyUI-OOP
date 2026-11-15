import random
from comfy_api.latest import io
from .oop_shared import NO_VALUE, format_pairs, random_value, OOP_HAIR


class OOPHairNode(io.ComfyNode):
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
    def define_schema(cls):
        return io.Schema(
            node_id="OOPHairNode",
            display_name="OOP Hair 🦰",
            category="Object-Oriented Prompting",
            description="Hair section of an object-oriented prompt: one colour, or two colours separated by a space, plus the style. A blank option leaves that pair out of the prompt.",
            inputs=[
                io.Combo.Input("style", options=cls.HAIR_STYLES, default="Short"),
                io.Combo.Input("main_color", options=cls.HAIR_COLORS, default="Black"),
                io.Combo.Input("optional_color", options=cls.HAIR_COLORS, default=NO_VALUE),
                io.Boolean.Input("randomize", default=False),
            ],
            outputs=[OOP_HAIR.Output("hair", tooltip="The hair section, ready to link into OOP Person or OOP Node.")],
        )

    @classmethod
    def execute(cls, style, main_color, optional_color=NO_VALUE, randomize=False) -> io.NodeOutput:
        if randomize:
            main_color = random_value(cls.HAIR_COLORS)
            style = random_value(cls.HAIR_STYLES)
            optional_color = random_value(cls.HAIR_COLORS)
        color = f"{main_color} {optional_color.strip()}".strip()
        return io.NodeOutput(format_pairs([("color", color), ("style", style)]))

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        if kwargs.get("randomize"):
            return random.getrandbits(32)  # Forces re-evaluation every time
