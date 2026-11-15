import random
from comfy_api.latest import io
from .oop_shared import NO_VALUE, format_pairs, random_value, OOP_ANIMAL


class OOPAnimalNode(io.ComfyNode):
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
    def define_schema(cls):
        return io.Schema(
            node_id="OOPAnimalNode",
            display_name="OOP Animal 🐾",
            category="Object-Oriented Prompting",
            description="Animal section of an object-oriented prompt: type, colour and action as key:value pairs. A blank option leaves that pair out of the prompt.",
            inputs=[
                io.Combo.Input("animal_type", options=cls.ANIMAL_TYPES, default="Cat"),
                io.Combo.Input("color", options=cls.COLORS, default="Black"),
                io.Combo.Input("action", options=cls.ACTIONS, default="Lying"),
                io.Boolean.Input("randomize", default=False),
            ],
            outputs=[OOP_ANIMAL.Output("animal", tooltip="The animal section, ready to link into OOP Node.")],
        )

    @classmethod
    def execute(cls, animal_type, color, action, randomize=False) -> io.NodeOutput:
        if randomize:
            animal_type = random_value(cls.ANIMAL_TYPES)
            color = random_value(cls.COLORS)
            action = random_value(cls.ACTIONS)
        return io.NodeOutput(format_pairs([("type", animal_type), ("color", color), ("action", action)]))

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        if kwargs.get("randomize"):
            return random.getrandbits(32)  # Forces re-evaluation every time
