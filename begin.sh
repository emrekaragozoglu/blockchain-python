#!/bin/bash

# # To install pip2:
# wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
# python3 get-pip.py

# # removing the get-pip.py after installation of pip2
# rm -rf get-pip.py

# # To install virtualEnv for python2.7 with pip2
# pip3 install virtualenv

# # Then create and your vitualenv in your working folder
virtualenv -p python3 blockchain-py3

# # To activate your virtualenv
source blockchain-py3/bin/activate

# # To install all the necessary libraries in your virtualenv
yum install gmp-devel
yum install autoconf
yum install dh-autoreconf
pip3 install -r ./files/requirements.txt

# to correct the error in py2p library (specifically in base.py file)
# this error was causing all the nodes to disconnect if among one of the nodes fails ot disconnects (corrected by editing the base.py file)
# to realize the edit run:
sh ./files/correct_py2p_base_py.sh .files/base.py