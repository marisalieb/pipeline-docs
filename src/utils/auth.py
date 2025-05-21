import requests # handles http requests

# Authentification request in python code
# Modified from:
# Copernicus SentinelHub Documentation. (n.d.). Authentication [online].
# [Accessed 20/02/2025]. Available from: https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Overview/Authentication.html 


def fetch_auth_token(client_id, client_secret):
    """
    Fetches an authentication token from the Copernicus API using client credentials.
    
    Args:
        client_id (str): The client ID for authentication.
        client_secret (str): The client secret for authentication.

    Returns:
        token (str): The access token if successful, None otherwise.
    """
    auth_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    # send http post request to auth_url with credentials
    response = requests.post(auth_url, data=auth_data)
    
    if response.status_code == 200: # 200 here means success, token received
        token = response.json().get("access_token") 
        return token
    else:
        print("error fetching token")
        return None


