import random
from .oop_shared import NO_VALUE, format_pairs, random_value


class OOPAnimalNode:
    ANIMAL_TYPES = [
        NO_VALUE, "Horse", "Cat", "Dog", "Elephant", "Lion", "Tiger", "Bear", "Monkey",
        "Snake", "Giraffe", "Kangaroo", "Wolf", "Rabbit", "Zebra", "Cheetah",
        "Penguin", "Koala", "Panda", "Alligator", "Leopard", "Frog"
    ]

    COLORS = [
        NO_VALUE, "Black", "White", "Brown", "Golden", "Gray", "Spotted", "Striped", "Red",
        "Blue", "Green", "Yellow", "Orange", "Purple", "Pink", "Beige", "Silver",
        "Turquoise", "Lavender", "Teal"
    ]

    ACTIONS = [
        NO_VALUE, "Jumping", "Lying", "Running", "Sleeping", "Playing", "Eating", "Roaring",
        "Climbing", "Taunting", "Swimming", "Hiding", "Flying", "Chasing", "Barking",
        "Meowing", "Purring", "Galloping", "Howling", "Scratching", "Biting", "Sniffing"
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "animal_type": (cls.ANIMAL_TYPES, {"default": "Cat"}),
                "color": (cls.COLORS, {"default": "Black"}),
                "action": (cls.ACTIONS, {"default": "Lying"}),
            },
            "optional": {
                "randomize": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("OOP_ANIMAL",)
    FUNCTION = "generate_animal"
    CATEGORY = "Object-Oriented Prompting"
    DESCRIPTION = "Animal section of an object-oriented prompt: type, colour and action as key:value pairs. A blank option leaves that pair out of the prompt."
    OUTPUT_TOOLTIPS = ("The animal section, ready to link into OOP Node.",)

    def generate_animal(self, animal_type, color, action, randomize=False):
        if randomize:
            animal_type = random_value(self.ANIMAL_TYPES)
            color = random_value(self.COLORS)
            action = random_value(self.ACTIONS)
        return (format_pairs([("type", animal_type), ("color", color), ("action", action)]),)

    @classmethod
    def IS_CHANGED(cls, animal_type, color, action, randomize):
        if randomize:
            return random.getrandbits(32)  # Forces re-evaluation every time

NODE_CLASS_MAPPINGS = {
    "OOPAnimalNode": OOPAnimalNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPAnimalNode": "OOP Animal 🐾"
}
