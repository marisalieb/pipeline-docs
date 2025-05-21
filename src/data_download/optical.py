
from .base import DataFetcher
from utils.post_json import post_json

# Data request in python for satelite S2L2A processing
# Modified from:
# Copernicus SentinelHub Documentation. (n.d.). Examples for S2L2A [online].
# [Accessed 27/02/2025]. Available from: https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Process/Examples/S2L2A.html 

class OpticalFetcher(DataFetcher):
    """Class to fetch optical data from Copernicus API."""
    def __init__(self, client_id, client_secret, coord_json,
                 out_png, width, height, time_from, time_to):
        """
        Initialize the OpticalFetcher.
        
        Args:
            client_id (str): Copernicus client ID.
            client_secret (str): Copernicus client secret.
            coord_json (str): Path to the JSON file containing coordinates.
            out_png (str): Path to save the output PNG.
            width (int): Width of the output image.
            height (int): Height of the output image.
            time_from (str): Start time for data fetching.
            time_to (str): End time for data fetching.
        """
        super().__init__(client_id, client_secret, coord_json, out_png)
        self.width, self.height = width, height
        self.time_from, self.time_to = time_from, time_to

    def build_payload(self):
        """Build the payload for the API request, specifically for the optical data."""
        return {
          "input": {
            "bounds": {"properties":{"crs":"http://www.opengis.net/def/crs/OGC/1.3/CRS84"},"bbox":self.bbox},
            "data": [{
              "type":"sentinel-2-l2a",
              "dataFilter": {
                 "timeRange": {"from":self.time_from, "to":self.time_to},
                 "orbitDirection": "DESCENDING"
              }
            }]
          },
          "output": {"width":self.width,"height":self.height},
                     
          "evalscript": """
            //VERSION=3
            function setup() {
            return {
                input: ["B02", "B03", "B04"],
                output: { bands: 3 },
            }
            }

            function evaluatePixel(sample) {
            return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
            }
            """
        }

    def fetch(self):
        """Override fetch to modify headers to accept tiff format."""
        self.authenticate()
        self.load_bbox()
        payload = self.build_payload()
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "image/tiff", 
        }

        resp = post_json(self.PROCESS_URL, headers, payload)

        if resp is None:
            print("Fetch failed, aborting or using fallback")
            return None

        with open(self.out_path, "wb") as f:
            f.write(resp.content)
        return self.out_path