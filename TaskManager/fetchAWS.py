import boto3
import json

def get_secret():
    secret_name = "OpenAIKey"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # [https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html](https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html)
        raise e

    # Parse the JSON-formatted string
    secret_json = json.loads(get_secret_value_response['SecretString'])
    secret_value = secret_json['OPENAI_API_KEY']  # Assuming the secret value is stored in a key named 'test'

    return secret_value

OPENAI_API_KEY = get_secret()