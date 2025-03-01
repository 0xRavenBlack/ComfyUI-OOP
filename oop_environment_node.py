import random

class OOPEnvironmentNode:
    DAY_TIMES = [
        "Morning", "Noon", "Afternoon", "Evening", "Night"
    ]

    MOODS = [
        "ClearNightSky", "SunDown", "CloudySky", "Sunny", "Rainy", "Stormy", "FullMoon", "HalfMoon"
    ]

    def __init__(self):
        self.name = "Environment"

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

    def generate_environment(self, day_time, mood, randomize=False):
        if randomize:
            day_time = random.choice(self.DAY_TIMES)
            mood = random.choice(self.MOODS)

        return (f"time:{day_time}, mood:{mood}",)

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
