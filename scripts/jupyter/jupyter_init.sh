#!/bin/bash

jupyter lab build --minimize False
jupyter notebook --generate-config -y
