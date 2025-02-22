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
    MATERIALS = [
        " ", "Cotton", "Denim", "Leather", "Silk", "Wool", "Linen", "Polyester", "Nylon", "Suede", "Velvet"
    ]
    FITS = [
        " ", "Loose", "Regular", "Slim", "Skinny", "Oversized"
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
                "upper_material": (cls.MATERIALS, {"default": " "}),
                "upper_fit": (cls.FITS, {"default": " "}),
                "lower_color": (cls.COLORS, {"default": " "}),
                "lower_material": (cls.MATERIALS, {"default": " "}),
                "lower_fit": (cls.FITS, {"default": " "}),
                "randomize": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("OOP_CLOTHING",)
    FUNCTION = "generate_clothing"
    CATEGORY = "Object-Oriented Prompting"

    def generate_clothing(self, upper_type, lower_type, upper_color="Black", upper_material="Cotton", upper_fit="Regular",
                          lower_color="Blue", lower_material="Denim", lower_fit="Regular", randomize=False):
        if randomize:
            upper_type = random.choice(self.UPPER_GARMENT_TYPES)
            lower_type = random.choice(self.LOWER_GARMENT_TYPES)
            upper_color = random.choice(self.COLORS[1:])
            upper_material = random.choice(self.MATERIALS[1:])
            upper_fit = random.choice(self.FITS[1:])
            lower_color = random.choice(self.COLORS[1:])
            lower_material = random.choice(self.MATERIALS[1:])
            lower_fit = random.choice(self.FITS[1:])

        # Build garment details, excluding options set to " "
        upper_garment = f"UpperGarment({upper_type}"
        if upper_color != " ":
            upper_garment += f", color:{upper_color}"
        if upper_material != " ":
            upper_garment += f", material:{upper_material}"
        if upper_fit != " ":
            upper_garment += f", fit:{upper_fit}"
        upper_garment += ")"

        lower_garment = f"LowerGarment({lower_type}"
        if lower_color != " ":
            lower_garment += f", color:{lower_color}"
        if lower_material != " ":
            lower_garment += f", material:{lower_material}"
        if lower_fit != " ":
            lower_garment += f", fit:{lower_fit}"
        lower_garment += ")"

        return (f"{upper_garment}, {lower_garment}",)

    @classmethod
    def IS_CHANGED(cls, upper_type, lower_type, upper_color, upper_material, upper_fit,
                    lower_color, lower_material, lower_fit, randomize):
        if randomize:
            return random.getrandbits(32)  # Forces re-evaluation every time

NODE_CLASS_MAPPINGS = {
    "OOPClothingNode": OOPClothingNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPClothingNode": "OOP Clothing 🥼"
}
