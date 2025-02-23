import random

class OOPLocationNode:
    PLACES = [
        "Forest", "City", "Desert", "Mountain", "Beach", "Cave", "Village", "Castle", "Temple", "SpaceStation", "Shop", "Club", "Bar"
    ]

    OBJECTS = [
        "Statue", "Tree", "Fountain", "Bridge", "Car", "House", "Bench", "Streetlamp", "Signpost", "Tower", "AdultToy", "Toy", "Laptop"
    ]

    def __init__(self):
        self.name = "Location"

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

    def generate_location(self, place, object, randomize=False):
        if randomize:
            place = random.choice(self.PLACES)
            object = random.choice(self.OBJECTS)

        return (f"location:{place}, object:{object}",)

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
