import json
import random

with open("data.json", "r") as file:
    data = json.load(file)
    
random_interaction = random.choice(data["predicates"]["too_hard"]["base"])
a = type(random_interaction)
print(a, random_interaction)

