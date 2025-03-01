import random

class OOPMouthNode:
    MOUTH_SHAPES = [
        "Round", "Wide", "Thin", "Full", "Heart", "Smile", "Frown", "Neutral",
        "Angled", "Downturned", "Oval", "Pointed", "Pout", "Curved", "Smirk",
        "Straight", "Upturned", "Chiseled", "Wide Smile", "Drooping"
    ]

    MOUTH_SIZES = [
        " ", "Small", "Medium", "Large", "Tiny", "Huge", "Petite", "Gigantic"
    ]

    MOUTH_OPENINGS = [
        " ", "Closed", "Slightly", "Wide", "Open", "Partially Open", "Fully Open",
        "Gaping", "Barely Open"
    ]

    def __init__(self):
        self.name = "Mouth"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "shape": (cls.MOUTH_SHAPES, {"default": "Neutral"}),
            },
            "optional": {
                "size": (cls.MOUTH_SIZES, {"default": " "}),
                "opening": (cls.MOUTH_OPENINGS, {"default": " "}),
                "randomize": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("OOP_MOUTH",)
    FUNCTION = "generate_mouth"
    CATEGORY = "Object-Oriented Prompting"

    def generate_mouth(self, shape, size="Medium", opening="Closed", randomize=False):
        if randomize:
            shape = random.choice(self.MOUTH_SHAPES)
            size = random.choice(self.MOUTH_SIZES[1:])
            opening = random.choice(self.MOUTH_OPENINGS[1:])

        # Build the return string
        result = f"shape:{shape}"

        # Only add size and opening if they are not " "
        if size != " ":
            result += f", size:{size}"
        if opening != " ":
            result += f", opened:{opening}"

        return (result,)

    @classmethod
    def IS_CHANGED(cls, shape, size, opening, randomize):
        if randomize:
            return random.getrandbits(32)  # Forces re-evaluation every time

NODE_CLASS_MAPPINGS = {
    "OOPMouthNode": OOPMouthNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPMouthNode": "OOP Mouth 👄"
}
