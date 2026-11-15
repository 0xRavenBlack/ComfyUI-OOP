import random
from comfy_api.latest import io
from .oop_shared import NO_VALUE, format_pairs, random_value, OOP_EYES


class OOPEyesNode(io.ComfyNode):
    EYE_SHAPES = [
        NO_VALUE, "Round", "Almond", "Hooded", "Monolid", "Upturned", "Downturned", "Oval", "Closed"
    ]
    EYE_COLORS = [
        NO_VALUE, "Blue", "Green", "Brown", "Hazel", "Gray", "Amber", "Violet"
    ]

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="OOPEyesNode",
            display_name="OOP Eyes 👀",
            category="Object-Oriented Prompting",
            description="Eye section of an object-oriented prompt: shape and colour. A blank option leaves that pair out of the prompt.",
            inputs=[
                io.Combo.Input("shape", options=cls.EYE_SHAPES, default="Round"),
                io.Combo.Input("color", options=cls.EYE_COLORS, default="Brown"),
                io.Boolean.Input("randomize", default=False),
            ],
            outputs=[OOP_EYES.Output("eyes", tooltip="The eye section, ready to link into OOP Person or OOP Node.")],
        )

    @classmethod
    def execute(cls, shape, color, randomize=False) -> io.NodeOutput:
        if randomize:
            shape = random_value(cls.EYE_SHAPES)
            color = random_value(cls.EYE_COLORS)
        return io.NodeOutput(format_pairs([("shape", shape), ("color", color)]))

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        if kwargs.get("randomize"):
            return random.getrandbits(32)  # Forces re-evaluation every time
