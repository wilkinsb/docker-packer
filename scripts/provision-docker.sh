#!/bin/sh

# NOTE! Don't write anything to /tmp in this script.
# It somehow screws things up so that packer cannot remove the
# script from /tmp at the end, and so it won't write the image.

set -x
set -v -v -v -v
set -e # exit if any command fails

# apt-get update
# apt-get install -y git

# cd /


# set -x
# set -v -v -v -v
# set -e # exit if any command fails


# # apt-get update # not needed, already done
# apt-get install -y openjdk-8-jdk-headless \
# python libcurl4-openssl-dev libssl-dev vim curl \
# build-essential python-dev

# apt-get remove -y unattended-upgrades liblxc1 lxd-client lxcfs

# curl https://bootstrap.pypa.io/get-pip.py | python

# pip install -U pip setuptools

# pip install virtualenv awscli ipython six


cd /

echo $ECR_URI
echo $ECR_LOGIN_SERVER
echo $AWS_ACCESS_KEY
echo $AWS_SECRET_KEY


echo "python and java installed successfully"