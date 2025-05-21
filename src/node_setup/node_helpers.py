import hou
from pathlib import Path

_cached_geo = None

def clear_geo_cache():
    """
    Clears the cached geometry node.
    This is useful when the geometry node changes for a new input such as when comparing different date ranges or areas.
    """
    global _cached_geo
    _cached_geo = None
    
def get_geo_node():
    """
    Gets the geometry node from the current context (only available in some cases) or usually prompts the user to select one.
    This function caches the geometry node to avoid prompting the user multiple times.
    If the geometry node is already selected, it will return the cached node.
    """
    global _cached_geo
    # If already selected, return it
    if _cached_geo is not None:
        return _cached_geo

    node = hou.pwd()
    if node:
        parent = node.parent()
        if parent and parent.type().name() == "geo":
            _cached_geo = parent
            return _cached_geo

    node_path = hou.ui.selectNode(
        relative_to_node=None,
        initial_node=None,
        node_type_filter=hou.nodeTypeFilter.Sop,
        title="Select a geometry node"
    )
    if not node_path:
        raise hou.NodeError("No geo node selected")

    geo_node = hou.node(node_path)
    if not geo_node:
        raise hou.NodeError(f"Invalid node selected: {node_path}")

    _cached_geo = geo_node
    return _cached_geo

def ensure_blend_slider(wrangle_node, num_images):
    """
    Ensures that the blend slider is present in the wrangle node since usually this requires user interaction on the wrangle node.    
    If it is not present, it creates a new slider with the specified number of images.
    """
    group = wrangle_node.parmTemplateGroup()
    if not group.find("blendAll"):
        blend_slider = hou.FloatParmTemplate(
            "blendAll", "Blend All", 1,
            default_value=(0.0,),
            min=0,
            max=max(1.0, num_images - 1),
            min_is_strict=True,
            max_is_strict=True
        )
        group.append(blend_slider)
        wrangle_node.setParmTemplateGroup(group)



def build_wrangle_snippet(data_folder, num_images, data_type, data_format):
    """
    Builds a wrangle snippet for blending images using colormap.
    The snippet uses the UV coordinates of the current point to sample the images.
    The blending is controlled by a slider that allows the user to blend between different times, for example for weekly data of 4 weeks it would set up a slider from 0 to 4.
    The snippet is designed to be used in a Wrangle node in Houdini.

    Args:
        data_folder (str): Path to the folder containing the images.
        num_images (int): Number of images to blend.
        data_type (str): Type of data, so either temperature or optical satalite data.
        data_format (str): Format of the images ("png", "jpg").

    Returns:
        snippet (str): The generated wrangle snippet.
    """
    lines = ['vector uv = point(0, "uv", @ptnum);', '']

    # Load colormaps
    for i in range(1, num_images + 1):
        img = Path(data_folder) / f"{data_type}_{i}.{data_format}"
        lines.append(f'vector map{i} = colormap("{img}", uv);')
    lines.append('')

    # Blending logic
    lines.append(f'float blend = chf("blendAll"); // 0–{num_images - 1}')
    lines.append('vector result;')
    lines.append('')

    for i in range(1, num_images):
        lines.append(f'if (blend < {i}.0) {{')
        lines.append(f'    float t = blend - {i - 1}.0;')
        lines.append(f'    result = lerp(map{i}, map{i + 1}, t);')
        if i < num_images - 1:
            lines.append('} else ')
        else:
            lines.append('} else {')
            lines.append(f'    result = map{num_images};')
            lines.append('}')

    lines.append('')
    lines.append('@Cd = result;')
    return "\n".join(lines)

