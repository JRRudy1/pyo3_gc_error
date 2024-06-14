# PyO3 Garbage Collection Error - Investigation and Minimal Example

This repository provides a minimal reproducible example of an error detected in 
PyO3's handling of unsendable pyclasses during garbage collection, details the 
sequence of events leading up to it, and presents a temporary workaround. An 
associated issue report was submitted to the PyO3 repository at 
https://github.com/PyO3/pyo3/issues/3688 and resolved in 
PR [#3689](https://github.com/PyO3/pyo3/pull/3689) by disabling the garbage 
collection of unsendable pyclasses when traversed on the wrong thread.


## Table of Contents
* [Introduction](#introduction)
* [Minimal Reproducible Example](#minimal-reproducible-example)
* [Investigation](#investigation)
  * [Conditions on the Python Side](#conditions-on-the-python-side)
  * [Error Sequence on the Rust Side](#error-sequence-on-the-rust-side)
* [Workaround](#workaround)
* [Discussion](#discussion)


## Introduction
I have discovered an error, or perhaps an undocumented limitation, in the way PyO3 
handles thread-checking for "unsendable" `pyclass` structs being traversed by 
Python's garbage collector (GC). In particular, this occurs when garbage collection 
is triggered from a separate thread, and the structs integrate with the GC by 
implementing the `__traverse__` magic method (see [Garbage Collector Integration](https://pyo3.rs/v0.19.1/class/protocols.html#garbage-collector-integration) 
in PyO3's docs). The error (or limitation) results in a hard abort, and is particularly 
problematic since it cannot be caught from Python using a `try`/`except` block.


## Minimal Reproducible Example
This repository contains a simple PyO3-based mixed Python/Rust project 
providing a minimal example of the error. The `main` function in 
[`python/unsendable_gc/__main__.py`](python/unsendable_gc/__main__.py) 
acts as the entry-point for the example, and is throughly commented to 
explain the error sequence.

The project may be installed into any Python 3.7+ environment by running `pip install .` 
from the repository root. The example may then be run to demonstrate the error using 
`python3 -m unsendable_gc`. To apply the workaround and avoid the error, simply add 
`-w` to the run command: `python3 -m unsendable_gc -w`.


## Investigation

### Conditions on the Python Side
1. Two or more objects of a `pyo3` pyclass are created on the main thread, where:
   - The pyclass is marked as "unsendable".
   - A reference cycle exists between these objects.
   - A `__traverse__` pymethod has been defined to walk the cycle.
2. All references outside the cycle are dropped, so:
   - The objects become "unreachable".
   - The GC is free to clean them up the next time it runs.
3. The objects are not garbage collected right away:
   - CPython makes no guarantees on when the GC will run, so we can't assume it will.
   - To model the case where it doesn't run, we can disable automatic garbage collection.
4. The garbage collector is triggered manually from a different thread:
   - It may be triggered by Python calls to the stdlib's `gc.collect` function,
     or by native calls to the C-API's `GcCollect` function.
   - This may be unavoidable if it occurs in upstream packages (`JPype` in my case)

### Error Sequence on the Rust Side
When the GC attempts to traverse the reference cycle and clean up these objects,
it ultimately calls back to Rust where `pyo3` checks whether they have been sent
between threads. This is done by comparing the ID of the calling thread (where
the GC was triggered from) to the ID of the original thread (where the objects
were first created). These will not match, so `pyo3` incorrectly assumes that
the objects were sent between threads and panics.

The (approximate) sequence of calls on the Rust side leading to the crash, with 
hyperlinks  to the relevant PyO3 source code, can be summarized as:
- [`__pymethod_traverse__`](https://github.com/PyO3/pyo3/blob/8bd29722017e51088e97112a8cebd658f61606c4/pyo3-macros-backend/src/pymethod.rs#L420)
- [`_call_traverse`](https://github.com/PyO3/pyo3/blob/8bd29722017e51088e97112a8cebd658f61606c4/src/impl_/pymethods.rs#L272)
- [`PyCell::try_borrow`](https://github.com/PyO3/pyo3/blob/8bd29722017e51088e97112a8cebd658f61606c4/src/pycell.rs#L348)
- [`PyCell::ensure_threadsafe`](https://github.com/PyO3/pyo3/blob/8bd29722017e51088e97112a8cebd658f61606c4/src/pycell.rs#L1025)
- [`ThreadCheckerImpl::ensure`](https://github.com/PyO3/pyo3/blob/8bd29722017e51088e97112a8cebd658f61606c4/src/impl_/pyclass.rs#L1048)
- `assert_eq!(thread::current().id(), self.0, "{} is unsendable, but sent to another thread", type_name)`

For the full call sequence leading to the crash, see the backtrace generated when 
running the example or those in the the `errors/*_traceback.md` files. 


## Workaround
The error can be avoided by explictly calling the garbage collector from the main 
thread to clean up the unsendable objects before starting the new thread. Call 
the `main` function with `workaround=True`, or append `-w` to the shell command, 
to apply the workaround and avoid the crash.


## Discussion
I am not entirely sure whether this would be classified as an error, an undocumented 
limitation, or something else. From a user's perspective, it feels like an error for 
a hard abort to be caused by sound code that doesn't break any (documented) rules. 
At best, the error message about "an unsendable object being sent between threads" 
is misleading, since nothing is being sent between threads; and if the GC call occurs 
in upstream code, then the cause of the error can be extremely difficult to identify.

One possible solution may be setting some sort of flag that causes the thread-check 
to be skipped during the GC cycle; however, I may not fully understand the possible 
implications of this. Perhaps certain (safe) `__traverse__` implementations could 
cause UB or memory leaks when triggered from a different thread? How would this 
interact with non-threadsafe types like `Rc` and `RefCell` that are not thread-safe?
Or, what if the object actually **was** illegally sent between threads during the 
sequence of events leading up to the crash as described in this project? If the 
thread-check were bypassed during the GC cycle, then this violation could go 
unnoticed.

If it is determined that `__traverse__` being called from another thread is inherently 
problematic and the issue cannot be fixed in PyO3, then at least the "Garbage Collector 
Integration" section of the documentation should be updated to mention the limitation 
and workaround. The error message should also be improved if it is practical to do so.
