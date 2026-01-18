"""Tests for timely_beliefs.sources.utils module."""

import warnings

import pandas as pd
import pytest

from timely_beliefs import BeliefSource
from timely_beliefs.sources.utils import ensure_source_exists, ensure_sources_exists


def test_ensure_source_exists_with_belief_source():
    """Test that a BeliefSource passes through unchanged."""
    source = BeliefSource("TestSource")
    result = ensure_source_exists(source)
    assert result is source
    assert isinstance(result, BeliefSource)


def test_ensure_source_exists_with_string():
    """Test creating a BeliefSource from a string."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = ensure_source_exists("TestSource")

        assert isinstance(result, BeliefSource)
        assert result.name == "TestSource"
        assert len(w) == 1
        assert "created from" in str(w[0].message)


def test_ensure_source_exists_with_int():
    """Test creating a BeliefSource from an integer."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = ensure_source_exists(42)

        assert isinstance(result, BeliefSource)
        # Integer gets converted to string name
        assert len(w) == 1
        assert "created from" in str(w[0].message)


def test_ensure_source_exists_with_none_not_allowed():
    """Test that None raises an error when not allowed."""
    with pytest.raises(Exception):
        ensure_source_exists(None, allow_none=False)


def test_ensure_source_exists_with_none_allowed():
    """Test that None is allowed when explicitly permitted."""
    result = ensure_source_exists(None, allow_none=True)
    assert result is None


def test_ensure_sources_exists_with_series():
    """Test applying ensure_source_exists on a Series."""
    # Create a Series with mixed types
    sources = pd.Series(
        [
            BeliefSource("Source1"),
            "Source2",
            BeliefSource("Source3"),
            "Source2",  # Duplicate to test mapping
        ]
    )

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = ensure_sources_exists(sources)

        assert isinstance(result, pd.Series)
        assert len(result) == 4

        # Check that all results are BeliefSource objects
        assert all(isinstance(s, BeliefSource) for s in result)

        # Check that Source1 and Source3 remained the same
        assert result.iloc[0].name == "Source1"
        assert result.iloc[2].name == "Source3"

        # Check that Source2 was created (appears twice)
        assert result.iloc[1].name == "Source2"
        assert result.iloc[3].name == "Source2"

        # Should only warn once per unique non-BeliefSource value
        assert len(w) == 1  # Only one unique string "Source2"


def test_ensure_sources_exists_all_belief_sources():
    """Test that a Series of BeliefSources passes through without warnings."""
    sources = pd.Series(
        [
            BeliefSource("Source1"),
            BeliefSource("Source2"),
            BeliefSource("Source1"),
        ]
    )

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = ensure_sources_exists(sources)

        assert isinstance(result, pd.Series)
        assert len(result) == 3
        assert all(isinstance(s, BeliefSource) for s in result)
        # No warnings should be issued
        assert len(w) == 0


def test_ensure_sources_exists_with_none_not_allowed():
    """Test that None in Series raises an error when not allowed."""
    sources = pd.Series([BeliefSource("Source1"), None])

    with pytest.raises(Exception):
        ensure_sources_exists(sources, allow_none=False)


def test_ensure_sources_exists_with_none_allowed():
    """Test that None in Series is allowed when explicitly permitted."""
    sources = pd.Series([BeliefSource("Source1"), None, "Source2"])

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = ensure_sources_exists(sources, allow_none=True)

        assert isinstance(result, pd.Series)
        assert len(result) == 3
        assert isinstance(result.iloc[0], BeliefSource)
        assert result.iloc[1] is None
        assert isinstance(result.iloc[2], BeliefSource)
        # Only Source2 should generate a warning
        assert len(w) == 1


def test_ensure_sources_exists_empty_series():
    """Test handling of an empty Series."""
    sources = pd.Series([], dtype=object)
    result = ensure_sources_exists(sources)

    assert isinstance(result, pd.Series)
    assert len(result) == 0


def test_ensure_sources_exists_preserves_index():
    """Test that the Series index is preserved."""
    sources = pd.Series([BeliefSource("Source1"), "Source2"], index=["a", "b"])

    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        result = ensure_sources_exists(sources)

        assert list(result.index) == ["a", "b"]
        assert isinstance(result.loc["a"], BeliefSource)
        assert isinstance(result.loc["b"], BeliefSource)
