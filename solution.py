import json
import math
from model import Task, Dependency

# input data: {taskname} input:{input_name}:{input_size} output:{output_name}:{output_size}

# output data: json, with
# {
#     "name": "task_1",
#     "numberOfInstructions": 123412341235,
#     "numberOfCores": 1,
#     "amdahlAlpha": 1,
#     "memoryRequirement": 1000000,
#     "inputFiles": [
#       {
#         "path": "bigfile",
#         "size": 20000000000
#       }
#     ],
#     "outputFiles": [
#       {
#         "path": "smallfile",
#         "size": 20000
#       }
#     ]
#   }


# resulting json file for each element, which is appended to the file each iteration

TASK_NAME = 1
N_INSTRUCTIONS = 7
N_CYCLES = 8
AVERAGE_CPU_USAGE = 9

ID_SCRIPT = 0
NAME_SCRIPT = 1

FILE_PATH = 1
FILE_SIZE = 2

# Nextflow traces
with open('trace_local.txt') as trace:
    trace_lns = trace.readlines()
    trace_lns = trace_lns[1:]
    # ignore first row, hash is key and rest of the string is dict for each row
    trace_dict = dict(line.split("\t", 2)[1:] for line in trace_lns)

# Script result file in the Nextflow directory after run
with open('script_local.txt') as script:
    input_output_file = script.readlines()


def read_trace(trace_id, index):
    if trace_id in trace_dict.keys():
        trace_elements = trace_dict[trace_id].split("\t")
        return trace_elements[index]


def process_in_out(in_out_file):
    outputs = {}
    tasks = []
    for in_out_line in in_out_file:
        in_out_elements = in_out_line.split()
        hash_id = in_out_elements[ID_SCRIPT]
        cpu_usage = float(read_trace(hash_id, AVERAGE_CPU_USAGE).replace('%', '')) / 100

        task = Task(
            hash_id,
            read_trace(hash_id, TASK_NAME),
            int(read_trace(hash_id, N_CYCLES)),
            10_000,
            cpu_usage,
            math.ceil(cpu_usage)
        )
        tasks.append(task)

        for element in in_out_elements:
            if "input:" in element:

                input_info = element.split(":")
                path = input_info[FILE_PATH]
                size = int(input_info[FILE_SIZE])

                # in case the file was produced by a predecessor it will be present in the outputs hashmap
                if path in outputs:
                    dependency = outputs[path]
                    # we register a new consumer for the dependency
                    dependency.insert_consumer(id, path, size)
                else:
                    # otherwise we create a 'Dangling' dependency which will later be an input file for the simulation
                    # TODO: check if the path references the 'inputdata' directory
                    dependency = Dependency(id, path, size, False)

                task.add_input(dependency)

            elif "output:" in element:
                output_info = element.split(":")
                path = output_info[FILE_PATH]
                size = int(output_info[FILE_SIZE])

                # If the file was already an output of a different task we register it as an additional producer,
                # this is the exact case why we need a more complex model of dependencies between task, in order to
                # resolve dependencies with multiple producers
                if path in outputs:
                    dependency = outputs[path]
                    dependency.insert_producer(id, path, size)
                else:
                    # If this is the first occurrence we create a new non 'dangling' dependency and register it in the
                    # hashmap
                    dependency = Dependency(id, path, size, True)
                    outputs[path] = dependency
                print(dependency.file_path)
                task.add_output(dependency)

    return [task.to_json() for task in tasks]


def main():
    print("Starting JSON generation...")
    result_json = process_in_out(input_output_file)
    print("Writing to the file...")
    with open('output_local.json', 'w') as output:
        json.dump(result_json, output, indent=2)
    print("JSON is created!")


main()
