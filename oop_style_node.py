from .oop_shared import NO_VALUE, format_pairs


class OOPStyleNode:
    STYLES = [
        NO_VALUE, "PhotoRAW", "Abstract", "BlackAndWhite", "Vintage", "Minimalist", "PopArt",
        "Watercolor", "OilPainting", "Sketch", "Cartoon", "Impressionist", "Surrealist", "Realistic",
        "Futuristic", "Cyberpunk", "Gothic", "Grunge", "FilmNoir", "ArtDeco", "Modernist", "Boho", "PaperCut",
        "Neon", "Retro", "Lomo", "PixelArt", "Glitch", "3DRendering", "HDR", "Fantasy", "StreetPhotography"
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_style": (cls.STYLES, {"default": "PhotoRAW"}),
            },
            "optional": {
                "second_style": (cls.STYLES, {"default": NO_VALUE}),
            }
        }

    RETURN_TYPES = ("OOP_STYLE",)
    FUNCTION = "generate_style"
    CATEGORY = "Object-Oriented Prompting"
    DESCRIPTION = "Style section of an object-oriented prompt: a base style and an optional second style. A blank option leaves that pair out of the prompt."
    OUTPUT_TOOLTIPS = ("The style section, ready to link into OOP Node.",)

    def generate_style(self, base_style, second_style=NO_VALUE):
        return (format_pairs([("base_style", base_style), ("second_style", second_style)]),)

NODE_CLASS_MAPPINGS = {
    "OOPStyleNode": OOPStyleNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPStyleNode": "OOP Style 🎨"
}
