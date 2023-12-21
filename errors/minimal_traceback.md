# Traceback for Minimal Reproducible Example

This file contains the traceback for the error as raised by the minimal working 
example. Note that some content has been redacted and replaced with `***`.

```
thread '<unnamed>' panicked at 'assertion failed: `(left == right)`
  left: `ThreadId(2)`,
 right: `ThreadId(1)`: unsendable_gc::Unsendable is unsendable, but sent to another thread!', ***\.cargo\registry\src\index.crates.io-6f17d22bba15001f\pyo3-0.19.2\src\impl_\pyclass.rs:927:9
stack backtrace:
   0: std::panicking::begin_panic_handler
             at /rustc/90c541806f23a127002de5b4038be731ba1458ca/library\std\src\panicking.rs:578
   1: core::panicking::panic_fmt
             at /rustc/90c541806f23a127002de5b4038be731ba1458ca/library\core\src\panicking.rs:67
   2: core::fmt::Arguments::new_v1
             at /rustc/90c541806f23a127002de5b4038be731ba1458ca/library\core\src\fmt\mod.rs:416
   3: core::panicking::assert_failed_inner
             at /rustc/90c541806f23a127002de5b4038be731ba1458ca/library\core\src\panicking.rs:268
   4: core::panicking::assert_failed<std::thread::ThreadId,std::thread::ThreadId>
             at /rustc/90c541806f23a127002de5b4038be731ba1458ca\library\core\src\panicking.rs:228
   5: pyo3::impl_::pyclass::impl$15::ensure<unsendable_gc::Unsendable>
             at ***\.cargo\registry\src\index.crates.io-6f17d22bba15001f\pyo3-0.19.2\src\impl_\pyclass.rs:927
   6: pyo3::pycell::impl$38::ensure_threadsafe<unsendable_gc::Unsendable>
             at ***\.cargo\registry\src\index.crates.io-6f17d22bba15001f\pyo3-0.19.2\src\pycell.rs:934
   7: pyo3::pycell::PyCell<unsendable_gc::Unsendable>::try_borrow<unsendable_gc::Unsendable>
             at ***\.cargo\registry\src\index.crates.io-6f17d22bba15001f\pyo3-0.19.2\src\pycell.rs:347
   8: pyo3::impl_::pymethods::_call_traverse<unsendable_gc::Unsendable>
             at ***\.cargo\registry\src\index.crates.io-6f17d22bba15001f\pyo3-0.19.2\src\impl_\pymethods.rs:270
   9: unsendable_gc::Unsendable::__pymethod_traverse__
             at ***\TestProjects\unsendable_gc\src\lib.rs:9
  10: Py_Get_Getpath_CodeObject
  11: Py_Get_Getpath_CodeObject
  12: Py_Get_Getpath_CodeObject
  13: Py_Get_Getpath_CodeObject
  14: PyCFunction_GetFlags
  15: PyVectorcall_Function
  16: PyObject_Call
  17: PyEval_GetFuncDesc
  18: PyEval_EvalFrameDefault
  19: PyEval_EvalFrameDefault
  20: PyFunction_Vectorcall
  21: PyCell_Set
  22: PyMethod_Self
  23: PyVectorcall_Function
  24: PyObject_Call
  25: PyOS_SigintEvent
  26: PyThread_init_thread
  27: configthreadlocale
  28: BaseThreadInitThunk
  29: RtlUserThreadStart
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
```