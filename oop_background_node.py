import random
from comfy_api.latest import io
from .oop_shared import NO_VALUE, format_pairs, random_value, OOP_BACKGROUND


class OOPBackgroundNode(io.ComfyNode):
    SETTINGS = [
        NO_VALUE, "Indoor", "Outdoor", "Studio", "Urban", "Nature", "Fantasy", "SciFi", "Abstract", "Underwater", "Space"
    ]
    DETAILS = [
        NO_VALUE, "Plain", "Bokeh", "Crowd", "Architecture", "Forest", "Mountains", "Ocean", "Skyline", "Ruins", "Garden", "Interior"
    ]
    COLORS = [
        NO_VALUE, "Neutral", "Warm", "Cool", "Dark", "Bright", "Pastel", "Monochrome"
    ]

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="OOPBackgroundNode",
            display_name="OOP Background 🖼️",
            category="Object-Oriented Prompting",
            description="Background section of an object-oriented prompt: setting, detail and colour mood. A blank option leaves that pair out of the prompt.",
            inputs=[
                io.Combo.Input("setting", options=cls.SETTINGS, default="Outdoor"),
                io.Combo.Input("detail", options=cls.DETAILS, default="Plain"),
                io.Combo.Input("color_mood", options=cls.COLORS, default="Neutral"),
                io.Boolean.Input("randomize", default=False),
            ],
            outputs=[OOP_BACKGROUND.Output("background", tooltip="The background section, ready to link into OOP Node.")],
        )

    @classmethod
    def execute(cls, setting, detail, color_mood, randomize=False) -> io.NodeOutput:
        if randomize:
            setting = random_value(cls.SETTINGS)
            detail = random_value(cls.DETAILS)
            color_mood = random_value(cls.COLORS)
        return io.NodeOutput(format_pairs([("setting", setting), ("detail", detail), ("color_mood", color_mood)]))

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        if kwargs.get("randomize"):
            return random.getrandbits(32)
