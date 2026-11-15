import random
from comfy_api.latest import io
from .oop_shared import NO_VALUE, format_pairs, random_value, OOP_POSE


class OOPPoseNode(io.ComfyNode):
    BASE_POSES = [
        NO_VALUE, "Sitting", "Stand", "Squat", "Groove", "Lie", "Jump", "Run", "Walk", "Fly",
        "HeadTilt", "LookingBack", "LookingDown", "LookingUp", "Smelling", "Sleeping",
        "Bathing", "AimingAtViewer", "Stretching", "HandsOnHips", "BreastsRestOnTable",
        "HugFromBehind", "LeaningForward", "Selfie"
    ]

    HAND_POSES = [
        NO_VALUE, "HandToMouth", "ArmAtSide", "ArmsBehindHead", "ArmsBehindBack", "HandOnOwnChest",
        "ArmsCrossed", "HandOnHips", "HandOnHip", "HandsUp", "Stretch", "Armpits",
        "LegHold", "Grabbing", "Holding", "Fingersmile", "HairPull", "HairScrunchie",
        "PeaceSymbol", "Salute", "ThumbsUp", "MiddleFinger", "CatPose", "FingerGun",
        "Waving", "SpreadArms"
    ]

    LEG_POSES = [
        NO_VALUE, "SpreadLegs", "CrossedLegs", "FetalPosition", "LegLift", "LegsUp", "LeaningForward",
        "AgainstWall", "OnStomach", "Seiza", "Wariza", "Yokozuwari", "IndianStyle",
        "LegHug", "Straddling", "Kneeling", "ArmSupport", "FeetUp", "OneKnee",
        "StandingOnOneLeg", "KneesUp"
    ]

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="OOPPoseNode",
            display_name="OOP Pose 🧍",
            category="Object-Oriented Prompting",
            description="Pose section of an object-oriented prompt: body, hand and leg pose. A blank option leaves that pair out of the prompt.",
            inputs=[
                io.Combo.Input("base_pose", options=cls.BASE_POSES, default="Stand"),
                io.Combo.Input("hand_pose", options=cls.HAND_POSES, default="Stretch"),
                io.Combo.Input("leg_pose", options=cls.LEG_POSES, default="AgainstWall"),
                io.Boolean.Input("randomize", default=False),
            ],
            outputs=[OOP_POSE.Output("pose", tooltip="The pose section, ready to link into OOP Node.")],
        )

    @classmethod
    def execute(cls, base_pose, hand_pose, leg_pose, randomize=False) -> io.NodeOutput:
        if randomize:
            base_pose = random_value(cls.BASE_POSES)
            hand_pose = random_value(cls.HAND_POSES)
            leg_pose = random_value(cls.LEG_POSES)
        return io.NodeOutput(format_pairs([("body", base_pose), ("hands", hand_pose), ("legs", leg_pose)]))

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        if kwargs.get("randomize"):
            return random.getrandbits(32)  # Forces re-evaluation every time
