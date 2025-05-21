import requests

def post_json(url, headers, json_data):
    """
    Post JSON data to a specified URL with headers.
    
    Args:
        url (str): The URL to post the data to.
        headers (dict): The headers to include in the request.
        json_data (dict): The JSON data to post.
    
    Returns:
        Response object or None if the request failed.
    """
    try:
        response = requests.post(url, headers=headers, json=json_data)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"HTTP POST failed: {e}")
        return None