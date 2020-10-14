#!/usr/bin/env python3

import boto3
import json
import os

client = boto3.client('secretsmanager')
awsSecretsManagerApiResponse = client.get_secret_value(SecretId = 'users_with_keys_testing')
secretString = awsSecretsManagerApiResponse['SecretString']
users = json.loads(secretString)
#print(type(awsSecretsManagerApiResponse))
#print(type(secretString))
for user, key in users.items():
    print(f'Creating user {user}')

    bash="""
    sudo useradd -m $user_name -s /bin/bash

    # Set the password to 'password'
    echo $user_name:password | sudo chpasswd

    # Set up the users .ssh folder and add their public key
    sudo su - $user_name -c 'mkdir -p .ssh'
    sudo su - $user_name -c 'chmod 700 .ssh/'
    sudo su - $user_name -c "echo ${user_key} > .ssh/authorized_keys"
    sudo su - $user_name -c 'chmod 600 .ssh/authorized_keys'

    # Put the user in the sudo or wheel group
    if grep -q sudo /etc/group; then
      sudo usermod -a -G sudo $user_name
    else
      if grep -q wheel /etc/group; then
        sudo usermod -a -G wheel $user_name
      fi
    fi

    # Allow user to sudo
    echo "$user_name    ALL=(ALL:ALL) ALL" | sudo EDITOR='tee -a' visudo
    echo "OMG"
    # Expire the users password which forces a change on next login (password is only required to use sudo, login is done with the public key)
    sudo chage -d 0 $user_name
  else
    sudo su - $user_name -c "echo ${user_key} > .ssh/authorized_keys"
  fi
    """
#    # Put the user in the sudo or wheel group
#    if grep -q sudo /etc/group; then
#      sudo usermod -a -G sudo $user_name
#    else
#      if grep -q wheel /etc/group; then
#        sudo usermod -a -G wheel $user_name
#      fi
#    fi
#
#    # Allow user to sudo
#    echo "$user_name    ALL=(ALL:ALL) ALL" | sudo EDITOR='tee -a' visudo
#
#    # Expire the users password which forces a change on next login (password is only required to use sudo, login is done with the public key)
#    sudo chage -d 0 $user_name
#  else
#    sudo su - $user_name -c "echo ${user_key} > .ssh/authorized_keys"
#  fi

