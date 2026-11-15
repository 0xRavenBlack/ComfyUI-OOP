import random
from comfy_api.latest import io
from .oop_shared import NO_VALUE, format_pairs, random_value, OOP_MOUTH


class OOPMouthNode(io.ComfyNode):
    MOUTH_SHAPES = [
        NO_VALUE, "Round", "Wide", "Thin", "Full", "Heart", "Smile", "Frown", "Neutral",
        "Angled", "Downturned", "Oval", "Pointed", "Pout", "Curved", "Smirk",
        "Straight", "Upturned", "Chiseled", "Wide Smile", "Drooping"
    ]

    MOUTH_SIZES = [
        NO_VALUE, "Small", "Medium", "Large", "Tiny", "Huge", "Petite", "Gigantic"
    ]

    MOUTH_OPENINGS = [
        NO_VALUE, "Closed", "Slightly", "Wide", "Open", "Partially Open", "Fully Open",
        "Gaping", "Barely Open"
    ]

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="OOPMouthNode",
            display_name="OOP Mouth 👄",
            category="Object-Oriented Prompting",
            description="Mouth section of an object-oriented prompt: shape, size and how open it is. A blank option leaves that pair out of the prompt.",
            inputs=[
                io.Combo.Input("shape", options=cls.MOUTH_SHAPES, default="Neutral"),
                io.Combo.Input("size", options=cls.MOUTH_SIZES, default=NO_VALUE),
                io.Combo.Input("opening", options=cls.MOUTH_OPENINGS, default=NO_VALUE),
                io.Boolean.Input("randomize", default=False),
            ],
            outputs=[OOP_MOUTH.Output("mouth", tooltip="The mouth section, ready to link into OOP Node.")],
        )

    @classmethod
    def execute(cls, shape, size=NO_VALUE, opening=NO_VALUE, randomize=False) -> io.NodeOutput:
        if randomize:
            shape = random_value(cls.MOUTH_SHAPES)
            size = random_value(cls.MOUTH_SIZES)
            opening = random_value(cls.MOUTH_OPENINGS)
        return io.NodeOutput(format_pairs([("shape", shape), ("size", size), ("opening", opening)]))

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        if kwargs.get("randomize"):
            return random.getrandbits(32)  # Forces re-evaluation every time
