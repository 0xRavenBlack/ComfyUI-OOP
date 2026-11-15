import hashlib
from .oop_shared import NO_VALUE, format_pairs


class OOPViewNode:
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
    def INPUT_TYPES(cls):
        return {
            "required": {
                "angle": (cls.ANGLE_DESCRIPTIONS, {"default": "Normal"}),
                # camelCase kept: input names are the saved-graph contract
                "viewType": (cls.VIEW_TYPES, {"default": "Portrait"}),
                "backgroundBlur": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("OOP_VIEW",)
    FUNCTION = "generate_view"
    CATEGORY = "Object-Oriented Prompting"
    DESCRIPTION = "Camera section of an object-oriented prompt: shot type, angle and background blur. A blank option leaves that pair out of the prompt."
    OUTPUT_TOOLTIPS = ("The view section, ready to link into OOP Node.",)

    def generate_view(self, angle, viewType, backgroundBlur):
        return (format_pairs([("shot", viewType), ("angle", angle), ("background", "Blur" if backgroundBlur else "NoBlur")]),)

    @classmethod
    def IS_CHANGED(cls, angle, viewType, backgroundBlur):
        # Built-in hash() is salted per process (PYTHONHASHSEED): the cache would miss on every
        # server start and different views could collide, so fingerprint the inputs stably.
        fingerprint = f"{angle}|{viewType}|{backgroundBlur}".encode()
        return hashlib.sha256(fingerprint).hexdigest()


NODE_CLASS_MAPPINGS = {
    "OOPViewNode": OOPViewNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPViewNode": "OOP View 📐"
}
