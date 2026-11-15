import random
from comfy_api.latest import io

# Shared prompt contract, not a node: every node module imports this instead of
# repeating the " " sentinel test and the key:value join. The io.Custom types are
# the eleven bespoke connection types of the OOP DAG, defined once so leaf
# outputs, the person aggregator and the assembler agree on the same classes.
NO_VALUE = " "
PROMPT_BULLET = "\n*  "

OOP_HAIR = io.Custom("OOP_HAIR")
OOP_EYES = io.Custom("OOP_EYES")
OOP_MOUTH = io.Custom("OOP_MOUTH")
OOP_CLOTHING = io.Custom("OOP_CLOTHING")
OOP_POSE = io.Custom("OOP_POSE")
OOP_PERSON = io.Custom("OOP_PERSON")
OOP_STYLE = io.Custom("OOP_STYLE")
OOP_VIEW = io.Custom("OOP_VIEW")
OOP_LOCATION = io.Custom("OOP_LOCATION")
OOP_ANIMAL = io.Custom("OOP_ANIMAL")
OOP_ENVIRONMENT = io.Custom("OOP_ENVIRONMENT")


def random_value(pool):
    return random.choice([value for value in pool if value.strip()])


def format_pairs(pairs):
    return ", ".join(f"{key}:{value}" for key, value in pairs if value and value.strip())
