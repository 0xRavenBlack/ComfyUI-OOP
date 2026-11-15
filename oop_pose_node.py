import random
from .oop_shared import NO_VALUE, format_pairs, random_value


class OOPPoseNode:
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
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_pose": (cls.BASE_POSES, {"default": "Stand"}),
                "hand_pose": (cls.HAND_POSES, {"default": "Stretch"}),
                "leg_pose": (cls.LEG_POSES, {"default": "AgainstWall"}),
            },
            "optional": {
                "randomize": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("OOP_POSE",)
    FUNCTION = "generate_pose"
    CATEGORY = "Object-Oriented Prompting"
    DESCRIPTION = "Pose section of an object-oriented prompt: body, hand and leg pose. A blank option leaves that pair out of the prompt."
    OUTPUT_TOOLTIPS = ("The pose section, ready to link into OOP Node.",)

    def generate_pose(self, base_pose, hand_pose, leg_pose, randomize=False):
        if randomize:
            base_pose = random_value(self.BASE_POSES)
            hand_pose = random_value(self.HAND_POSES)
            leg_pose = random_value(self.LEG_POSES)
        return (format_pairs([("body", base_pose), ("hands", hand_pose), ("legs", leg_pose)]),)

    @classmethod
    def IS_CHANGED(cls, base_pose, hand_pose, leg_pose, randomize):
        if randomize:
            return random.getrandbits(32)  # Forces re-evaluation every time

NODE_CLASS_MAPPINGS = {
    "OOPPoseNode": OOPPoseNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPPoseNode": "OOP Pose 🧍"
}
