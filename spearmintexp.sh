#!/bin/bash

./spearmint --driver=local --method=GPEIOptChooser --method-args=noiseless=$1 -w --max-concurrent=$2 ./config.pb
