import hou

from node_setup.node_builder import NodeBuilder
from node_setup.node_helpers import ensure_blend_slider, build_wrangle_snippet


class OpticalNodeBuilder(NodeBuilder):
    """
    OpticalNodeBuilder is a subclass of NodeBuilder that creates a node graph for optical data processing in Houdini.
    It sets up a series of nodes to handle optical satelite data, including blending image values and switching between textured and untextured terrain.
    """
    def __init__(self, geo_node, data_folder, date_ranges):
        """
        Initializes the OpticalNodeBuilder with a geometry node and data folder.
        
        Args:
            geo_node (hou.Node): The geometry node to build the node graph in.
            data_folder (str): The folder where the optical data is stored.
            date_ranges (list): A list of date ranges for the optical data.
        """
        super().__init__(geo_node)
        self.tiff = data_folder
        self.date_ranges = date_ranges


    def build(self):
        """
        Builds the node graph for optical data processing.
        This includes creating nodes for blending image values by passing in a VEX snippet, switching between textured and untextured terrain, and connecting the nodes to the existing terrain nodes.
        It also sets colours on the nodes to better visualise the nodes the user should interact with, so green for the nodes that should be viewed and red for the nodes that should be interacted with.
        """
        terrain_node = self.geo.node("OUT_Terrain")
        if terrain_node is None:
            raise hou.NodeError("Node 'OUT_terrain' not found!")

        num_images = len(self.date_ranges)

        snippet = build_wrangle_snippet(self.tiff, num_images, "optical_data", "tiff")

        attrib_wrangle_optical = self.geo.createNode("attribwrangle", "blend_values")
        attrib_wrangle_optical.parm("snippet").set(snippet)
        attrib_wrangle_optical.setInput(0, terrain_node)
        attrib_wrangle_optical.setDisplayFlag(True)
        ensure_blend_slider(attrib_wrangle_optical, num_images)
        attrib_wrangle_optical.setColor(hou.Color((1.0, 0.0, 0.0)))

        color_node = self.geo.createNode("color", "untextured_terrain")
        color_node.parmTuple("color").set((1,1,1))
        color_node.setInput(0, terrain_node)

        switch = self.geo.createNode("switch", "switch_untextured_to_textured_terrain")
        switch.setInput(0, attrib_wrangle_optical)
        switch.setInput(1, color_node)
        switch.setColor(hou.Color((1.0, 0.0, 0.0)))

        # add attribute delete for uvs
        attrib_delete = self.geo.createNode("attribdelete", "delete_uvs_terrain")
        attrib_delete.parm("ptdel").set("uv")
        attrib_delete.setInput(0, switch)

        out_terrain_thermal = self.geo.createNode("null", "OUT_Textured_Terrain")
        out_terrain_thermal.setInput(0, attrib_delete)
        #out_terrain_thermal.setColor(hou.Color((1.0, 1.0, 1.0)))
        out_terrain_thermal.setColor(hou.Color((.075, .30, .07550)))

        out_terrain_thermal.setDisplayFlag(True)

        self.geo.layoutChildren()