# Nextflow traces to json format converter

### This python script our traces after running nextflow job + additional information, which we get by running our script after finish nextflow execution, and creates JSON, which is later used for Simulation in WRENCH.

### To run:
  1. Extract traces 
  2. Specify a path to trace files inside of solution.py file (or just leave them in the same folder with solution.py file)
  3. Simply run the script with {$python3 solution.py}
  4. Results will be written to output_local.json (or you can specify path to the output file by yourself)


### Clean Up Input data
The `clean-file-paths.sh` script removes common file path prefixes, which will both reduce the filesize, but most importantly 
remove task dependent folder names, which would finding task dependencies by matching filenames impossible.

> ./clean-file-paths.sh in_out_files.txt

Creates the script_local.txt which is used by the python script