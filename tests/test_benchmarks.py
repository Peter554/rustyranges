import random
from decimal import Decimal

import pytest
from xocto import ranges as xocto_ranges
import rustyranges
import pysimpleranges


@pytest.mark.benchmark(group="range_init")
@pytest.mark.parametrize("ranges_module", [xocto_ranges, rustyranges, pysimpleranges])
def test_benchmark_range_init(ranges_module, benchmark):
    n = 100_000

    def init_ranges():
        for x in range(n):
            ranges_module.Range(Decimal(x), Decimal(x + 1))

    benchmark(init_ranges)


@pytest.mark.benchmark(group="range_read_start_and_end")
@pytest.mark.parametrize("ranges_module", [xocto_ranges, rustyranges, pysimpleranges])
def test_benchmark_range_read_start_and_end(ranges_module, benchmark):
    n = 100_000
    ranges = [ranges_module.Range(Decimal(x), Decimal(x + 1)) for x in range(n)]

    def read_start_and_end():
        for range_ in ranges:
            _ = range_.start
            _ = range_.end

    benchmark(read_start_and_end)


@pytest.mark.benchmark(group="range_intersection")
@pytest.mark.parametrize("ranges_module", [xocto_ranges, rustyranges, pysimpleranges])
def test_benchmark_range_intersection(ranges_module, benchmark):
    n = 100_000
    ranges = [ranges_module.Range(Decimal(x), Decimal(x + 2)) for x in range(n)]

    def intersection():
        for r1, r2 in zip(ranges[:-1], ranges[1:]):
            _ = r1.intersection(r2)

    benchmark(intersection)


@pytest.mark.benchmark(group="rangeset_init")
@pytest.mark.parametrize("ranges_module", [xocto_ranges, rustyranges, pysimpleranges])
def test_benchmark_rangeset_init(ranges_module, benchmark):
    n = 100_000
    ranges = [ranges_module.Range(Decimal(x), Decimal(x + 1)) for x in range(n)]
    random.seed(42)
    random.shuffle(ranges)

    rangeset = benchmark(ranges_module.RangeSet, ranges)

    assert list(rangeset) == [ranges_module.Range(Decimal(0), Decimal(n))]
