import random
from .oop_shared import NO_VALUE, format_pairs, random_value


class OOPClothingNode:
    UPPER_GARMENT_TYPES = [
        NO_VALUE, "Nude", "TShirt", "Sweater", "Jacket", "Shirt", "Blouse", "Hoodie",
        "Coat", "TankTop", "Vest", "Cardigan", "Poncho", "Kimono", "Polo",
        "ButtonDown", "CropTop", "Jumper", "Raincoat", "Parka"
    ]
    LOWER_GARMENT_TYPES = [
        NO_VALUE, "Nude", "Jeans", "Shorts", "Skirt", "Trousers", "Leggings", "Sweatpants",
        "Cargo Pants", "Chinos", "Dress", "Short Skirt", "Overalls", "Capri Pants",
        "Joggers", "Palazzo Pants", "Dungarees", "Culottes", "Mini Skirt", "Maxi Skirt"
    ]
    COLORS = [
        NO_VALUE, "Black", "White", "Gray", "Red", "Blue", "Green", "Yellow", "Pink", "Purple", "Brown", "Beige", "Orange"
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "upper_type": (cls.UPPER_GARMENT_TYPES, {"default": "Sweater"}),
                "lower_type": (cls.LOWER_GARMENT_TYPES, {"default": "Jeans"}),
            },
            "optional": {
                "upper_color": (cls.COLORS, {"default": NO_VALUE}),
                "lower_color": (cls.COLORS, {"default": NO_VALUE}),
                "randomize": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("OOP_CLOTHING",)
    FUNCTION = "generate_clothing"
    CATEGORY = "Object-Oriented Prompting"
    DESCRIPTION = "Clothing section of an object-oriented prompt: the top and bottom garment plus their colours. A blank option leaves that pair out of the prompt, and a Nude garment carries no colour."
    OUTPUT_TOOLTIPS = ("The clothing section, ready to link into OOP Person or OOP Node.",)

    def generate_clothing(self, upper_type, lower_type, upper_color=NO_VALUE, lower_color=NO_VALUE, randomize=False):
        if randomize:
            upper_type = random_value(self.UPPER_GARMENT_TYPES)
            lower_type = random_value(self.LOWER_GARMENT_TYPES)
            upper_color = random_value(self.COLORS)
            lower_color = random_value(self.COLORS)

        pairs = []
        for position, garment, color in (("top", upper_type, upper_color), ("bottom", lower_type, lower_color)):
            pairs.append((f"{position}_garment", garment))
            if garment.strip() and garment != "Nude":
                pairs.append((f"{position}_color", color))

        return (format_pairs(pairs),)

    @classmethod
    def IS_CHANGED(cls, upper_type, lower_type, upper_color, lower_color, randomize):
        if randomize:
            return random.getrandbits(32)  # Forces re-evaluation every time

NODE_CLASS_MAPPINGS = {
    "OOPClothingNode": OOPClothingNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPClothingNode": "OOP Clothing 🥼"
}
