import boto3
from langchain_aws import BedrockEmbeddings, BedrockLLM
from src.utils.config import get_settings

settings = get_settings()

def get_bedrock_client():
    return boto3.client(
        service_name='bedrock-runtime',
        region_name=settings.aws_default_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key
    )

def get_embeddings_model():
    return BedrockEmbeddings(
        client=get_bedrock_client(),
        model_id=settings.bedrock_embedding_model_id
    )

def get_llm():
    return BedrockLLM(
        client=get_bedrock_client(),
        model_id=settings.bedrock_llm_model_id
    )
