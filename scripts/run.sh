#!/bin/bash

first_time_flg=/tmp/first_time_flg

if [ ! -e $first_time_flg ]; then
    echo "First time setup"
    touch $first_time_flg

    for file in scripts/**/*
    do
        sh $file
    done
    echo "......Done."
fi

jupyter lab --allow-root --ip 0.0.0.0 --port ${PORT}
