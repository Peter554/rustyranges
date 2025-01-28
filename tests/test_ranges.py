from decimal import Decimal as D

import pytest
import xocto.ranges as xocto_ranges
import rustyranges
import pysimpleranges


RANGE_MODULES = {xocto_ranges, rustyranges, pysimpleranges}


@pytest.mark.parametrize("ranges_module", RANGE_MODULES)
def test_range(ranges_module):
    range = ranges_module.Range(D(0), D(1))
    if ranges_module in {xocto_ranges, pysimpleranges}:
        assert range.start == D(0)
        assert range.end == D(1)
    else:
        assert range.start.value() == D(0)
        assert range.end.value() == D(1)


@pytest.mark.parametrize("ranges_module", RANGE_MODULES)
@pytest.mark.parametrize(
    "ranges_fn, expected_intersection_fn",
    [
        [
            lambda rm: (
                rm.Range(D(0), D(1)),
                rm.Range(D(1), D(2)),
            ),
            lambda rm: None,
        ],
        [
            lambda rm: (
                rm.Range(D(0), D(2)),
                rm.Range(D(1), D(3)),
            ),
            lambda rm: rm.Range(D(1), D(2)),
        ],
        [
            lambda rm: (
                rm.Range(D(0), D(3)),
                rm.Range(D(1), D(2)),
            ),
            lambda rm: rm.Range(D(1), D(2)),
        ],
    ],
)
def test_range_intersection(ranges_fn, expected_intersection_fn, ranges_module):
    r1, r2 = ranges_fn(ranges_module)
    assert (
        r1.intersection(r2)
        == r2.intersection(r1)
        == expected_intersection_fn(ranges_module)
    )


@pytest.mark.parametrize("ranges_module", RANGE_MODULES)
@pytest.mark.parametrize(
    "ranges_fn,expected_ranges_fn",
    [
        [
            lambda rm: [
                rm.Range(D(0), D(1)),
                rm.Range(D(2), D(3)),
            ],
            lambda rm: [
                rm.Range(D(0), D(1)),
                rm.Range(D(2), D(3)),
            ],
        ],
        [
            lambda rm: [
                rm.Range(D(0), D(2)),
                rm.Range(D(1), D(3)),
            ],
            lambda rm: [
                rm.Range(D(0), D(3)),
            ],
        ],
        [
            lambda rm: [
                rm.Range(D(0), D(10)),
                rm.Range(D(1), D(9)),
            ],
            lambda rm: [
                rm.Range(D(0), D(10)),
            ],
        ],
        [
            lambda rm: [rm.Range(D(x), D(x + 1)) for x in range(0, 100)],
            lambda rm: [
                rm.Range(D(0), D(100)),
            ],
        ],
    ],
)
def test_rangeset(ranges_fn, expected_ranges_fn, ranges_module):
    ranges = ranges_fn(ranges_module)
    ranges.reverse()
    ranges_copy = ranges.copy()

    rangeset = ranges_module.RangeSet(ranges)

    assert list(rangeset) == expected_ranges_fn(ranges_module)
    assert ranges == ranges_copy  # Check that `ranges` was not modified.
