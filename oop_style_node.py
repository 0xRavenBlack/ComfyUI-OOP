from comfy_api.latest import io
from .oop_shared import NO_VALUE, format_pairs, OOP_STYLE


class OOPStyleNode(io.ComfyNode):
    STYLES = [
        NO_VALUE, "PhotoRAW", "Abstract", "BlackAndWhite", "Vintage", "Minimalist", "PopArt",
        "Watercolor", "OilPainting", "Sketch", "Cartoon", "Impressionist", "Surrealist", "Realistic",
        "Futuristic", "Cyberpunk", "Gothic", "Grunge", "FilmNoir", "ArtDeco", "Modernist", "Boho", "PaperCut",
        "Neon", "Retro", "Lomo", "PixelArt", "Glitch", "3DRendering", "HDR", "Fantasy", "StreetPhotography"
    ]

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="OOPStyleNode",
            display_name="OOP Style 🎨",
            category="Object-Oriented Prompting",
            description="Style section of an object-oriented prompt: a base style and an optional second style. A blank option leaves that pair out of the prompt.",
            inputs=[
                io.Combo.Input("base_style", options=cls.STYLES, default="PhotoRAW"),
                io.Combo.Input("second_style", options=cls.STYLES, default=NO_VALUE),
            ],
            outputs=[OOP_STYLE.Output("style", tooltip="The style section, ready to link into OOP Node.")],
        )

    @classmethod
    def execute(cls, base_style, second_style=NO_VALUE) -> io.NodeOutput:
        return io.NodeOutput(format_pairs([("base_style", base_style), ("second_style", second_style)]))
