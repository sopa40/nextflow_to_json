#!/bin/bash

cat $1 | sed 's/\/workdir\/work\/[a-z0-9]\{2\}\/[a-z0-9]\{30\}//g' | sed 's/\/data\/FORCE2NXF-Rangeland\/inputdata//g' | sed 's/\/tmp\/nxf\.[a-zA-Z0-9]\{10\}//g' > script_local.txt
echo "Created script_local.txt"
