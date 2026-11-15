import random
from comfy_api.latest import io
from .oop_shared import NO_VALUE, format_pairs, random_value, OOP_CLOTHING


class OOPClothingNode(io.ComfyNode):
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
    def define_schema(cls):
        return io.Schema(
            node_id="OOPClothingNode",
            display_name="OOP Clothing 🥼",
            category="Object-Oriented Prompting",
            description="Clothing section of an object-oriented prompt: the top and bottom garment plus their colours. A blank option leaves that pair out of the prompt, and a Nude garment carries no colour.",
            inputs=[
                io.Combo.Input("upper_type", options=cls.UPPER_GARMENT_TYPES, default="Sweater"),
                io.Combo.Input("lower_type", options=cls.LOWER_GARMENT_TYPES, default="Jeans"),
                io.Combo.Input("upper_color", options=cls.COLORS, default=NO_VALUE),
                io.Combo.Input("lower_color", options=cls.COLORS, default=NO_VALUE),
                io.Boolean.Input("randomize", default=False),
            ],
            outputs=[OOP_CLOTHING.Output("clothing", tooltip="The clothing section, ready to link into OOP Person or OOP Node.")],
        )

    @classmethod
    def execute(cls, upper_type, lower_type, upper_color=NO_VALUE, lower_color=NO_VALUE, randomize=False) -> io.NodeOutput:
        if randomize:
            upper_type = random_value(cls.UPPER_GARMENT_TYPES)
            lower_type = random_value(cls.LOWER_GARMENT_TYPES)
            upper_color = random_value(cls.COLORS)
            lower_color = random_value(cls.COLORS)

        pairs = []
        for position, garment, color in (("top", upper_type, upper_color), ("bottom", lower_type, lower_color)):
            pairs.append((f"{position}_garment", garment))
            if garment.strip() and garment != "Nude":
                pairs.append((f"{position}_color", color))

        return io.NodeOutput(format_pairs(pairs))

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        if kwargs.get("randomize"):
            return random.getrandbits(32)  # Forces re-evaluation every time
