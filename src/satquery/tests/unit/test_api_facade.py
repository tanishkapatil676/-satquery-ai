import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from satquery.schemas.api import QueryApiRequest
from satquery.application.api_facade import SatQueryApiFacade

def test_query_schema_validation():
    # Valid VQA
    req = QueryApiRequest(task="vqa", asset_ids=["a1"], question="Is there water?")
    assert req.task == "vqa"

    # Invalid VQA without question
    with pytest.raises(ValueError, match="non-empty question"):
        QueryApiRequest(task="vqa", asset_ids=["a1"])

    # Invalid change detection with 1 asset
    with pytest.raises(ValueError, match="requires exactly 2 asset IDs"):
        QueryApiRequest(task="change_detection", asset_ids=["a1"])

def test_facade_unknown_asset():
    facade = SatQueryApiFacade(asset_registry={})
    req = QueryApiRequest(task="vqa", asset_ids=["unknown-id"], question="Test?")
    res = facade.process_query(req)
    assert res.status == "rejected"
    assert "not found" in res.warnings[0]
