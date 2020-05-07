#!/bin/sh

if [ ! -d data ]; then
    mkdir -p data
fi

python main.py
cd SchedJulia && git reset --hard
