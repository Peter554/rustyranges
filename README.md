# rustyranges

This repository benchmarks a few different implementations of ranges.

* [`xocto/ranges`](https://github.com/octoenergy/xocto/).
* `rustyranges` - a tiny ranges implementation in rust within the `src/` directory. 
  This is exposed as a python package via [maturin](https://www.maturin.rs) and [PyO3](https://github.com/PyO3/pyo3).
* `pysimpleranges` - a tiny ranges implementation in python within the `pysimpleranges/` directory, 
  almost identical to `rustyranges` in implementation.

The benchmarks are found within `tests/test_benchmarks.py`. 

The results:

```
--------------- benchmark 'range_init': 3 tests ----------------
Name (time in ms)                                 Mean
----------------------------------------------------------------
test_benchmark_range_init[pysimpleranges]      51.7537 (1.0)
test_benchmark_range_init[rustyranges]         79.6356 (1.54)
test_benchmark_range_init[xocto.ranges]       188.3826 (3.64)
----------------------------------------------------------------

--------------- benchmark 'range_intersection': 3 tests ----------------
Name (time in ms)                                         Mean
------------------------------------------------------------------------
test_benchmark_range_intersection[rustyranges]          8.5629 (1.0)
test_benchmark_range_intersection[pysimpleranges]      59.4437 (6.94)
test_benchmark_range_intersection[xocto.ranges]       266.8459 (31.16)
------------------------------------------------------------------------

--------------- benchmark 'range_read_start_and_end': 3 tests ---------------
Name (time in ms)                                              Mean
-----------------------------------------------------------------------------
test_benchmark_range_read_start_and_end[pysimpleranges]      1.4229 (1.0)
test_benchmark_range_read_start_and_end[xocto.ranges]        1.4871 (1.05)
test_benchmark_range_read_start_and_end[rustyranges]        35.3588 (24.85)
-----------------------------------------------------------------------------

---------------- benchmark 'rangeset_init': 3 tests ---------------
Name (time in ms)                                    Mean
-------------------------------------------------------------------
test_benchmark_rangeset_init[rustyranges]         10.3282 (1.0)
test_benchmark_rangeset_init[pysimpleranges]     108.7979 (10.53)
test_benchmark_rangeset_init[xocto.ranges]       466.8007 (45.20)
-------------------------------------------------------------------
```

## Running the code

* Install rust.
* Install [maturin](https://www.maturin.rs).
* Install [Taskfile](https://taskfile.dev/).
* Create and activate a python virtual environment (I used python 3.12).
* Install requirements: `task install-requirements`
* Run the benchmarks: `task bench`
