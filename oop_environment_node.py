import random
from .oop_shared import NO_VALUE, format_pairs, random_value


class OOPEnvironmentNode:
    DAY_TIMES = [
        NO_VALUE, "Morning", "Noon", "Afternoon", "Evening", "Night"
    ]

    MOODS = [
        NO_VALUE, "ClearNightSky", "SunDown", "CloudySky", "Sunny", "Rainy", "Stormy", "FullMoon", "HalfMoon"
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "day_time": (cls.DAY_TIMES, {"default": "Noon"}),
                "mood": (cls.MOODS, {"default": "ClearNightSky"}),
            },
            "optional": {
                "randomize": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("OOP_ENVIRONMENT",)
    FUNCTION = "generate_environment"
    CATEGORY = "Object-Oriented Prompting"
    DESCRIPTION = "Environment section of an object-oriented prompt: time of day and the mood of the scene. A blank option leaves that pair out of the prompt."
    OUTPUT_TOOLTIPS = ("The environment section, ready to link into OOP Node.",)

    def generate_environment(self, day_time, mood, randomize=False):
        if randomize:
            day_time = random_value(self.DAY_TIMES)
            mood = random_value(self.MOODS)
        return (format_pairs([("time", day_time), ("mood", mood)]),)

    @classmethod
    def IS_CHANGED(cls, day_time, mood, randomize):
        if randomize:
            return random.getrandbits(32)  # Forces re-evaluation every time

NODE_CLASS_MAPPINGS = {
    "OOPEnvironmentNode": OOPEnvironmentNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPEnvironmentNode": "OOP Environment ⛅"
}
