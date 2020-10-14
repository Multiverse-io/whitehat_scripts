#!/usr/bin/env python3

import boto3
import json

client = boto3.client('secretsmanager')
awsSecretsManagerApiResponse = client.get_secret_value(SecretId = 'users_with_keys_testing')
secretString = awsSecretsManagerApiResponse['SecretString']
users = json.loads(secretString)
#print(type(awsSecretsManagerApiResponse))
#print(type(secretString))

