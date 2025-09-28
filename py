.py com apoio do chat gpt - Open AI
---

# 📄 lambda_function.py

```python
import json
import boto3
from botocore.exceptions import ClientError

# Cliente S3
s3_client = boto3.client("s3")


def lambda_handler(event, context):
    """
    Função Lambda disparada por eventos do S3.
    Objetivo: registrar no CloudWatch informações sobre o arquivo enviado
    e retornar metadados do objeto.
    """
    try:
        # Extrair informações do evento
        record = event["Records"][0]
        bucket_name = record["s3"]["bucket"]["name"]
        object_key = record["s3"]["object"]["key"]
        file_size = record["s3"]["object"].get("size", 0)

        # Log da operação
        print(f"Novo arquivo recebido: {object_key} ({file_size} bytes) no bucket {bucket_name}")

        # Obter metadados
        metadata = get_object_metadata(bucket_name, object_key)
        print(f"Metadados do objeto: {metadata}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Processamento concluído com sucesso!",
                "bucket": bucket_name,
                "file": object_key,
                "size": file_size,
                "metadata": metadata
            })
        }

    except Exception as error:
        print(f"Erro no processamento: {error}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(error)})
        }


def get_object_metadata(bucket: str, key: str) -> dict:
    """
    Recupera os metadados de um objeto armazenado no S3.
    """
    try:
        response = s3_client.head_object(Bucket=bucket, Key=key)
        return response.get("Metadata", {})
    except ClientError as e:
        print(f"Erro ao obter metadados do objeto {key}: {e}")
        return {}
