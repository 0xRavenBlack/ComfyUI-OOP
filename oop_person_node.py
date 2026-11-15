import random
from comfy_api.latest import io
from .oop_shared import NO_VALUE, PROMPT_BULLET, random_value, OOP_HAIR, OOP_EYES, OOP_MOUTH, OOP_CLOTHING, OOP_POSE, OOP_PERSON


class OOPPersonNode(io.ComfyNode):
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
    def define_schema(cls):
        return io.Schema(
            node_id="OOPPersonNode",
            display_name="OOP Person 👤",
            category="Object-Oriented Prompting",
            description="Person block of an object-oriented prompt: age, body shape, ethnicity, gender, plus linked hair, eyes, mouth, clothing and pose sections. Blank options are left out.",
            inputs=[
                io.Int.Input("age", default=25, min=cls.AGE_MIN, max=cls.AGE_MAX, step=1),
                io.Combo.Input("body_shape", options=cls.BODY_SHAPES, default="Average"),
                io.Combo.Input("ethnicity", options=cls.ETHNICITIES, default="Asian"),
                io.Boolean.Input("randomize", default=False),
                io.Combo.Input("gender", options=cls.GENDER),
                OOP_HAIR.Input("hair", optional=True),
                OOP_EYES.Input("eyes", optional=True),
                OOP_MOUTH.Input("mouth", optional=True),
                OOP_CLOTHING.Input("clothing", optional=True),
                OOP_POSE.Input("poses", optional=True),
            ],
            outputs=[OOP_PERSON.Output("person", tooltip="The person block, ready to link into OOP Node.")],
        )

    @classmethod
    def get_age_category(cls, age):
        for min_age, max_age, category in cls.AGE_BUCKETS:
            if age <= max_age:
                return category
        return cls.AGE_BUCKETS[-1][2]

    @classmethod
    def build_person_details(cls, age, body_shape, ethnicity, randomize, gender):
        if randomize:
            min_age, max_age, _ = random.choice(cls.AGE_BUCKETS)
            age = random.randint(min_age, max_age)
        return [
            ("BodyShape", body_shape),
            ("Gender", gender),
            ("Age", cls.get_age_category(age)),
            ("Ethnicity", ethnicity),
        ]

    @classmethod
    def join_person_sections(cls, details):
        return "".join(f"{PROMPT_BULLET}{label}: {value}" for label, value in details if value and value.strip())

    @classmethod
    def execute(cls, age, body_shape, ethnicity, randomize, gender, hair=None, eyes=None, mouth=None, clothing=None, poses=None) -> io.NodeOutput:
        details = cls.build_person_details(age, body_shape, ethnicity, randomize, gender)
        details += [("Hair", hair), ("Eyes", eyes), ("Mouth", mouth), ("Clothes", clothing), ("Poses", poses)]
        return io.NodeOutput(cls.join_person_sections(details))

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        if kwargs.get("randomize"):
            return random.getrandbits(32)  # Forces re-evaluation every time
