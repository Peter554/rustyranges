use pyo3::prelude::*;
use rust_decimal::Decimal;
use std::cmp::{max, min};

#[pyclass(frozen, eq, hash)]
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Range {
    #[pyo3(get)]
    start: Decimal,
    #[pyo3(get)]
    end: Decimal,
}

#[pymethods]
impl Range {
    #[new]
    fn new(start: Decimal, end: Decimal) -> Self {
        Self { start, end }
    }

    fn intersection(&self, other: &Self) -> Option<Self> {
        let (left, right) = if self.start <= other.start {
            (self, other)
        } else {
            (other, self)
        };
        if left.end <= right.start {
            None
        } else {
            Some(Self::new(right.start, min(left.end, right.end)))
        }
    }
}

#[pyclass]
#[derive(Debug, Clone)]
struct RangeIterator {
    ranges: Vec<Range>,
    idx: usize,
}

#[pymethods]
impl RangeIterator {
    fn __iter__(&self) -> Self {
        self.clone()
    }

    fn __next__(&mut self) -> Option<Range> {
        let range = self.ranges.get(self.idx);
        self.idx += 1;
        range.cloned()
    }
}

#[pyclass]
#[derive(Debug, Clone)]
struct RangeSet {
    #[pyo3(get)]
    ranges: Vec<Range>,
}

#[pymethods]
impl RangeSet {
    #[new]
    fn new(ranges: Vec<Range>) -> Self {
        Self {
            ranges: Self::condense_ranges(ranges),
        }
    }

    fn __iter__(&self) -> PyResult<RangeIterator> {
        Ok(RangeIterator {
            ranges: self.ranges.clone(),
            idx: 0,
        })
    }
}

impl RangeSet {
    fn condense_ranges(mut ranges: Vec<Range>) -> Vec<Range> {
        if ranges.is_empty() {
            return vec![];
        }

        ranges.sort_by_key(|r| r.start);
        let mut ranges = ranges.into_iter();

        // `with_capacity` or just `new` here? Depends how many overlaps we expect?
        let mut condensed_ranges: Vec<Range> = Vec::with_capacity(ranges.len());
        condensed_ranges.push(ranges.next().unwrap());

        for range in ranges {
            let last_range = condensed_ranges.last_mut().unwrap();
            if last_range.end >= range.start {
                last_range.end = max(last_range.end, range.end);
            } else {
                condensed_ranges.push(range)
            }
        }

        condensed_ranges
    }
}

#[pymodule]
fn rustyranges(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Range>()?;
    m.add_class::<RangeSet>()?;
    Ok(())
}
