import hou

from node_setup.node_builder import NodeBuilder
from node_setup.node_helpers import ensure_blend_slider, build_wrangle_snippet


class TemperatureNodeBuilder(NodeBuilder):
    """
    TemperatureNodeBuilder is a subclass of NodeBuilder that creates a node graph for temperature data processing in Houdini.
    It sets up a series of nodes to handle temperature data, including blending image values, scattering points on the surface and visualising the temperatures with spheres.
    """
    def __init__(self, geo_node, data_folder, date_ranges):
        """
        Initializes the TemperatureNodeBuilder with a geometry node and data folder.
        
        Args:
            geo_node (hou.Node): The geometry node to build the node graph in.
            data_folder (str): The folder where the temperature data is stored.
            date_ranges (list): A list of date ranges for the temperature data.
        """
        super().__init__(geo_node)
        self.png = data_folder
        self.date_ranges = date_ranges

    def build(self):
        """
        Builds the node graph for temperature data processing.
        This includes creating nodes for blending image values by passing in a VEX snippet, scattering points on the surface, visualising the temperatures and connecting the nodes to the existing terrain and optical nodes.
        It also sets colours on the nodes to better visualise the nodes the user should interact with, so green for the nodes that should be viewed and red for the nodes that should be interacted with.
        """
        num_images = len(self.date_ranges)

        snippet = build_wrangle_snippet(self.png, num_images, "thermal_data", "png")

        terrain_node = self.geo.node("OUT_Terrain")
        if terrain_node is None:
            raise hou.NodeError("Node 'OUT_terrain' not found.")

        attrib_wrangle_temperature = self.geo.createNode("attribwrangle", "blend_values_temperature")
        attrib_wrangle_temperature.parm("snippet").set(snippet)
        attrib_wrangle_temperature.setInput(0, terrain_node)
        attrib_wrangle_temperature.setDisplayFlag(True)
        ensure_blend_slider(attrib_wrangle_temperature, num_images)
        # attrib_wrangle_temperature.setColor(hou.Color((1.0, 0.0, 0.0)))
        attrib_wrangle_temperature.parm("blendAll").setExpression('ch("../blend_values/blendAll")')


        scatter = self.geo.createNode("scatter", "scatter_points")
        scatter.parm("npts").set(2000)
        scatter.setInput(0, attrib_wrangle_temperature)

        sphere_size_wrangle = self.geo.createNode("attribwrangle", "sphere_scale")
        sphere_size_wrangle.parm("snippet").set('f@pscale = clamp(@Cd.r * 100.0, 0.1, 3.0);')  
        sphere_size_wrangle.setInput(0, scatter)

        sphere = self.geo.createNode("sphere", "sphere_temperature")
        sphere.parm("type").set(0) 
        sphere.parm("radx").set(0.5)
        sphere.parm("rady").set(0.5)
        sphere.parm("radz").set(0.5)
        sphere.parm("scale").set(0.2)

        transform = self.geo.createNode("xform", "sphere_transform")
        transform.parm("ty").set(0.1)
        transform.setInput(0, sphere)

        transform_sphere_size = self.geo.createNode("xform", "sphere_size")
        transform_sphere_size.setColor(hou.Color((1.0, 0.0, 0.0)))  # Red
        transform_sphere_size.setInput(0, transform)
            
        copy = self.geo.createNode("copytopoints::2.0", "copy_spheres")
        copy.setInput(0, transform_sphere_size)
        copy.setInput(1, sphere_size_wrangle)
        copy.setColor(hou.Color((1.0, 1.0, 1.0)))

        
        attrib_delete = self.geo.createNode("attribdelete", "delete_uvs_spheres")
        attrib_delete.parm("ptdel").set("uv")
        attrib_delete.setInput(0, copy)

        color_node = self.geo.createNode("color", "spheres_color")
        color_node.parmTuple("color").set((0.15,0.3,0.3))
        color_node.setInput(0, attrib_delete)
        color_node.setColor(hou.Color((1.0, 0.0, 0.0)))  # Red
        
        thermal_out = self.geo.createNode("null", "OUT_THERMAL")
        thermal_out.setInput(0, color_node)
        thermal_out.setColor(hou.Color((1.0, 1.0, 1.0)))

        terrain_textured_out = self.geo.node("OUT_Textured_Terrain")
        if terrain_textured_out is None:
            raise hou.NodeError("Node 'OUT_Textured_Terrain' not found.")

        merge = self.geo.createNode("merge", "merge_terrain_thermal")
        merge.setInput(0, thermal_out)
        merge.setInput(1, terrain_textured_out)

        out_terrain_thermal = self.geo.createNode("null", "OUT_Temperature_Change_with_Terrain")
        out_terrain_thermal.setInput(0, merge)
        out_terrain_thermal.setColor(hou.Color((.075, .30, .0750)))

        self.geo.layoutChildren()

        out_terrain_thermal.setDisplayFlag(True)
        out_terrain_thermal.setRenderFlag(True)

