from utils.auth import fetch_auth_token
from utils.post_json import post_json
from utils.bbox import get_bbox_from_json

class DataFetcher:
    """Base class for any Copernicus data fetcher."""
    PROCESS_URL = "https://sh.dataspace.copernicus.eu/api/v1/process"

    def __init__(self, client_id, client_secret, coord_json_path, out_path):
        """
        Initialize the data fetcher.

        Args:
            client_id (str): Copernicus client ID.
            client_secret (str): Copernicus client secret.
            coord_json_path (str): Path to the JSON file containing coordinates.
            out_path (str): Path to save the output data.
        """
        self.client_id     = client_id
        self.client_secret = client_secret
        self.coord_json    = coord_json_path
        self.out_path      = out_path
        self.bbox = None 
        self.load_bbox()


    def authenticate(self):
        """Authenticate with the Copernicus API and fetch the token."""
        self.token = fetch_auth_token(self.client_id, self.client_secret)
        if not self.token:
            raise RuntimeError("Auth failed")

    def load_bbox(self):
        """Load the bounding box from the JSON file."""
        self.bbox = get_bbox_from_json(self.coord_json)
        if not self.bbox:
            raise RuntimeError("Invalid BBOX")

    def build_payload(self):
        """Build the payload for the API request."""
        raise NotImplementedError

    def fetch(self):
        """
        Fetch data from the Copernicus API.
        This method handles the authentication, payload creation,
        and the actual data fetching process.
        """
        self.authenticate()
        # self.load_bbox()
        payload = self.build_payload()
        headers = {
          "Authorization": f"Bearer {self.token}",
          "Content-Type":    "application/json",
        }
        # print("POSTING to", self.PROCESS_URL)
        # print("Payload:", json.dumps(payload, indent=2))

        resp = post_json(self.PROCESS_URL, headers, payload)

        if resp is None:
            print("Fetch failed, aborting or using fallback")
            return None
            
        with open(self.out_path, "wb") as f:
            f.write(resp.content)
        return self.out_path
