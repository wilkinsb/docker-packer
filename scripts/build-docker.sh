#!/bin/bash

set -x
set -v -v -v -v
set -e # exit if any command fails

apt-get install -y python curl unzip


cd /tmp
curl -O https://releases.hashicorp.com/packer/1.0.3/packer_1.0.3_linux_amd64.zip
unzip packer_1.0.3_linux_amd64.zip
cp packer /usr/local/bin

cd /docker-packer
/usr/local/bin/packer build -machine-readable -only=master packer-template.json 2>&1 | tee build.out

curl https://bootstrap.pypa.io/get-pip.py | python

# pip install boto3 requests watchtower

# python post_processing.py