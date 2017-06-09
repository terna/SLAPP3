#!/bin/bash

# see
# https://linuxconfig.org/bash-scripting-tutorial#h8-2-read-file-into-bash-array



exec < ./userNames.txt

while read LINE; do

    ./addSLAPP_toUser.sh $LINE

done
