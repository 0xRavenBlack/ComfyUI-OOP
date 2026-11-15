import hashlib
from comfy_api.latest import io
from .oop_shared import NO_VALUE, format_pairs, OOP_VIEW


class OOPViewNode(io.ComfyNode):
    ANGLE_DESCRIPTIONS = [
        NO_VALUE, "Normal", "High", "Low", "Upward", "Downward", "Side", "Tilted",
        "Diagonal", "EyeLevel", "Bird's Eye", "Worm's Eye", "Dutch Angle", "Overhead"
    ]
    VIEW_TYPES = [
        NO_VALUE, "Closeup", "Portrait", "FullBody", "Landscape", "Panorama", "WideAngle",
        "Macro", "MediumShot", "LongShot", "Establishing", "Aerial", "Profile",
        "ActionShot", "Over-the-Shoulder", "Extreme Closeup"
    ]

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="OOPViewNode",
            display_name="OOP View 📐",
            category="Object-Oriented Prompting",
            description="Camera section of an object-oriented prompt: shot type, angle and background blur. A blank option leaves that pair out of the prompt.",
            inputs=[
                io.Combo.Input("angle", options=cls.ANGLE_DESCRIPTIONS, default="Normal"),
                # camelCase kept: input names are the saved-graph contract
                io.Combo.Input("viewType", options=cls.VIEW_TYPES, default="Portrait"),
                io.Boolean.Input("backgroundBlur", default=False),
            ],
            outputs=[OOP_VIEW.Output("view", tooltip="The view section, ready to link into OOP Node.")],
        )

    @classmethod
    def execute(cls, angle, viewType, backgroundBlur) -> io.NodeOutput:
        return io.NodeOutput(format_pairs([("shot", viewType), ("angle", angle), ("background", "Blur" if backgroundBlur else "NoBlur")]))

    @classmethod
    def fingerprint_inputs(cls, angle, viewType, backgroundBlur):
        # Built-in hash() is salted per process (PYTHONHASHSEED): the cache would miss on every
        # server start and different views could collide, so fingerprint the inputs stably.
        fingerprint = f"{angle}|{viewType}|{backgroundBlur}".encode()
        return hashlib.sha256(fingerprint).hexdigest()
