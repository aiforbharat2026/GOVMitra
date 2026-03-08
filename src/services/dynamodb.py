import boto3
from src.utils.config import get_settings

settings = get_settings()

def get_dynamodb_client():
    return boto3.resource(
        service_name='dynamodb',
        region_name=settings.aws_default_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key
    )

def store_chat_history(session_id: str, question: str, answer: str):
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table(settings.dynamodb_table_name)
    
    table.put_item(
        Item={
            'session_id': session_id,
            'question': question,
            'answer': answer
        }
    )
