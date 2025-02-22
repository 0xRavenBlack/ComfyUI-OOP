class OOPStyleNode:
    STYLES = [
        " ",  "Photo_RAW", "Abstract", "Black_and_White", "Vintage", "Minimalist", "Pop_Art",
        "Watercolor", "Oil_Painting", "Sketch", "Cartoon", "Impressionist", "Surrealist", "Realistic",
        "Futuristic", "Cyberpunk", "Gothic", "Grunge", "Film_Noir", "Art_Deco", "Modernist", "Boho", "Paper_cut",
        "Neon", "Retro", "Lomo", "Pixel_Art", "Glitch", "3D_Rendering", "HDR", "Fantasy", "Street_Photography"
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_style": (cls.STYLES, {"default": "Photo_RAW"}),
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
