import random
from comfy_api.latest import io
from .oop_shared import NO_VALUE, format_pairs, random_value, OOP_ENVIRONMENT


class OOPEnvironmentNode(io.ComfyNode):
    DAY_TIMES = [
        NO_VALUE, "Morning", "Noon", "Afternoon", "Evening", "Night"
    ]

    MOODS = [
        NO_VALUE, "ClearNightSky", "SunDown", "CloudySky", "Sunny", "Rainy", "Stormy", "FullMoon", "HalfMoon"
    ]

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="OOPEnvironmentNode",
            display_name="OOP Environment ⛅",
            category="Object-Oriented Prompting",
            description="Environment section of an object-oriented prompt: time of day and the mood of the scene. A blank option leaves that pair out of the prompt.",
            inputs=[
                io.Combo.Input("day_time", options=cls.DAY_TIMES, default="Noon"),
                io.Combo.Input("mood", options=cls.MOODS, default="ClearNightSky"),
                io.Boolean.Input("randomize", default=False),
            ],
            outputs=[OOP_ENVIRONMENT.Output("environment", tooltip="The environment section, ready to link into OOP Node.")],
        )

    @classmethod
    def execute(cls, day_time, mood, randomize=False) -> io.NodeOutput:
        if randomize:
            day_time = random_value(cls.DAY_TIMES)
            mood = random_value(cls.MOODS)
        return io.NodeOutput(format_pairs([("time", day_time), ("mood", mood)]))

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        if kwargs.get("randomize"):
            return random.getrandbits(32)  # Forces re-evaluation every time
