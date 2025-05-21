import hou
from PIL import Image
import numpy as np

from node_setup.node_builder import NodeBuilder
from utils.bbox import get_bbox_from_json, bbox_to_km_scale, calculate_transform_scale_from_coords


class DEMNodeBuilder(NodeBuilder):
    """
    DEMNodeBuilder is a subclass of NodeBuilder that creates a node graph for Digital Elevation Model (DEM) data in Houdini.
    It sets up a series of nodes to handle DEM data, including reading the TIFF file, scaling the heightfield, converting it to polygons, and setting up the DEM output node.
    """
    def __init__(self, geo_node, tiff_path, coord_json):
        """
        Initializes the DEMNodeBuilder with a geometry node, TIFF file path, and coordinate JSON file.
        
        Args:
            geo_node (hou.Node): The geometry node to build the node graph in.
            tiff_path (str): The path to the TIFF file containing the DEM data.
            coord_json (str): The path to the JSON file containing coordinate information.
        """
        super().__init__(geo_node)
        self.tiff = tiff_path
        self.coord_json = coord_json

    def build(self):
        """
        Builds the node graph for DEM data processing.
        This includes creating nodes for reading the TIFF file, scaling the heightfield, converting it to polygons, and setting up the output node.        """

        hf = self.geo.createNode("heightfield_file", "DEM_in")
        hf.parm("filename").set(self.tiff)
        hf.parm('size').set(100) # set this dynamically later
        hf.parm('heightscale').set(2200/1000)
        hf.setColor(hou.Color((1.0, 1.0, 1.0)))

        bbox = get_bbox_from_json(self.coord_json)
        bbox_to_km_scale(bbox)
        sx, sz = calculate_transform_scale_from_coords(self.coord_json, bbox)

        xf = self.geo.createNode("xform", "scale_km")
        xf.setInput(0, hf)
        xf.parm("sx").set(sz) # needs to be swapped for houdini axes
        xf.parm("sz").set(sx)

        # create heightfield convert
        hf_convert = self.geo.createNode("convertheightfield", "convert_to_polygons")
        hf_convert.setInput(0, xf)
        hf_convert.parm("lod").set(0.5)  # Convert to heightfield

        out = self.geo.createNode("null", "OUT_Terrain")
        out.setInput(0, hf_convert)
        out.setColor(hou.Color((1.0, 1.0, 1.0)))

        out.setDisplayFlag(True)
        self.layout()


class FallbackNodeBuilder(NodeBuilder):
    """
    FallbackNodeBuilder is a subclass of NodeBuilder that creates a fallback node graph in Houdini.
    It sets up a series of nodes to handle cases where the DEM data is not available or invalid.
    It creates a blank TIFF file and sets up a File SOP pointing to the fallback TIFF and colours it red to make it obvisou to the user that it is a fallback.
    """
    def __init__(self, geo_node, fallback_path, width, height):
        """
        Initializes the FallbackNodeBuilder with a geometry node, fallback TIFF file path, width and height.
        
        Args:
            geo_node (hou.Node): The geometry node to build the node graph in.
            fallback_path (str): The path to the fallback TIFF file.
            width (float): The width of the blank TIFF image.
            height (float): The height of the blank TIFF image.
        """
        super().__init__(geo_node)
        self.fallback_path = fallback_path
        self.width = width
        self.height = height

    def create_blank_tiff(self):
        """Creates a blank 16-bit grayscale TIFF file."""
        data = np.zeros((self.height, self.width), dtype=np.uint16)
        image = Image.fromarray(data, mode='I;16')
        image.save(self.fallback_path, format='TIFF')
        print(f"Blank TIFF image created at: {self.fallback_path}")

    def build(self):
        """Creates a File SOP pointing to the fallback TIFF and colours it red."""
        self.create_blank_tiff()
        file_node = self.geo.createNode("file", "fallback_file_class")
        file_node.parm("file").set(self.fallback_path)

        # set colour to red
        colour_node = self.geo.createNode("color", "color_fallback")
        colour_node.parm('colorr').set(1)
        colour_node.parm('colorg').set(0)
        colour_node.parm('colorb').set(0)
        colour_node.setInput(0, file_node)

        null_node = self.geo.createNode("null", "OUT_terrain")
        null_node.setInput(0, colour_node)
        null_node.setDisplayFlag(True)

        self.layout()
        print("Fallback null node added successfully!")
        return null_node

