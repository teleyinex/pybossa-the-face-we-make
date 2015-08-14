from task_run_tmpl import task_run
from random import choice
from random import random
from copy import copy, deepcopy
import json

def create_tr(i):
    gender = ["male", "female"]
    answers = ["Suprised :-O", "Smile :-)", "Grin :-D",
               "Angry :-@", "Tongue :-P", "Disappointed :-|",
               "Wink ;-)", "Sad :-(", "Cry :~(", "Kiss :-*"]

    tr = deepcopy(task_run)
    tr['id'] = int(tr['id']) + i
    tr['user_id'] = int(tr['id']) + i
    tr['info']['gender'] = choice(gender)
    for a in tr['info']['answers']:
        if random() > 0.5:
            a['user_answer'] = choice(answers)
        else:
            a['user_answer'] = a['correct_answer']
    return tr

task_runs = []
for i in range(30):
    task_runs.append(create_tr(i))

with open('task_runs.json', 'w') as f:
    f.write(json.dumps(task_runs))
