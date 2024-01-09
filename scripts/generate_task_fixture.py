import json
from faker import Faker
from datetime import timedelta
import random

fake = Faker()

examples = []
for i in range(1, 51):
    task = {
        "model": "core.task",
        "pk": i,
        "fields": {
            "name": fake.word(),
            "description": fake.text(),
            "estimated": str(timedelta(minutes=random.randint(30, 240))),
            "state": random.choice(["planned", "completed", "in_progress"])
        }
    }
    examples.append(task)

# Guardar los ejemplos en un archivo JSON
with open("task_fixture.json", "w") as json_file:
    json.dump(examples, json_file, indent=2)

print("Fixture generado con éxito.")
