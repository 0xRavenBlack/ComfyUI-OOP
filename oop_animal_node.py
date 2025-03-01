import random

class OOPAnimalNode:
    ANIMAL_TYPES = [
        "Horse", "Cat", "Dog", "Elephant", "Lion", "Tiger", "Bear", "Monkey", "Snake"
    ]

    COLORS = [
        "Black", "White", "Brown", "Golden", "Gray", "Spotted", "Striped", "Red"
    ]

    ACTIONS = [
        "Jumping", "Lying", "Running", "Sleeping", "Playing", "Eating", "Roaring", "Climbing", "Teasing"
    ]

    def __init__(self):
        self.name = "Animal"

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

    def generate_animal(self, animal_type, color, action, randomize=False):
        if randomize:
            animal_type = random.choice(self.ANIMAL_TYPES)
            color = random.choice(self.COLORS)
            action = random.choice(self.ACTIONS)
        return (f"type:{animal_type}, color: {color}, action:{action}",)

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
