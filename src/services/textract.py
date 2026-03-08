import boto3
from src.utils.config import get_settings

settings = get_settings()

def get_textract_client():
    return boto3.client(
        service_name='textract',
        region_name=settings.aws_default_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key
    )

def extract_text_from_s3(bucket: str, key: str):
    client = get_textract_client()
    
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        }
    )
    
    job_id = response['JobId']
    
    return job_id

def get_job_results(job_id: str):
    client = get_textract_client()
    
    response = client.get_document_text_detection(JobId=job_id)
    
    # Needs polling mechanism for production
    pages = []
    while response['JobStatus'] == 'IN_PROGRESS':
        import time; time.sleep(1)
        response = client.get_document_text_detection(JobId=job_id)
        
    full_text = ""
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            full_text += item['Text'] + "\n"
            
    return full_text
