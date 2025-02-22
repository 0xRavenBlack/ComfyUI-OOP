class OOPStyleNode:
    STYLES = [
        " ",  "PhotoRAW", "Abstract", "BlackAndWhite", "Vintage", "Minimalist", "PopArt",
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
                "second_style": (cls.STYLES, {"default": " "}),
            }
        }

    RETURN_TYPES = ("OOP_STYLE",)
    FUNCTION = "generate_style"
    CATEGORY = "Object-Oriented Prompting"

    def generate_style(self, base_style, second_style=" "):
        # Start with the base style
        result = f"{base_style}"

        # Only add second_style if it is not " "
        if second_style != " ":
            result += f", {second_style}"

        return (result,)

NODE_CLASS_MAPPINGS = {
    "OOPStyleNode": OOPStyleNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPStyleNode": "OOP Style 🎨"
}
