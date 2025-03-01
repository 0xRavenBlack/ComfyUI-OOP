import random

class OOPPersonNode:
    GENDER = [
        "Female", "Male", "Androgynous"
    ]
    AGE_CATEGORIES = {
        (16, 19): "18-19Years",
        (20, 29): "20-29Years",
        (30, 39): "30-39Years",
        (40, 49): "40-49Years",
        (50, 59): "50-59Years",
        (60, 120): "60+Years"
    }
    BODY_SHAPES = [
            "Slim", "Athletic", "Average", "Curvy", "Chubby", "Hourglass", "Muscular"
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
                "age": ("INT", {"default": 25, "min": 18, "max": 120, "step": 1}),
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

    def get_age_category(self, age):
        for (min_age, max_age), category in self.AGE_CATEGORIES.items():
            if min_age <= age <= max_age:  # Ensure the age fits within the range
                return category
        return "unknown"  # For ages that don't fall into any category

    def generate_person(self, gender, age, body_shape, hair, eyes, ethnicity, mouth, poses, clothing, randomize):
        if randomize:
            age = random.randint(16, 99)
        age_category = self.get_age_category(age)
        details = [
                f"\n*  BodyShape: {body_shape}",
                f"*  Gender: {gender}",
                f"*  Age: {age_category}",
                f"*  Ethnicity: {ethnicity}"
            ]
        if hair.strip():
            details.append(f"*  Hair: {hair}")
        if eyes.strip():
            details.append(f"*  Eyes: {eyes}")
        if mouth.strip():
            details.append(f"*  Mouth: {mouth}")
        if clothing.strip():
            details.append(f"*  Clothes: {clothing}")
        if poses.strip():
            details.append(f"*  Poses: {poses}")
        return ("\n".join(details),)

NODE_CLASS_MAPPINGS = {
    "OOPPersonNode": OOPPersonNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPPersonNode": "OOP Person 👤"
}
