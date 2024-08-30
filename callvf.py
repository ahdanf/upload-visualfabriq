import hashlib
import hmac
import base64
import requests
import json
from config import s_shared_key, s_path_to_file, s_key_label, s_url

def get_signature_for_file(path_to_file, shared_key):
    with open(path_to_file, "rb") as f:
        file_bytes = f.read()
        signature_obj = hmac.new(
            shared_key.encode("utf-8"),
            msg=file_bytes,
            digestmod=hashlib.sha256,
        )
    return signature_obj.hexdigest(), file_bytes

def send_post_request(url, path_to_file, shared_key, key_label):
    signature, file_bytes = get_signature_for_file(path_to_file, shared_key)
    
    file_content_base64 = base64.b64encode(file_bytes).decode('utf-8')
    
    headers = {
        "X-VF-Signature": signature,
        "Content-Type": "application/json"
    }
    
    body = {
        "path": "test_id_folder",
        "file_name": path_to_file.split('/')[-1],
        "file_content": file_content_base64,
        "key_label": key_label
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(body))
    return response

if __name__ == '__main__':
    path_to_file = s_path_to_file
    shared_key = s_shared_key
    key_label = s_key_label 
    url = s_url
    
    response = send_post_request(url, path_to_file, shared_key, key_label)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content}")
