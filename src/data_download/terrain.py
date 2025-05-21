from .base import DataFetcher

# Data request in python for DEM processing
# Modified from :
# Copernicus SentinelHub Documentation. (n.d.). DEM Processing Examples [online].
# [Accessed 27/02/2025]. Available from: https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Process/Examples/DEM.html 

class DEMFetcher(DataFetcher):
    """Class to fetch Digital Elevation Model (DEM) data from Copernicus API."""
    def __init__(self, client_id, client_secret, coord_json, out_tiff, res=0.0003):
        """
        Initialize the DEMFetcher.
        
        Args:
            client_id (str): Copernicus client ID.
            client_secret (str): Copernicus client secret.
            coord_json (str): Path to the JSON file containing coordinates.
            out_tiff (str): Path to save the output TIFF.
            res (float): Resolution of the output data.
        """
        super().__init__(client_id, client_secret, coord_json, out_tiff)
        self.res = res

    def build_payload(self):
        """Build the payload for the API request, specifically for the DEM data."""
        return {
          "input": {
            "bounds": {
              "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
              "bbox": self.bbox
            },
            "data": [
              {
                "type": "dem",
                "dataFilter": {"demInstance": "COPERNICUS_30"},
                "processing": {"upsampling": "BILINEAR", "downsampling": "BILINEAR"}
              }
            ]
          },
          "output": {
            "resx": self.res, "resy": self.res,
            "responses": [{"identifier":"default","format":{"type":"image/tiff"}}]
          },
          "evalscript": """
            //VERSION=3
            function setup() {
            return {
                input: ["DEM"],
                output: { bands: 1 },
            }
            }
            
            function evaluatePixel(sample) {
            return [sample.DEM / 2200]
            }
            """
        }
