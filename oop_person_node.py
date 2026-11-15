import random
from .oop_shared import NO_VALUE, PROMPT_BULLET, random_value


class OOPPersonNode:
    GENDER = [
        NO_VALUE, "Female", "Male", "Androgynous"
    ]
    # Single source of truth: (min_age, max_age, label) drives the slider range, the classifier and the randomizer
    AGE_BUCKETS = [
        (18, 19, "18-19 Years"),
        (20, 29, "20-29 Years"),
        (30, 39, "30-39 Years"),
        (40, 49, "40-49 Years"),
        (50, 59, "50-59 Years"),
        (60, 120, "60+ Years")
    ]
    AGE_MIN = AGE_BUCKETS[0][0]
    AGE_MAX = AGE_BUCKETS[-1][1]
    BODY_SHAPES = [
        NO_VALUE, "Slim", "Athletic", "Average", "Curvy", "Chubby", "Hourglass", "Muscular"
    ]
    ETHNICITIES = [
        NO_VALUE, "African", "Asian", "Caucasian", "Latino", "Pacific", "Alien"
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "age": ("INT", {"default": 25, "min": cls.AGE_MIN, "max": cls.AGE_MAX, "step": 1}),
                "body_shape": (cls.BODY_SHAPES, {"default": "Average"}),
                "ethnicity": (cls.ETHNICITIES, {"default": "Asian"}),
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
    DESCRIPTION = "Person block of an object-oriented prompt: age, body shape, ethnicity, gender, plus linked hair, eyes, mouth, clothing and pose sections. Blank options are left out."
    OUTPUT_TOOLTIPS = ("The person block, ready to link into OOP Node.",)

    def get_age_category(self, age):
        for min_age, max_age, category in self.AGE_BUCKETS:
            if age <= max_age:
                return category
        return self.AGE_BUCKETS[-1][2]

    def build_person_details(self, age, body_shape, ethnicity, randomize, gender):
        if randomize:
            min_age, max_age, _ = random.choice(self.AGE_BUCKETS)
            age = random.randint(min_age, max_age)
        return [
            ("BodyShape", body_shape),
            ("Gender", gender),
            ("Age", self.get_age_category(age)),
            ("Ethnicity", ethnicity),
        ]

    def generate_person(self, age, body_shape, ethnicity, randomize, gender, hair="", eyes="", mouth="", clothing="", poses=""):
        details = self.build_person_details(age, body_shape, ethnicity, randomize, gender)
        details += [("Hair", hair), ("Eyes", eyes), ("Mouth", mouth), ("Clothes", clothing), ("Poses", poses)]
        return (self.join_person_sections(details),)

    def join_person_sections(self, details):
        return "".join(f"{PROMPT_BULLET}{label}: {value}" for label, value in details if value.strip())

    @classmethod
    def IS_CHANGED(cls, age, body_shape, ethnicity, randomize, gender, hair="", eyes="", mouth="", clothing="", poses=""):
        if randomize:
            return random.getrandbits(32)  # Forces re-evaluation every time

NODE_CLASS_MAPPINGS = {
    "OOPPersonNode": OOPPersonNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPPersonNode": "OOP Person 👤"
}
