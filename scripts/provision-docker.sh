#!/bin/sh

# NOTE! Don't write anything to /tmp in this script.
# It somehow screws things up so that packer cannot remove the
# script from /tmp at the end, and so it won't write the image.

set -x
set -v -v -v -v
set -e # exit if any command fails

sudo -s

sudo apt-get update
sudo apt-get install -y git
cd /
echo $GITHUB_SSH_KEY | sudo sed 's/NEWLINE/\n/g' > /home/ubuntu/.github_ssh_key
sudo mv /home/ubuntu/.github_ssh_key /
sudo chmod 0400 /.github_ssh_key

export GIT_SSH_COMMAND="ssh -i /.github_ssh_key -o StrictHostKeyChecking=no"


sudo -E git clone git@github.com:bwilkins/docker-packer.git
cd docker-packer


set -x
set -v -v -v -v
set -e # exit if any command fails


# apt-get update # not needed, already done
sudo apt-get install -y openjdk-8-jdk-headless \
python libcurl4-openssl-dev libssl-dev vim curl \
build-essential python-dev

sudo apt-get remove -y unattended-upgrades liblxc1 lxd-client lxcfs

curl https://bootstrap.pypa.io/get-pip.py | sudo python

sudo pip install -U pip setuptools

sudo pip install virtualenv awscli ipython six


cd /


echo "python and java installed successfully"