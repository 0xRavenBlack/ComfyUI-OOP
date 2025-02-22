import random

class OOPPoseNode:
    BASE_POSES = [
        "Sitting", "Stand", "Squat", "Grovel", "Lie", "Jump", "Run", "Walk", "Fly",
        "Head_tilt", "Looking_back", "Looking_down", "Looking_up", "Smelling", "Sleeping",
        "Bathing", "aiming_at_viewer", "stretching", "hands_on_hips", "breasts_rest_on_table",
        "hug_from_behind", "leaning_forward", "selfie"
    ]

    HAND_POSES = [
        "Hand_to_mouth", "Arm_at_side", "Arms_behind_head", "Arms_behind_back", "Hand_on_own_chest",
        "Arms_crossed", "Hand_on_hips", "Hand_on_hip", "Hands_up", "Stretch", "Armpits",
        "Leg_hold", "Grabbing", "Holding", "Fingersmile", "Hair_pull", "Hair_scrunchie",
        "Peace_symbol", "Salute", "Thumbs_up", "Middle_finger", "Cat_pose", "Finger_gun",
        "Waving", "Spread_arms"
    ]

    LEG_POSES = [
        "Spread_legs", "Crossed_legs", "Fetal_position", "Leg_lift", "Legs_up", "Leaning_forward",
        "Against_wall", "On_stomach", "Seiza", "Wariza-W-sitting", "Yokozuwari", "Indian_style",
        "Leg_hug", "Straddling", "Kneeling", "Arm_support", "feet_up", "one_knee",
        "standing_on_one_leg", "knees_up"
    ]


    def __init__(self):
        self.name = "Pose"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_pose": (cls.BASE_POSES, {"default": "Stand"}),
                "hand_pose": (cls.HAND_POSES, {"default": "Stretch"}),
                "leg_pose": (cls.LEG_POSES, {"default": "Against_wall"}),
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
