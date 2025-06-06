import json

def encode_message(message: str) -> bytes:
    return json.dumps({"message": message}).encode('utf-8')

def decode_message(data: bytes) -> str:
    return json.loads(data.decode('utf-8'))["message"]