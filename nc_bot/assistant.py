import requests

config = None


def query_assistant(url, prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": prompt,
    }
    response = requests.post(url+"/chat", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error querying assistant: {response.text}")
