import pytest
import snippet_128 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bytes_0 = b'\x82\xa6[\xe8'
    module_0.PartitionRefinement(bytes_0)