import json

with open('workflow.json') as f:
    json_data = json.load(f)

json_tasks = list(t_id.get('id') for t_id in json_data)

exec_file = open("trace.txt",'r')
exec_lines = exec_file.readlines()[1:]
exec_tasks = []

for line in exec_lines:
    line_members = line.split('\t')
    exec_tasks.append(line_members[1])
   
task_dif = len(exec_tasks) - len(json_tasks)

if task_dif:
    out = open('missing_ids.txt', 'w')
    print("Missing", task_dif, "task ids. Writing missing hashes to missing_ids.txt")
    miss_id_list = list(missing_tasks for missing_tasks in exec_tasks if missing_tasks not in json_tasks)
    out.write('\n'.join(miss_id_list))