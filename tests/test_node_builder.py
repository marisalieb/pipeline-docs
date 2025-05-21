import pytest
from unittest.mock import MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# mock for hou node error
class DummyNodeError(Exception):
    pass
mock_hou = MagicMock()
mock_hou.NodeError = DummyNodeError
# dummy hou module
sys.modules['hou'] = mock_hou

from node_setup.node_builder import NodeBuilder
import hou

def test_init_raises_if_no_geo_node():
    with pytest.raises(hou.NodeError):
        NodeBuilder(None)

def test_build_raises_not_implemented():
    mock_geo = MagicMock()
    builder = NodeBuilder(mock_geo)
    with pytest.raises(NotImplementedError):
        builder.build()

def test_layout_calls_layoutChildren():
    mock_geo = MagicMock()
    builder = NodeBuilder(mock_geo)
    builder.layout()
    mock_geo.layoutChildren.assert_called_once()
