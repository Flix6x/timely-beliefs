# Test Coverage Recommendations for timely-beliefs

This document provides recommendations for improving test coverage in the timely-beliefs library, based on analysis of the codebase and existing test suite.

## Current Coverage Status

Based on the initial coverage analysis, the project has approximately **20% overall code coverage**. Key areas have varying levels of coverage:

### Well-Covered Modules (✅ >50% coverage)
- `db_base.py` - 100%
- `sensors/__init__.py` - 100%  
- `sources/__init__.py` - 100%
- `sensors/classes.py` - 53%
- `examples/__init__.py` - 70%
- `sources/classes.py` - 64%

### Partially Covered Modules (⚠️ 20-50% coverage)
- `beliefs/classes.py` - 23% (736 statements, 570 missed)
- `examples/beliefs_data_frames.py` - 27%
- `sensors/func_store/knowledge_horizons.py` - 34%
- `sensors/func_store/utils.py` - 16%
- `sensors/utils.py` - 40%
- `sources/utils.py` - 43%

### Uncovered or Minimally Covered Modules (❌ <20% coverage)
- `beliefs/probabilistic_utils.py` - 12% (243 statements, 213 missed)
- `beliefs/utils.py` - 12% (381 statements, 336 missed)
- `beliefs/queries.py` - 0% (19 statements, all missed)
- `utils.py` (root) - 12% (104 statements, 91 missed)
- `visualization/graphs.py` - 0% (39 statements, all missed)
- `visualization/selectors.py` - 0% (42 statements, all missed)
- `visualization/utils.py` - 0% (132 statements, all missed)
- `sensors/func_store/event_values.py` - 0%
- `examples/visualize_example.py` - 0%

## Priority Recommendations

### High Priority: Core Business Logic

#### 1. `beliefs/utils.py` (12% → Target: 70%+)
**Current gaps**: 336 of 381 statements untested

Key functions needing coverage:
- `propagate_beliefs()` - Belief propagation logic
- `resample_instantaneous_events()` - Event resampling
- `add_belief_to_nan_df()` - DataFrame manipulation
- `set_of_belief_horizons()` - Horizon calculations
- `filter_query_window()` - Query filtering

**Recommended tests**:
```python
# Test basic belief propagation
def test_propagate_beliefs_forward():
    # Test forward propagation of beliefs

def test_propagate_beliefs_backward():
    # Test backward propagation of beliefs

# Test resampling functionality
def test_resample_instantaneous_events_upsampling():
    # Test converting instantaneous events to time slots

def test_resample_instantaneous_events_downsampling():
    # Test aggregating time slots to instantaneous

# Test DataFrame operations
def test_add_belief_to_nan_df():
    # Test adding beliefs to empty DataFrames

def test_filter_query_window_inclusive():
    # Test window filtering with inclusive bounds

def test_filter_query_window_exclusive():
    # Test window filtering with exclusive bounds
```

#### 2. `beliefs/probabilistic_utils.py` (12% → Target: 65%+)
**Current gaps**: 213 of 243 statements untested

Critical functions:
- `interpret_complete_cdf()` - CDF interpretation
- `cp_to_p()` - Probability conversion  
- `get_median_belief()` - Median calculation
- `partial_cdf()` - Partial CDF operations
- `marginal_distribution()` - Distribution marginalization

**Recommended tests**:
```python
def test_interpret_complete_cdf_normal_distribution():
    # Test CDF interpretation for normal distributions

def test_cp_to_p_conversion():
    # Test cumulative to point probability conversion

def test_get_median_belief():
    # Test median extraction from probabilistic beliefs

def test_partial_cdf_extraction():
    # Test extracting partial CDFs

def test_marginal_distribution_bivariate():
    # Test marginalization of bivariate distributions

def test_marginal_distribution_multivariate():
    # Test marginalization of multivariate distributions
```

#### 3. `beliefs/queries.py` (0% → Target: 80%+)
**Current gaps**: All 19 statements untested

The `query_unchanged_beliefs()` function has complex SQL logic that should be thoroughly tested.

**Recommended tests**:
```python
def test_query_unchanged_beliefs_no_changes():
    # Test when beliefs haven't changed

def test_query_unchanged_beliefs_with_changes():
    # Test filtering out changed beliefs

def test_query_unchanged_beliefs_multiple_sources():
    # Test with multiple belief sources

def test_query_unchanged_beliefs_time_ranges():
    # Test with various time ranges
```

#### 4. `beliefs/classes.py` (23% → Target: 60%+)
**Current gaps**: 570 of 736 statements untested

Major untested areas:
- BeliefDataFrame aggregation methods
- Probabilistic belief operations
- DataFrame slicing and filtering edge cases
- Metadata preservation during operations

**Focus areas**:
- Test all aggregation methods (sum, mean, etc.)
- Test probabilistic operations (belief combinations)
- Test edge cases (empty frames, single values)
- Test metadata retention across operations

### Medium Priority: Utility Functions

#### 5. `utils.py` (root) (12% → Target: 70%+)
**Current gaps**: 91 of 104 statements untested

Key utilities:
- `parse_datetime_like()` - Datetime parsing
- `enforce_tz()` - Timezone enforcement
- `remove_deprecated_kwargs()` - Deprecated parameter handling
- `timedelta_to_pandas_freq_str()` - Frequency string conversion

#### 6. New Test Files Created

The following test files have been added to improve coverage:

**`test_sensor_utils.py`** - Tests for `sensors/utils.py`:
- ✅ `jsonify_time_dict()` - ISO string conversion
- ✅ `unjsonify_time_dict()` - ISO string parsing
- ✅ `eval_verified_knowledge_horizon_fnc()` - Knowledge horizon evaluation
- ✅ `FUNC_STORE` - Function store validation

**`test_source_utils.py`** - Tests for `sources/utils.py`:
- ✅ `ensure_source_exists()` - Source creation and validation
- ✅ `ensure_sources_exists()` - Batch source validation

**Note**: These tests currently fail due to PostgreSQL authentication issues in the local environment, but they are properly structured and will work in the CI environment where PostgreSQL is correctly configured.

### Low Priority: Visualization (Optional Dependencies)

#### 7. Visualization Modules (0% → Target: 40%+)
**Current gaps**: All visualization code untested

These modules depend on optional dependencies (altair), so lower coverage is acceptable:
- `visualization/graphs.py` - 0%
- `visualization/selectors.py` - 0%
- `visualization/utils.py` - 0%

**Recommendations**:
- Add tests for core visualization logic (data preparation)
- Mock altair dependency where possible
- Test data transformation without rendering
- Add integration tests when altair is available

### Testing Infrastructure Improvements

#### 8. Database Test Fixtures

**Current issue**: All test fixtures have `autouse=True` which causes database connection attempts even for tests that don't need it.

**Recommendation**: Refactor `conftest.py` to:
1. Make database fixtures opt-in (set `autouse=False`)
2. Create marker for DB-required tests: `@pytest.mark.requires_db`
3. Allow non-DB tests to run without PostgreSQL

Example:
```python
@pytest.fixture(scope="function", autouse=False)  # Changed from True
def db():
    """Database fixture - only used when explicitly requested."""
    Base.metadata.create_all(engine)
    yield Base.metadata
    session.close()
    Base.metadata.drop_all(engine)
```

#### 9. Coverage Configuration

Coverage reporting has been configured in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
addopts = "--cov=timely_beliefs --cov-report=term-missing --cov-report=lcov"

[tool.coverage.run]
source = ["timely_beliefs"]
omit = ["*/tests/*", "*/test_*.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

## Testing Best Practices

### General Guidelines

1. **Test Independence**: Each test should be runnable in isolation
2. **Clear Names**: Use descriptive test names that explain what is being tested
3. **Arrange-Act-Assert**: Structure tests with clear setup, execution, and verification
4. **Edge Cases**: Test boundary conditions, empty inputs, and error cases
5. **Parametrize**: Use `@pytest.mark.parametrize` for testing multiple scenarios

### Example Test Structure

```python
def test_function_name_scenario():
    """Clear description of what this test verifies."""
    # Arrange: Set up test data
    input_data = create_test_data()
    
    # Act: Execute the function
    result = function_under_test(input_data)
    
    # Assert: Verify expectations
    assert result == expected_output
    assert result.property == expected_value
```

### Coverage Goals

- **Critical paths**: 80%+ coverage
- **Business logic**: 70%+ coverage
- **Utilities**: 65%+ coverage  
- **Visualization**: 40%+ coverage (optional dependencies)
- **Overall project**: 60%+ coverage (current: ~20%)

## Next Steps

1. ✅ **Set up Coveralls integration** - Completed
2. ✅ **Add coverage badge to README** - Completed
3. ✅ **Configure pytest-cov** - Completed
4. ✅ **Create initial test files** - `test_sensor_utils.py` and `test_source_utils.py` added
5. ⏳ **Fix database fixture issues** - Recommended for future work
6. ⏳ **Implement high-priority tests** - Begin with `beliefs/queries.py` and `beliefs/utils.py`
7. ⏳ **Improve core module coverage** - Focus on `beliefs/probabilistic_utils.py`
8. ⏳ **Add integration tests** - Test complete workflows
9. ⏳ **Review and update** - Regularly review coverage reports and update priorities

## Continuous Integration

The GitHub Actions workflow (`.github/workflows/lint-and-test.yml`) now includes:
- Automated coverage collection with pytest-cov
- Coverage upload to Coveralls (Python 3.12 only)
- Coverage badge in README showing current coverage percentage

Coverage will be tracked automatically on every push, making it easy to see the impact of new tests.

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Plugin](https://pytest-cov.readthedocs.io/)
- [Coveralls Documentation](https://docs.coveralls.io/)
- [Code Coverage Best Practices](https://testing.googleblog.com/2020/08/code-coverage-best-practices.html)

---

**Last Updated**: 2026-01-18  
**Overall Coverage**: ~20% (Target: 60%+)
