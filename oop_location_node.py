import random
from comfy_api.latest import io
from .oop_shared import NO_VALUE, format_pairs, random_value, OOP_LOCATION


class OOPLocationNode(io.ComfyNode):
    PLACES = [
        NO_VALUE, "Forest", "City", "Desert", "Mountain", "Beach", "Cave", "Village",
        "Castle", "Temple", "SpaceStation", "Shop", "Club", "Bar", "Office",
        "BedRoom", "Kitchen", "Park", "Library", "Airport", "Hotel", "Factory",
        "Garden", "Street", "Museum", "Warehouse", "Zoo", "Hospital", "Bridge",
        "Courtyard", "Restaurant", "AmusementPark", "Submarine", "Lighthouse"
    ]

    OBJECTS = [
        NO_VALUE, "Statue", "Tree", "Fountain", "Bridge", "Car", "House", "Bench",
        "Streetlamp", "Signpost", "Tower", "TeddyBear", "Toy", "Laptop",
        "CookingUtensils", "Doll", "Chair", "Book", "Computer", "Cup",
        "Lamp", "Piano", "Clock", "Guitar", "Sofa", "Desk", "Fridge",
        "Television", "Microwave", "WashingMachine", "Toothbrush", "Rug"
    ]

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="OOPLocationNode",
            display_name="OOP Location 🌍",
            category="Object-Oriented Prompting",
            description="Scene section of an object-oriented prompt: the place and the object inside it. A blank option leaves that pair out of the prompt.",
            inputs=[
                io.Combo.Input("place", options=cls.PLACES, default="City"),
                io.Combo.Input("object", options=cls.OBJECTS, default="Statue"),
                io.Boolean.Input("randomize", default=False),
            ],
            outputs=[OOP_LOCATION.Output("location", tooltip="The location section, ready to link into OOP Node.")],
        )

    # "object" is the socket name: ComfyUI calls nodes by keyword, so renaming it
    # would break every saved workflow.
    @classmethod
    def execute(cls, place, object, randomize=False) -> io.NodeOutput:
        if randomize:
            place = random_value(cls.PLACES)
            object = random_value(cls.OBJECTS)
        return io.NodeOutput(format_pairs([("location", place), ("object", object)]))

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        if kwargs.get("randomize"):
            return random.getrandbits(32)  # Forces re-evaluation every time
