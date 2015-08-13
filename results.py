from enki import Enki
from pandas import *

e = Enki('api', 'http://localhost:5001', 'thefacewemake2')

e.get_tasks(json_file='tasks.json')
e.get_task_runs(json_file='task_runs.json')

task = e.tasks[0]

task_data = dict()

for photo in task.info['photos']:
    key = photo['photo_info']['photo']['id']
    task_data[key] = None

print task_data.keys()

d = dict()

def create_series(tr, photo_id):
    """Creates a series from a task_run object."""
    index = ['gender', 'user_answer', 'correct_answer', 'photo_id', 'url_b']
    data = [tr.info['gender']]
    for a in tr.info['answers']:
        _photo_id =  a['photo']['photo_info']['photo']['id']
        if _photo_id == photo_id:
            data.append(a['user_answer'])
            data.append(a['correct_answer'])
            data.append(a['photo']['photo_info']['photo']['id'])
            data.append(a['photo']['url_b'])
            break
    return Series(data, index)

photo_id = task_data.keys()[0]

for tr in e.task_runs[task.id]:
    d[tr.id] = create_series(tr, photo_id)


tmp = DataFrame(d)


### Gender histogram
print "################"
print "GENDER HISTOGRAM"
print "################"
print tmp.loc['gender'].value_counts()
print tmp.loc['photo_id'].value_counts()
### Correct answer
print "##############"
print "CORRECT ANSWER"
print "##############"
for photo in task.info['photos']:
    key = photo['photo_info']['photo']['id']
    if key == photo_id:
        value = photo['photo_info']['photo']['description']['_content'].split('\n\n')[0]
        print "Correct answer from task is: %s" % value
print "Correct answer from task_run is:"
print tmp.loc['correct_answer'].describe()
### Top answer from users
print "#############"
print "USERS ANSWER"
print "#############"
print tmp.loc['user_answer'].describe()
print tmp.loc['user_answer'].value_counts()
#

