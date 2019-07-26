#!/bin/bash

source venv/bin/activate

for i in {1..20}
  do
    echo "./spearmint --driver=local --method=GPEIOptChooser --method-args='noiseless=0, eistop=0.1, jobstop=6' -w --port=37035 --max-concurrent=1 ./config.pb" > command.txt
    ./spearmint --driver=local --method=GPEIOptChooser --method-args='noiseless=0, eistop=0.1, jobstop=6' -w --port=37035 --max-concurrent=1 ./config.pb
    python save_exp.py
    ./clearoutput
  done
