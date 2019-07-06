#!/bin/bash

touch fulllogs.json
jq -s '.[1] + { ((.[1]|length)|tostring) :.[0]}' newestlogs.json fulllogs.json > temp.json
mv temp.json fulllogs.json
