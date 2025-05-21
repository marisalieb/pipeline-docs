import hou

class NodeBuilder:
    """
    Base class for building a node graph in Houdini.
    Subclasses should implement the build() method to create a specific node graph.
    """
    def __init__(self, geo_node):
        """
        Initializes the NodeBuilder with a geometry node.
        
        Args:
            geo_node (hou.Node): The geometry node to build the node graph in.
        """
        self.geo = geo_node
        if not self.geo:
            raise hou.NodeError("Geometry node is None")

    def build(self):
        """Subclasses implement their node graph here."""
        raise NotImplementedError

    def layout(self):
        """
        Layout the children nodes.
        """
        self.geo.layoutChildren()


