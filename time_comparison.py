simu_file = open("log1.txt",'r')
exec_file = open("trace.txt",'r')

simu_lines = simu_file.readlines()
exec_lines = exec_file.readlines()[1:]

simu_dict = {}
exec_dict = {}

for line in simu_lines:
    line_members = line.split(" ")
    simu_dict[line_members[0]] = float(line_members[1])


for line in exec_lines:
    line_members = line.split('\t')
    time_units = line_members[8].split(' ')
    total_time = 0
    for unit in time_units:
        if ('m' in unit):
          total_time += float(unit[:-1]) * 60
        elif ('s' in unit):
          total_time += float(unit[:-1])
        
    exec_dict[line_members[1]] = total_time

result = []

not_present = 0
present = 0

total_diff = 0

f = open('missing_tasks.txt', 'w')

for key, value in exec_dict.items():
    if key in simu_dict.keys():
        result.append([key, value, simu_dict[key], value - simu_dict[key]])
        total_diff += (value - simu_dict[key])
        present += 1
    else:
        not_present += 1
        f.write(key + '\n')
        
print(total_diff)

print("amount of present keys is ", present)
print("amount of not present keys is ", not_present)