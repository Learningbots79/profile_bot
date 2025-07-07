import requests

def shortern_url(long_url: str) -> str:
    try:
        api = "https://api.tinyurl.com/create"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer Your_APi_key" # optional
        }
        payload = {
            "url": long_url
        }

        response = requests.post(api, json=payload, headers=headers)
        if response.status_code == 201:
            return response.json()["data"]["tiny_url"]
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"Faild: {e}"