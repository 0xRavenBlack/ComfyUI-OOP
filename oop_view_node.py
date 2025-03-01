class OOPViewNode:
    # Predefined angle descriptions for consistency
    ANGLE_DESCRIPTIONS = ["Normal", "High", "Low"]
    # Predefined view types for consistency
    VIEW_TYPES = ["Closeup", "Portrait", "FullBody", "Landscape", "Panorama"]

    def __init__(self):
        self.name = "View"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "angle": (cls.ANGLE_DESCRIPTIONS, {"default": "Normal"}),
                "viewType": (cls.VIEW_TYPES, {"default": "Portrait"}),
                "backgroundBlur": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("OOP_VIEW",)
    FUNCTION = "generate_view"
    CATEGORY = "Object-Oriented Prompting"

    def generate_view(self, angle, viewType, backgroundBlur):
        # Determine background color based on the boolean flag
        background = "NoBlur"
        if backgroundBlur:
            background = "Blur"
        # Return a formatted string summarizing the view properties
        return (f"shot:{viewType}, angle:{angle}, background:{background}",)

    @classmethod
    def IS_CHANGED(cls, angle, viewType, backgroundBlur):
        # Simple hash function to signal a change when any parameter changes
        return hash((angle, viewType, backgroundBlur))


# Mapping the node class to a name key
NODE_CLASS_MAPPINGS = {
    "OOPViewNode": OOPViewNode
}

# A friendly display name for the node
NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPViewNode": "OOP View 📐"
}
