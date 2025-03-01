import random

class OOPClothingNode:
    UPPER_GARMENT_TYPES = [
        "Nude", "TShirt", "Sweater", "Jacket", "Shirt", "Blouse", "Hoodie", "Coat", "TankTop", "Vest"
    ]
    LOWER_GARMENT_TYPES = [
        "Nude", "Jeans", "Shorts", "Skirt", "Trousers", "Leggings", "Sweatpants", "Cargo Pants", "Chinos", "Dress"
    ]
    COLORS = [
        " ", "Black", "White", "Gray", "Red", "Blue", "Green", "Yellow", "Pink", "Purple", "Brown", "Beige", "Orange"
    ]

    def __init__(self):
        self.name = "Clothing"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "upper_type": (cls.UPPER_GARMENT_TYPES, {"default": "Sweater"}),
                "lower_type": (cls.LOWER_GARMENT_TYPES, {"default": "Jeans"}),
            },
            "optional": {
                "upper_color": (cls.COLORS, {"default": " "}),
                "lower_color": (cls.COLORS, {"default": " "}),
                "randomize": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("OOP_CLOTHING",)
    FUNCTION = "generate_clothing"
    CATEGORY = "Object-Oriented Prompting"

    def generate_clothing(self, upper_type, lower_type, upper_color="Black", lower_color="Blue", randomize=False):
        if randomize:
            upper_type = random.choice(self.UPPER_GARMENT_TYPES)
            lower_type = random.choice(self.LOWER_GARMENT_TYPES)
            upper_color = random.choice(self.COLORS[1:])
            lower_color = random.choice(self.COLORS[1:])

        # Build garment details, excluding options set to " "
        upper_garment = f"Top::Garment:{upper_type}"
        if upper_color != " " and upper_type != "Nude":
            upper_garment += f", color:{upper_color}"

        lower_garment = f"Bottom::Garment:{lower_type}"
        if lower_color != " " and lower_type != "Nude":
            lower_garment += f", color:{lower_color}"

        return (f"{upper_garment}, {lower_garment}",)

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
