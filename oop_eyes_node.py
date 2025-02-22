import random

class OOPEyesNode:
    EYE_SHAPES = [
        "Round", "Almond", "Hooded", "Monolid", "Upturned", "Downturned", "Oval", "Closed"
    ]
    EYE_COLORS = [
        "Blue", "Green", "Brown", "Hazel", "Gray", "Amber", "Violet"
    ]

    def __init__(self):
        self.name = "Eyes"
        self.randomize = False
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

    def generate_eyes(self, shape, color, randomize=False):
        if randomize:
            shape = random.choice(self.EYE_SHAPES)
            color = random.choice(self.EYE_COLORS)
        return (f"shape:{shape}, color:{color}",)

    @classmethod
    def IS_CHANGED(cls, shape, color, randomize=False):
        if randomize:
            return random.getrandbits(32)  # Forces re-evaluation every time

NODE_CLASS_MAPPINGS = {
    "OOPEyesNode": OOPEyesNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPEyesNode": "OOP Eyes 👀"
}
