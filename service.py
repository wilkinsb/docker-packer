import logging
import os

import boto3

import local_settings as conf

def get_user_data():
    """Get user data"""
    output = f"""#!/bin/bash

set -e # exit after any error
set -x # see which commands are being run and their output

# terminate self after 230 minutes- safety precaution
echo "sudo halt" | at now + 230 minutes

export GH_ACCESS_TOKEN="{os.getenv("GH_ACCESS_TOKEN")}"
export ECR_LOGIN_SERVER="{os.getenv("ECR_LOGIN_SERVER")}"
export ECR_URI="{os.getenv("ECR_URI")}"


echo $ECR_LOGIN_SERVER

apt-get update
apt-get install -y git docker.io

sudo systemctl start docker
sudo systemctl enable docker

echo $docker --version


git clone https://{os.getenv("GH_ACCESS_TOKEN")}:@github.com/wilkinsb/docker-packer.git
cd docker-packer

cd scripts

./build-docker.sh
"""

    return output


def find_image():
    """
    Finds the latest Canonical Ubuntu 16.04 AMI and return the ID.
    based on
    https://gist.github.com/robert-mcdermott/a9901aaafe208a6eb76e0fc3b9fc47c9
    """
    ec2 = boto3.resource('ec2', region_name=os.getenv("AWS_REGION"))
    images = ec2.images.filter(
        Owners=['099720109477'],
        Filters=[
            {'Name': 'name', 'Values': [
                'ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*']},
            {'Name': 'state', 'Values': ['available']},
            {'Name': 'architecture', 'Values': ['x86_64']},
            {'Name': 'root-device-type', 'Values': ['ebs']},
            {'Name': 'virtualization-type', 'Values': ['hvm']}
        ]
    )
    candidates = {}
    for image in images:
        candidates[image.creation_date] = image.image_id
    cdate = sorted(candidates.keys(), reverse=True)[0]
    ami = candidates[cdate]
    return ami

def trigger_build(event, context):
    """
    Both web and S3 events will eventually call this.
    """
    ec2_client = boto3.client("ec2", region_name=os.getenv("AWS_REGION"))

    arn = os.getenv("EC2_ARN")
    response = ec2_client.run_instances(
        ImageId=find_image(),
        MinCount=1,
        MaxCount=1,
        KeyName=os.getenv("SSH_KEYNAME"),
        SecurityGroupIds=[os.getenv("SEC_GROUP_ID")],
        InstanceType="t2.micro",
        IamInstanceProfile={"Arn": arn},
        InstanceInitiatedShutdownBehavior="terminate",
        TagSpecifications=[
            {"ResourceType": "instance", "Tags": [{"Key": "Name", "Value": "DockerPacker"}]}
        ],
        UserData=get_user_data(),
    )
    instance_id = response["Instances"][0]["ImageId"]
    return instance_id

