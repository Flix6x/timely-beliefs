"""Tests for timely_beliefs.sensors.utils module."""
from datetime import datetime, timedelta

import pytest
from pytz import utc

from timely_beliefs.sensors.utils import (
    jsonify_time_dict,
    unjsonify_time_dict,
    eval_verified_knowledge_horizon_fnc,
    FUNC_STORE,
)


def test_jsonify_time_dict():
    """Test converting datetime and timedelta values to ISO string format."""
    d = {
        "dt": datetime(2020, 1, 1, 12, 0, tzinfo=utc),
        "td": timedelta(hours=2),
        "str": "test",
        "int": 42,
    }
    result = jsonify_time_dict(d)

    assert result["dt"] == "2020-01-01T12:00:00+00:00"
    assert result["td"] == "PT2H"
    assert result["str"] == "test"
    assert result["int"] == 42


def test_unjsonify_time_dict():
    """Test converting ISO string values back to datetime and timedelta."""
    d = {
        "dt": "2020-01-01T12:00:00+00:00",
        "td": "PT2H",
        "str": "test",
        "int": 42,
    }
    result = unjsonify_time_dict(d)

    assert result["dt"] == datetime(2020, 1, 1, 12, 0, tzinfo=utc)
    assert result["td"] == timedelta(hours=2)
    assert result["str"] == "test"
    assert result["int"] == 42


def test_jsonify_unjsonify_roundtrip():
    """Test that jsonify and unjsonify are inverse operations."""
    original = {
        "dt": datetime(2020, 1, 1, 12, 0, tzinfo=utc),
        "td": timedelta(hours=2, minutes=30),
        "str": "test",
    }
    jsonified = jsonify_time_dict(original)
    result = unjsonify_time_dict(jsonified)

    assert result["dt"] == original["dt"]
    assert result["td"] == original["td"]
    assert result["str"] == original["str"]


def test_func_store_exists():
    """Test that FUNC_STORE is populated with knowledge horizon functions."""
    assert isinstance(FUNC_STORE, dict)
    assert len(FUNC_STORE) > 0

    # Check that each entry has expected structure
    for func_name, func_spec in FUNC_STORE.items():
        assert "fnc" in func_spec
        assert "args" in func_spec
        assert callable(func_spec["fnc"])
        assert isinstance(func_spec["args"], list)


def test_eval_verified_knowledge_horizon_fnc_ex_ante():
    """Test evaluating ex_ante knowledge horizon function."""
    result = eval_verified_knowledge_horizon_fnc(
        "ex_ante",
        par={"ex_ante_horizon": timedelta(hours=2)},  # Fixed: added required parameter
        event_start=datetime(2020, 1, 1, 12, 0, tzinfo=utc),
        event_resolution=timedelta(hours=1),
    )
    assert isinstance(result, timedelta)
    assert result == timedelta(hours=2)


def test_eval_verified_knowledge_horizon_fnc_ex_post():
    """Test evaluating ex_post knowledge horizon function."""
    event_resolution = timedelta(hours=1)
    result = eval_verified_knowledge_horizon_fnc(
        "ex_post",
        par={},
        event_start=datetime(2020, 1, 1, 12, 0, tzinfo=utc),
        event_resolution=event_resolution,
    )
    assert isinstance(result, timedelta)
    assert result == -event_resolution


def test_eval_verified_knowledge_horizon_fnc_x_days_ago_at_y_oclock():
    """Test evaluating x_days_ago_at_y_oclock knowledge horizon function."""
    event_start = datetime(2020, 1, 5, 15, 0, tzinfo=utc)
    result = eval_verified_knowledge_horizon_fnc(
        "x_days_ago_at_y_oclock",
        par={"x": 1, "y": 12, "z": "Europe/Amsterdam"},
        event_start=event_start,
    )
    assert isinstance(result, timedelta)
    # Should be positive since knowledge time is before event time
    assert result > timedelta(0)


def test_eval_verified_knowledge_horizon_fnc_with_bounds():
    """Test evaluating knowledge horizon function with bounds."""
    result = eval_verified_knowledge_horizon_fnc(
        "ex_ante",
        par={"ex_ante_horizon": timedelta(hours=2)},  # Fixed: added required parameter
        event_start=datetime(2020, 1, 1, 12, 0, tzinfo=utc),
        event_resolution=timedelta(hours=1),
        get_bounds=True,
    )
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], timedelta)
    assert isinstance(result[1], timedelta)


def test_eval_verified_knowledge_horizon_fnc_invalid_function():
    """Test that evaluating an invalid function name raises an exception."""
    with pytest.raises(Exception, match="cannot be executed safely"):
        eval_verified_knowledge_horizon_fnc(
            "invalid_function_name",
            par={},
            event_start=datetime(2020, 1, 1, 12, 0, tzinfo=utc),
            event_resolution=timedelta(hours=1),
        )


def test_eval_verified_knowledge_horizon_fnc_with_time_params():
    """Test evaluating knowledge horizon function with datetime/timedelta parameters."""
    event_start = datetime(2020, 1, 5, 15, 0, tzinfo=utc)
    # Parameters as ISO strings (as they would come from JSON)
    par = {
        "x": 1,
        "y": 12,
        "z": "Europe/Amsterdam",
    }
    result = eval_verified_knowledge_horizon_fnc(
        "x_days_ago_at_y_oclock",
        par=par,
        event_start=event_start,
    )
    assert isinstance(result, timedelta)
