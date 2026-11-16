import random
from comfy_api.latest import io
from .oop_shared import NO_VALUE, format_pairs, random_value, OOP_LIGHTING


class OOPLightingNode(io.ComfyNode):
    LIGHT_TYPES = [
        NO_VALUE, "Natural", "Studio", "Cinematic", "Soft", "Hard", "Dramatic", "Ambient", "Neon", "GoldenHour", "Backlit", "Rim", "Volumetric"
    ]
    DIRECTIONS = [
        NO_VALUE, "Front", "Side", "Top", "Back", "TopLeft", "TopRight", "Bottom", "ThreePoint"
    ]
    INTENSITIES = [
        NO_VALUE, "Dim", "Balanced", "Bright", "Harsh"
    ]

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="OOPLightingNode",
            display_name="OOP Lighting 💡",
            category="Object-Oriented Prompting",
            description="Lighting section of an object-oriented prompt: light type, direction and intensity. A blank option leaves that pair out of the prompt.",
            inputs=[
                io.Combo.Input("light_type", options=cls.LIGHT_TYPES, default="Natural"),
                io.Combo.Input("direction", options=cls.DIRECTIONS, default="Front"),
                io.Combo.Input("intensity", options=cls.INTENSITIES, default="Balanced"),
                io.Boolean.Input("randomize", default=False),
            ],
            outputs=[OOP_LIGHTING.Output("lighting", tooltip="The lighting section, ready to link into OOP Node.")],
        )

    @classmethod
    def execute(cls, light_type, direction, intensity, randomize=False) -> io.NodeOutput:
        if randomize:
            light_type = random_value(cls.LIGHT_TYPES)
            direction = random_value(cls.DIRECTIONS)
            intensity = random_value(cls.INTENSITIES)
        return io.NodeOutput(format_pairs([("type", light_type), ("direction", direction), ("intensity", intensity)]))

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        if kwargs.get("randomize"):
            return random.getrandbits(32)
