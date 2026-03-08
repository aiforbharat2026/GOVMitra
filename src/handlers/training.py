import json
from src.services.textract import extract_text_from_s3, get_job_results
from src.services.bedrock import get_embeddings_model
from src.services.opensearch import get_opensearch_client, create_index_if_not_exists
from src.utils.chunking import get_text_chunks
from src.utils.config import get_settings

settings = get_settings()

def handler(event, context):
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']
    
    # 1. Start text extraction
    job_id = extract_text_from_s3(s3_bucket, s3_key)
    
    # 2. Get full text (assumes polling and completion)
    full_text = get_job_results(job_id)
    
    # 3. Chunk text
    chunks = get_text_chunks(full_text)
    
    # 4. Generate embeddings and store in OpenSearch
    embeddings_model = get_embeddings_model()
    opensearch_client = get_opensearch_client()
    create_index_if_not_exists(opensearch_client, settings.opensearch_index_name)
    
    for i, chunk in enumerate(chunks):
        embedding = embeddings_model.embed_query(chunk)
        
        doc = {
            'text': chunk,
            'vector_field': embedding,
            'metadata': {
                'source': s3_key,
                'chunk_index': i
            }
        }
        
        opensearch_client.index(
            index=settings.opensearch_index_name,
            body=doc
        )
        
    return {
        'statusCode': 200,
        'body': json.dumps('Training pipeline completed successfully!')
    }
