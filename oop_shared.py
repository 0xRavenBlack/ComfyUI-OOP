import random

# Shared prompt contract, not a node: every node module imports this instead of
# repeating the " " sentinel test and the key:value join.
NO_VALUE = " "
PROMPT_BULLET = "\n*  "


def random_value(pool):
    return random.choice([value for value in pool if value.strip()])


def format_pairs(pairs):
    return ", ".join(f"{key}:{value}" for key, value in pairs if value and value.strip())
