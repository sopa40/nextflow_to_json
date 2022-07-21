# This class represents an n-to-m dependency between tasks.
# On one side we have producers who will create the file at a path on the other we have consumers who depend on the file
# When analyzing nextflow execution we noticed files appearing as outputs for multiple tasks, this behavior is not
# supported by wrench. We use a Class to generate unique, yet matching file names for such cases.
# The Following case is not supported by wrench and needs to be resolved
# Task_01: output:file.a:2000
# Task_02: output:file.a:4000
# Task_11: input: file.a:4000

# The current implementation will generate the following:
# Task_01: output:file.a0:2000
# Task_02: output:file.a1:4000
# Task_11: input: file.a1:4000

# We need to investigate if we may resolve in other ways for example:
# Task_01: output:file.a0:2000
# Task_02: output:file.a1:4000
# Task_11: input:file.a0:2000 input:file.a1:4000
class Dependency:

    def reset_print_counter(self):
        self.internal_producer_counter = 0

    def to_producer_json(self):
        json = {
            "path": self.file_path,
            "size": list(self.file_sizes)[0]
        }

        return json

    def to_consumer_json(self):
        json = {
            "path": self.file_path,
            "size": list(self.file_sizes)[0]
        }

        return [json]

    def __init__(self, hash_id, path, size, producer):
        self.internal_producer_counter = 0
        self.file_path = path
        self.file_sizes = [size]
        self.parent_ids = []
        self.children_ids = []

        if producer:
            self.parent_ids.append(hash_id)
        else:
            self.children_ids.append(hash_id)

    def insert_producer(self, hash_id, path, size):
        assert(path == self.file_path)
        self.file_sizes.append(size)
        self.parent_ids.append(hash_id)

    def insert_consumer(self, hash_id, path, size):
        assert(path == self.file_path)
        self.file_sizes.append(size)
        self.children_ids.append(hash_id)


class Task:
    def __init__(self, hash_id, name, n_instructions, memory_requirement, average_cpu_usage, n_cores):
        self.children = []
        self.parents = []
        self.hash_id = hash_id
        self.name = name
        self.n_instructions = n_instructions
        self.memory_requirement = memory_requirement
        self.average_cpu_usage = average_cpu_usage
        self.n_cores = n_cores

    def add_output(self, dependency):
        self.children.append(dependency)

    def add_input(self, dependency):
        self.parents.append(dependency)

    def to_json(self):
        print("%s has %d dependent tasks" % (self.name, len(self.children)))
        return {
            "id": self.hash_id,
            "name": self.name,
            "memoryRequirement": self.memory_requirement,
            "numberOfInstructions": self.n_instructions,
            "averageCpuUsage": self.average_cpu_usage,
            "numberOfCores": self.n_cores,
            "inputFiles": [input for parent in self.parents for input in parent.to_consumer_json() ],
            "outputFiles": [child.to_producer_json() for child in self.children]
        }
