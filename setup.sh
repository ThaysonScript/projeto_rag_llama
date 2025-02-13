#!/usr/bin/env bash

python3 -m venv env

source env/bin/activate && wait

pip install pypdf