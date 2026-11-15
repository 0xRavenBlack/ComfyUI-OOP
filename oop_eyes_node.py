import random
from .oop_shared import NO_VALUE, format_pairs, random_value


class OOPEyesNode:
    EYE_SHAPES = [
        NO_VALUE, "Round", "Almond", "Hooded", "Monolid", "Upturned", "Downturned", "Oval", "Closed"
    ]
    EYE_COLORS = [
        NO_VALUE, "Blue", "Green", "Brown", "Hazel", "Gray", "Amber", "Violet"
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "shape": (cls.EYE_SHAPES, {"default": "Round"}),
                "color": (cls.EYE_COLORS, {"default": "Brown"}),
            },
            "optional": {
                "randomize": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("OOP_EYES",)
    FUNCTION = "generate_eyes"
    CATEGORY = "Object-Oriented Prompting"
    DESCRIPTION = "Eye section of an object-oriented prompt: shape and colour. A blank option leaves that pair out of the prompt."
    OUTPUT_TOOLTIPS = ("The eye section, ready to link into OOP Person or OOP Node.",)

    def generate_eyes(self, shape, color, randomize=False):
        if randomize:
            shape = random_value(self.EYE_SHAPES)
            color = random_value(self.EYE_COLORS)
        return (format_pairs([("shape", shape), ("color", color)]),)

    @classmethod
    def IS_CHANGED(cls, shape, color, randomize):
        if randomize:
            return random.getrandbits(32)  # Forces re-evaluation every time

NODE_CLASS_MAPPINGS = {
    "OOPEyesNode": OOPEyesNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPEyesNode": "OOP Eyes 👀"
}
