import random
from comfy_api.latest import io
from .oop_shared import NO_VALUE, format_pairs, random_value, OOP_EXPRESSION


class OOPExpressionNode(io.ComfyNode):
    EMOTIONS = [
        NO_VALUE, "Neutral", "Happy", "Sad", "Angry", "Surprised", "Fearful", "Disgusted", "Confident", "Shy", "Calm", "Excited", "Smirk", "Serious"
    ]
    INTENSITIES = [
        NO_VALUE, "Subtle", "Mild", "Strong"
    ]
    GAZE = [
        NO_VALUE, "AtViewer", "Away", "Up", "Down", "Side", "ClosedEyes"
    ]

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="OOPExpressionNode",
            display_name="OOP Expression 🙂",
            category="Object-Oriented Prompting",
            description="Expression section of an object-oriented prompt: emotion, intensity and gaze. A blank option leaves that pair out of the prompt.",
            inputs=[
                io.Combo.Input("emotion", options=cls.EMOTIONS, default="Neutral"),
                io.Combo.Input("intensity", options=cls.INTENSITIES, default="Mild"),
                io.Combo.Input("gaze", options=cls.GAZE, default="AtViewer"),
                io.Boolean.Input("randomize", default=False),
            ],
            outputs=[OOP_EXPRESSION.Output("expression", tooltip="The expression section, ready to link into OOP Person or OOP Node.")],
        )

    @classmethod
    def execute(cls, emotion, intensity, gaze, randomize=False) -> io.NodeOutput:
        if randomize:
            emotion = random_value(cls.EMOTIONS)
            intensity = random_value(cls.INTENSITIES)
            gaze = random_value(cls.GAZE)
        return io.NodeOutput(format_pairs([("emotion", emotion), ("intensity", intensity), ("gaze", gaze)]))

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        if kwargs.get("randomize"):
            return random.getrandbits(32)
