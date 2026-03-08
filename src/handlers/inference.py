import json
from src.services.bedrock import get_embeddings_model, get_llm
from src.services.opensearch import get_opensearch_client
from src.utils.config import get_settings

settings = get_settings()

def handler(event, context):
    user_question = event.get('question')
    
    # 1. Convert question into embedding
    embeddings_model = get_embeddings_model()
    question_embedding = embeddings_model.embed_query(user_question)
    
    # 2. Retrieve relevant document chunks from OpenSearch
    opensearch_client = get_opensearch_client()
    query = {
        'size': 5,
        'query': {
            'knn': {
                'vector_field': {
                    'vector': question_embedding,
                    'k': 5
                }
            }
        }
    }
    
    response = opensearch_client.search(
        index=settings.opensearch_index_name,
        body=query
    )
    
    hits = response['hits']['hits']
    retrieved_chunks = [hit['_source']['text'] for hit in hits]
    
    # 3. Combine context and question
    context_text = "\n\n".join(retrieved_chunks)
    prompt = f"Answer the user's question based ONLY on the context provided below.\n\nContext:\n{context_text}\n\nQuestion: {user_question}\n\nAnswer:"
    
    # 4. Generate final answer with LLM
    llm = get_llm()
    answer = llm.predict(prompt)
    
    # 5. Store conversation in DynamoDB (Stub)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'answer': answer,
            'source_documents': [hit['_source']['metadata']['source'] for hit in hits]
        })
    }
