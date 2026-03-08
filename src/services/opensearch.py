from opensearchpy import OpenSearch, RequestsHttpConnection
from src.utils.config import get_settings

settings = get_settings()

def get_opensearch_client():
    auth = (settings.aws_access_key_id, settings.aws_secret_access_key)
    
    return OpenSearch(
        hosts=[{'host': settings.opensearch_endpoint, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

def create_index_if_not_exists(client: OpenSearch, index_name: str):
    if not client.indices.exists(index_name):
        settings_body = {
            "settings": {
                "index": {
                    "knp.index": True,
                    "knn.algo_parameter.ef_search": "512"
                }
            },
            "mappings": {
                "properties": {
                    "vector_field": {
                        "type": "knn_vector",
                        "dimension": 1536, # Amazon Titan Embeddings are 1536
                        "method": {
                            "name": "hnsw",
                            "space_type": "l2",
                            "engine": "nmslib",
                            "parameters": {
                                "ef_construction": 512,
                                "m": 16
                            }
                        }
                    },
                    "text": {"type": "text"},
                    "metadata": {"type": "object"}
                }
            }
        }
        client.indices.create(index=index_name, body=settings_body)
