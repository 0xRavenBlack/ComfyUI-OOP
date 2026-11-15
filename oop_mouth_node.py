import random
from .oop_shared import NO_VALUE, format_pairs, random_value


class OOPMouthNode:
    MOUTH_SHAPES = [
        NO_VALUE, "Round", "Wide", "Thin", "Full", "Heart", "Smile", "Frown", "Neutral",
        "Angled", "Downturned", "Oval", "Pointed", "Pout", "Curved", "Smirk",
        "Straight", "Upturned", "Chiseled", "Wide Smile", "Drooping"
    ]

    MOUTH_SIZES = [
        NO_VALUE, "Small", "Medium", "Large", "Tiny", "Huge", "Petite", "Gigantic"
    ]

    MOUTH_OPENINGS = [
        NO_VALUE, "Closed", "Slightly", "Wide", "Open", "Partially Open", "Fully Open",
        "Gaping", "Barely Open"
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "shape": (cls.MOUTH_SHAPES, {"default": "Neutral"}),
            },
            "optional": {
                "size": (cls.MOUTH_SIZES, {"default": NO_VALUE}),
                "opening": (cls.MOUTH_OPENINGS, {"default": NO_VALUE}),
                "randomize": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("OOP_MOUTH",)
    FUNCTION = "generate_mouth"
    CATEGORY = "Object-Oriented Prompting"
    DESCRIPTION = "Mouth section of an object-oriented prompt: shape, size and how open it is. A blank option leaves that pair out of the prompt."
    OUTPUT_TOOLTIPS = ("The mouth section, ready to link into OOP Node.",)

    def generate_mouth(self, shape, size=NO_VALUE, opening=NO_VALUE, randomize=False):
        if randomize:
            shape = random_value(self.MOUTH_SHAPES)
            size = random_value(self.MOUTH_SIZES)
            opening = random_value(self.MOUTH_OPENINGS)
        return (format_pairs([("shape", shape), ("size", size), ("opening", opening)]),)

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
