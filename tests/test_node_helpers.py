from unittest.mock import MagicMock
import sys
from pathlib import Path

sys.modules['hou'] = MagicMock()

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from node_setup.node_helpers import build_wrangle_snippet, ensure_blend_slider

def test_blend_slider_added_if_missing():
    wrangle = MagicMock()
    group = MagicMock()
    group.find.return_value = None
    wrangle.parmTemplateGroup.return_value = group

    ensure_blend_slider(wrangle, 3)

    group.append.assert_called()
    wrangle.setParmTemplateGroup.assert_called_with(group)


def test_wrangle_snippet_two_images():
    snippet = build_wrangle_snippet("/data", 2, "optical", "tiff")
    assert 'colormap("/data/optical_1.tiff", uv);' in snippet
    assert 'result = lerp(map1, map2, t);' in snippet
    assert '@Cd = result;' in snippet
