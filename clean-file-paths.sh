#!/bin/bash

cat $1 | grep /tmp/nxf
cat $1 | sed 's/\/workdir//g' | sed 's/\/data\/FORCE2NXF-Rangeland\/inputdata//g' > script_local.txt
echo "Created script_local.txt"
