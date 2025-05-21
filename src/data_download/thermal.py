from .base import DataFetcher

# Data request in python for satelite S3SLSTR processing
# Modified from:
# Copernicus SentinelHub Documentation. (n.d.). Examples for S3SLSTR [online].
# [Accessed 27/02/2025]. Available from: https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Process/Examples/S3SLSTR.html 

class ThermalFetcher(DataFetcher):
    """Class to fetch thermal data from Copernicus API."""
    def __init__(self, client_id, client_secret, coord_json,
                 out_png, width, height, time_from, time_to):
        """
        Initialize the ThermalFetcher.
        
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
        """Build the payload for the API request, specifically for the thermal data."""
        return {
          "input": {
            "bounds": {"properties":{"crs":"http://www.opengis.net/def/crs/EPSG/0/4326"},"bbox":self.bbox},
            "data": [{
              "type":"sentinel-3-slstr",
              "dataFilter": {
                 "timeRange": {"from":self.time_from, "to":self.time_to},
                 "orbitDirection": "DESCENDING"
              }
            }]
          },
          "output": {"width":self.width,"height":self.height,
                     "responses":[{"format":{"type":"image/png"}}]},
                     
          "evalscript": """
            //VERSION=3
            function setup() {
            return {
                input: ["F1"],
                output: {
                bands: 3,
                },
            }
            }

            // Create a Red gradient visualiser from 274-450 K
            var viz = ColorGradientVisualizer.createRedTemperature(274, 450)

            function evaluatePixel(sample) {
            return viz.process(sample.F1)
            }
            """
        }

