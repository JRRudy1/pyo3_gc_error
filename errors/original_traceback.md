# Traceback for Original Instance of the Error

This file contains the traceback for the error when I first experienced it 
during development of a (proprietary) Python library that involves interaction 
with both a Rust library (via `pyo3`) and an external program's Java API (via 
`jpype`). The sequence of events was kicked off by the `jpype` library, which
explicitly calls `GcCollect` from the worker thread where it starts the JVM.

Note that some content has been redacted and replaced with `***`.

```
Starting Java VM via JPype 1.4.1.
thread '<unnamed>' panicked at 'assertion failed: `(left == right)`
  left: `ThreadId(3)`,
 right: `ThreadId(1)`: *** is unsendable, but sent to another thread!', ***/.cargo/registry/src/index.crates.io-6f17d22bba15001f/pyo3-0.19.0/src/impl_/pyclass.rs:927:9
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
thread '<unnamed>' panicked at 'uncaught panic inside __traverse__ handler', ***/.cargo/registry/src/index.crates.io-6f17d22bba15001f/pyo3-0.19.0/src/impl_/panic.rs:25:9
stack backtrace:
   0:     0x7f7ec78b1d81 - std::backtrace_rs::backtrace::libunwind::trace::he648b5c8dd376705
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/../../backtrace/src/backtrace/libunwind.rs:93:5
   1:     0x7f7ec78b1d81 - std::backtrace_rs::backtrace::trace_unsynchronized::h5da3e203eef39e9f
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/../../backtrace/src/backtrace/mod.rs:66:5
   2:     0x7f7ec78b1d81 - std::sys_common::backtrace::_print_fmt::h8d28d3f20588ae4c
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/sys_common/backtrace.rs:65:5
   3:     0x7f7ec78b1d81 - <std::sys_common::backtrace::_print::DisplayBacktrace as core::fmt::Display>::fmt::hd9a5b0c9c6b058c0
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/sys_common/backtrace.rs:44:22
   4:     0x7f7ec78d87df - core::fmt::rt::Argument::fmt::h0afc04119f252b53
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/core/src/fmt/rt.rs:138:9
   5:     0x7f7ec78d87df - core::fmt::write::h50b1b3e73851a6fe
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/core/src/fmt/mod.rs:1094:21
   6:     0x7f7ec78af437 - std::io::Write::write_fmt::h184eaf275e4484f0
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/io/mod.rs:1714:15
   7:     0x7f7ec78b1b95 - std::sys_common::backtrace::_print::hf58c3a5a25090e71
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/sys_common/backtrace.rs:47:5
   8:     0x7f7ec78b1b95 - std::sys_common::backtrace::print::hb9cf0a7c7f077819
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/sys_common/backtrace.rs:34:9
   9:     0x7f7ec78b30c3 - std::panicking::default_hook::{{closure}}::h066adb2e3f3e2c07
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/panicking.rs:269:22
  10:     0x7f7ec78b2e54 - std::panicking::default_hook::h277fa2776900ff14
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/panicking.rs:288:9
  11:     0x7f7ec78b3649 - std::panicking::rust_panic_with_hook::hceaf38da6d9db792
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/panicking.rs:705:13
  12:     0x7f7ec78b3547 - std::panicking::begin_panic_handler::{{closure}}::h2bce3ed2516af7df
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/panicking.rs:597:13
  13:     0x7f7ec78b21e6 - std::sys_common::backtrace::__rust_end_short_backtrace::h090f3faf8f98a395
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/sys_common/backtrace.rs:151:18
  14:     0x7f7ec78b3292 - rust_begin_unwind
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/panicking.rs:593:5
  15:     0x7f7ec7713e33 - core::panicking::panic_fmt::h4ec8274704d163a3
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/core/src/panicking.rs:67:14
  16:     0x7f7ec788e588 - <pyo3::impl_::panic::PanicTrap as core::ops::drop::Drop>::drop::he8453f8e205dcbf5
  17:     0x7f7ec7749c71 - pyo3::impl_::pymethods::call_traverse_impl::hff81ecba4a16963d
  18:     0x5637de6dbc04 - subtract_refs
                               at /usr/local/src/conda/python-3.11.5/Modules/gcmodule.c:478:16
  19:     0x5637de6dbc04 - deduce_unreachable
                               at /usr/local/src/conda/python-3.11.5/Modules/gcmodule.c:1100:5
  20:     0x5637de6db137 - gc_collect_main
                               at /usr/local/src/conda/python-3.11.5/Modules/gcmodule.c:1226:5
  21:     0x5637de7a560b - gc_collect_with_callback
                               at /usr/local/src/conda/python-3.11.5/Modules/gcmodule.c:1400:14
  22:     0x5637de7d85f1 - PyGC_Collect
                               at /usr/local/src/conda/python-3.11.5/Modules/gcmodule.c:2086:13
  23:     0x7f7ec248c046 - _ZN19JPGarbageCollection9triggeredEv
  24:     0x7f7ec24968aa - Java_org_jpype_ref_JPypeReferenceNative_wake
  25:     0x7f7e9d00f9b0 - <unknown>
thread '<unnamed>' panicked at 'panic in a function that cannot unwind', library/core/src/panicking.rs:126:5
stack backtrace:
   0:     0x7f7ec78b1d81 - std::backtrace_rs::backtrace::libunwind::trace::he648b5c8dd376705
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/../../backtrace/src/backtrace/libunwind.rs:93:5
   1:     0x7f7ec78b1d81 - std::backtrace_rs::backtrace::trace_unsynchronized::h5da3e203eef39e9f
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/../../backtrace/src/backtrace/mod.rs:66:5
   2:     0x7f7ec78b1d81 - std::sys_common::backtrace::_print_fmt::h8d28d3f20588ae4c
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/sys_common/backtrace.rs:65:5
   3:     0x7f7ec78b1d81 - <std::sys_common::backtrace::_print::DisplayBacktrace as core::fmt::Display>::fmt::hd9a5b0c9c6b058c0
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/sys_common/backtrace.rs:44:22
   4:     0x7f7ec78d87df - core::fmt::rt::Argument::fmt::h0afc04119f252b53
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/core/src/fmt/rt.rs:138:9
   5:     0x7f7ec78d87df - core::fmt::write::h50b1b3e73851a6fe
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/core/src/fmt/mod.rs:1094:21
   6:     0x7f7ec78af437 - std::io::Write::write_fmt::h184eaf275e4484f0
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/io/mod.rs:1714:15
   7:     0x7f7ec78b1b95 - std::sys_common::backtrace::_print::hf58c3a5a25090e71
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/sys_common/backtrace.rs:47:5
   8:     0x7f7ec78b1b95 - std::sys_common::backtrace::print::hb9cf0a7c7f077819
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/sys_common/backtrace.rs:34:9
   9:     0x7f7ec78b30c3 - std::panicking::default_hook::{{closure}}::h066adb2e3f3e2c07
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/panicking.rs:269:22
  10:     0x7f7ec78b2e54 - std::panicking::default_hook::h277fa2776900ff14
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/panicking.rs:288:9
  11:     0x7f7ec78b3649 - std::panicking::rust_panic_with_hook::hceaf38da6d9db792
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/panicking.rs:705:13
  12:     0x7f7ec78b3501 - std::panicking::begin_panic_handler::{{closure}}::h2bce3ed2516af7df
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/panicking.rs:595:13
  13:     0x7f7ec78b21e6 - std::sys_common::backtrace::__rust_end_short_backtrace::h090f3faf8f98a395
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/sys_common/backtrace.rs:151:18
  14:     0x7f7ec78b3292 - rust_begin_unwind
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/std/src/panicking.rs:593:5
  15:     0x7f7ec7713e73 - core::panicking::panic_nounwind_fmt::h0f341873eb403cbf
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/core/src/panicking.rs:96:14
  16:     0x7f7ec7713f17 - core::panicking::panic_nounwind::h022979288a4bdd8f
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/core/src/panicking.rs:126:5
  17:     0x7f7ec7713fb3 - core::panicking::panic_cannot_unwind::h1503df11b6505c85
                               at /rustc/5680fa18feaa87f3ff04063800aec256c3d4b4be/library/core/src/panicking.rs:189:5
  18:     0x7f7ec7749c81 - pyo3::impl_::pymethods::call_traverse_impl::hff81ecba4a16963d
  19:     0x5637de6dbc04 - subtract_refs
                               at /usr/local/src/conda/python-3.11.5/Modules/gcmodule.c:478:16
  20:     0x5637de6dbc04 - deduce_unreachable
                               at /usr/local/src/conda/python-3.11.5/Modules/gcmodule.c:1100:5
  21:     0x5637de6db137 - gc_collect_main
                               at /usr/local/src/conda/python-3.11.5/Modules/gcmodule.c:1226:5
  22:     0x5637de7a560b - gc_collect_with_callback
                               at /usr/local/src/conda/python-3.11.5/Modules/gcmodule.c:1400:14
  23:     0x5637de7d85f1 - PyGC_Collect
                               at /usr/local/src/conda/python-3.11.5/Modules/gcmodule.c:2086:13
  24:     0x7f7ec248c046 - _ZN19JPGarbageCollection9triggeredEv
  25:     0x7f7ec24968aa - Java_org_jpype_ref_JPypeReferenceNative_wake
  26:     0x7f7e9d00f9b0 - <unknown>
thread caused non-unwinding panic. aborting.
Aborted (core dumped)
```