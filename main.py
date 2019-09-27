import logging
import os

import boto3

import local_settings as conf

def get_user_data():
    """Get user data"""
    output = """#!/bin/bash

set -e # exit after any error
set -x # see which commands are being run and their output

# terminate self after 230 minutes- safety precaution
echo "sudo halt" | at now + 230 minutes

export GITHUB_SSH_KEY="{}"
apt-get update
apt-get install -y git

cd /
echo $GITHUB_SSH_KEY | sed 's/NEWLINE/\\n/g' > /.github_ssh_key
chmod 0400 .github_ssh_key

export GIT_SSH_COMMAND="ssh -i /.github_ssh_key -o StrictHostKeyChecking=no"

git clone git@github.com:sciscogenetics/docker-packer.git
cd docker-packer/scripts

./build-docker.sh

    """.format(conf.GITHUB_SSH_KEY)

    return output


def trigger_build():
    """
    Both web and S3 events will eventually call this.
    """
    ec2_client = boto3.client("ec2", region_name=conf.AWS_REGION)

    arn = conf.EC2_ARN
    response = ec2_client.run_instances(
        # ImageId=find_image("us-west-2"),
        MinCount=1,
        MaxCount=1,
        KeyName=conf.SSH_KEYNAME,
        SecurityGroupIds=[conf.SEC_GROUP_ID],
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


if __name__ == "__main__":
    trigger_build()
