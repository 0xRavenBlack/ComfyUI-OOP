import random

class OOPPersonNode:
    GENDER = [
        "Female", "Male", "NonBinary"
    ]
    AGE_CATEGORIES = {
            (16, 19): "Young",
            (20, 29): "YoungAdult",
            (30, 39): "Adult",
            (40, 49): "MidAdult",
            (50, 59): "SeniorAdult",
            (60, 120): "Elderly"
    }
    BODY_SHAPES = [
            "Slim", "Athletic", "Average", "Curvy", "Chubby", "Fat", "Hourglass", "Muscular"
    ]
    ETHNICITIES = [
        "African",
        "Asian",
        "Caucasian",
        "Latino",
        "Pacific",
        "Alien"
    ]
    def __init__(self):
        self.name = "Person"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "age": ("INT", {"default": 25, "min": 16, "max": 120, "step": 1}),
                "body_shape": (cls.BODY_SHAPES, {"default": "Average"}),
                "ethnicitie": (cls.ETHNICITIES, {"default": "Asian"}),
                "randomize": ("BOOLEAN", {"default": False}),
                "gender": (cls.GENDER,),
            },
            "optional": {
                "hair": ("OOP_HAIR", {"forceInput": True, "default": ""}),
                "eyes": ("OOP_EYES", {"forceInput": True, "default": ""}),
                "mouth": ("OOP_MOUTH", {"forceInput": True, "default": ""}),
                "clothing": ("OOP_CLOTHING", {"forceInput": True, "default": ""}),
                "poses": ("OOP_POSE", {"forceInput": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("OOP_PERSON",)
    FUNCTION = "generate_person"
    CATEGORY = "Object-Oriented Prompting"

    def get_age_category(self, age):
        for (min_age, max_age), category in self.AGE_CATEGORIES.items():
            if min_age <= age <= max_age:  # Ensure the age fits within the range
                return category
        return "unknown"  # For ages that don't fall into any category

    def generate_person(self, gender, age, body_shape, hair, eyes, ethnicitie, mouth, poses, clothing, randomize):
        if randomize:
            age = random.randint(16, 99)
        age_category = self.get_age_category(age)
        person_info = f" bodyShape:{body_shape}, gender:{gender}, age:{age_category}, ethnicitie:{ethnicitie}"
        if hair.strip():
            person_info += f", Hair({hair})"
        if eyes.strip():
            person_info += f", Eyes({eyes})"
        if eyes.strip():
            person_info += f", Mouth({mouth})"
        if eyes.strip():
            person_info += f", Clothes({clothing})"
        if poses.strip():
            person_info += f", Poses({poses})"
        return (person_info,)

NODE_CLASS_MAPPINGS = {
    "OOPPersonNode": OOPPersonNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPPersonNode": "OOP Person 👤"
}
