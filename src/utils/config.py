from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    aws_access_key_id: str = "placeholder"
    aws_secret_access_key: str = "placeholder"
    aws_default_region: str = "us-east-1"
    
    s3_bucket_name: str = "your-bucket"
    
    bedrock_embedding_model_id: str = "amazon.titan-embed-text-v1"
    bedrock_llm_model_id: str = "amazon.titan-text-express-v1"
    
    opensearch_endpoint: str = "https://placeholder"
    opensearch_index_name: str = "govmitra-rag-index"
    
    dynamodb_table_name: str = "govmitra-chat-history"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings():
    return Settings()
