#!/bin/sh

# NOTE! Don't write anything to /tmp in this script.
# It somehow screws things up so that packer cannot remove the
# script from /tmp at the end, and so it won't write the image.

set -x
set -v -v -v -v
set -e # exit if any command fails

apt-get update
apt-get install -y git

cd /
echo $GITHUB_SSH_KEY | sed 's/NEWLINE/\n/g' > /home/ubuntu/.github_ssh_key
mv /home/ubuntu/.github_ssh_key /
chmod 0400 /.github_ssh_key

export GIT_SSH_COMMAND="ssh -i /.github_ssh_key -o StrictHostKeyChecking=no"


git clone git@github.com:bwilkins/docker-packer.git
cd docker-packer
git checkout staging


set -x
set -v -v -v -v
set -e # exit if any command fails


# apt-get update # not needed, already done
apt-get install -y openjdk-8-jdk-headless \
python libcurl4-openssl-dev libssl-dev vim curl \
build-essential python-dev

apt-get remove -y unattended-upgrades liblxc1 lxd-client lxcfs

curl https://bootstrap.pypa.io/get-pip.py | python

pip install -U pip setuptools

pip install virtualenv awscli ipython six


cd /


echo "python and java installed successfully"