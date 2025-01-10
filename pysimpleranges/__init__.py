from __future__ import annotations

import dataclasses
from decimal import Decimal
from collections.abc import Iterator


@dataclasses.dataclass(frozen=True)
class Range:
    start: Decimal
    end: Decimal

    def intersection(self, other: Range) -> Range | None:
        left, right = (self, other) if self.start <= other.start else (other, self)
        if left.end <= right.start:
            return None
        return Range(right.start, min(left.end, right.end))


class RangeSet:
    def __init__(self, ranges: list[Range]) -> None:
        self.ranges = self._condense_ranges(ranges)

    @staticmethod
    def _condense_ranges(ranges: list[Range]) -> list[Range]:
        if not ranges:
            return []

        ranges = sorted(ranges, key=lambda r: r.start)

        condensed_ranges: list[Range] = [ranges[0]]

        for range in ranges[1:]:
            last_range = condensed_ranges[-1]
            if last_range.end >= range.start:
                condensed_ranges[-1] = Range(
                    last_range.start, max([last_range.end, range.end])
                )
            else:
                condensed_ranges.append(range)

        return condensed_ranges

    def __iter__(self) -> Iterator[Range]:
        return iter(self.ranges)
