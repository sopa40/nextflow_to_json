import json

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
result_json = []

N_INSTRUCTIONS = 8

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


def read_trace(trace_id):
    if trace_id in trace_dict.keys():
        trace_elements = trace_dict[trace_id].split("\t")
        return trace_elements[N_INSTRUCTIONS]



def process_in_out(in_out_file):
    for in_out_line in in_out_file:
        in_out_elements = in_out_line.split()
        task_info = dict()
        task_info["id"] = in_out_elements[ID_SCRIPT]
        task_info["name"] = in_out_elements[NAME_SCRIPT]

        # add info from Nextflow trace file
        task_info["numberOfInstructions"] = read_trace(task_info["id"])

        # populate input and output files
        task_info["inputFiles"] = []
        task_info["outputFiles"] = []
        for element in in_out_elements:
            if "input:" in element:
                input_info = element.split(":")
                in_dct = dict()
                in_dct["path"] = input_info[FILE_PATH]
                in_dct["size"] = input_info[FILE_SIZE]
                task_info["inputFiles"].append(in_dct)
            elif "output:" in element:
                output_info = element.split(":")
                out_dct = dict()
                out_dct["path"] = output_info[FILE_PATH]
                out_dct["size"] = output_info[FILE_SIZE]
                task_info["outputFiles"].append(out_dct)

        result_json.append(task_info)


def main():
    print("Starting JSON generation...")
    process_in_out(input_output_file)
    print("Writing to the file...")
    with open('output_local.json', 'w') as output:
        json.dump(result_json, output, indent=2)
    print("JSON is created!")

main()


