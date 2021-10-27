#!/bin/sh
cd
cd ros_ws/src/exp_robotics_ass1_4949035/
python setup.py bdist_wheel
pip3 install dist/mylibrary-0.1.1-py3-none-any.whl --upgrade

