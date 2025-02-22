import random

class OOPPoseNode:
    BASE_POSES = [
        "Sitting", "Stand", "Squat", "Grovel", "Lie", "Jump", "Run", "Walk", "Fly",
        "HeadTilt", "LookingBack", "LookingDown", "LookingUp", "Smelling", "Sleeping",
        "Bathing", "AimingAtViewer", "Stretching", "HandsOnHips", "BreastsRestOnTable",
        "HugFromBehind", "LeaningForward", "Selfie"
    ]

    HAND_POSES = [
        "HandToMouth", "ArmAtSide", "ArmsBehindHead", "ArmsBehindBack", "HandOnOwnChest",
        "ArmsCrossed", "HandOnHips", "HandOnHip", "HandsUp", "Stretch", "Armpits",
        "LegHold", "Grabbing", "Holding", "Fingersmile", "HairPull", "HairScrunchie",
        "PeaceSymbol", "Salute", "ThumbsUp", "MiddleFinger", "CatPose", "FingerGun",
        "Waving", "SpreadArms"
    ]

    LEG_POSES = [
        "SpreadLegs", "CrossedLegs", "FetalPosition", "LegLift", "LegsUp", "LeaningForward",
        "AgainstWall", "OnStomach", "Seiza", "WarizaWSitting", "Yokozuwari", "IndianStyle",
        "LegHug", "Straddling", "Kneeling", "ArmSupport", "FeetUp", "OneKnee",
        "StandingOnOneLeg", "KneesUp"
    ]


    def __init__(self):
        self.name = "Pose"

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

    def generate_pose(self, base_pose, hand_pose, leg_pose, randomize=False):
        if randomize:
            base_pose = random.choice(self.BASE_POSES)
            hand_pose = random.choice(self.HAND_POSES)
            leg_pose = random.choice(self.LEG_POSES)

        return (f"body:{base_pose}, hands:{hand_pose}, legs:{leg_pose}",)

    @classmethod
    def IS_CHANGED(cls, base_pose, hand_pose, leg_pose, randomize):
        if randomize:
            return random.getrandbits(32)  # Forces re-evaluation every time

NODE_CLASS_MAPPINGS = {
    "OOPPoseNode": OOPPoseNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPPoseNode": "OOP Poses 🧍"
}
