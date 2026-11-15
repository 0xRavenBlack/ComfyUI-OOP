import random
from .oop_shared import NO_VALUE, format_pairs, random_value


class OOPLocationNode:
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
    def INPUT_TYPES(cls):
        return {
            "required": {
                "place": (cls.PLACES, {"default": "City"}),
                "object": (cls.OBJECTS, {"default": "Statue"}),
            },
            "optional": {
                "randomize": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("OOP_LOCATION",)
    FUNCTION = "generate_location"
    CATEGORY = "Object-Oriented Prompting"
    DESCRIPTION = "Scene section of an object-oriented prompt: the place and the object inside it. A blank option leaves that pair out of the prompt."
    OUTPUT_TOOLTIPS = ("The location section, ready to link into OOP Node.",)

    # "object" is the socket name: ComfyUI calls nodes by keyword, so renaming it
    # would break every saved workflow.
    def generate_location(self, place, object, randomize=False):
        if randomize:
            place = random_value(self.PLACES)
            object = random_value(self.OBJECTS)
        return (format_pairs([("location", place), ("object", object)]),)

    @classmethod
    def IS_CHANGED(cls, place, object, randomize):
        if randomize:
            return random.getrandbits(32)  # Forces re-evaluation every time

NODE_CLASS_MAPPINGS = {
    "OOPLocationNode": OOPLocationNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPLocationNode": "OOP Location 🌍"
}
