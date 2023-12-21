"""Minimal reproducible example of the garbage collection error."""
import gc
import sys
import threading

# `Unsendable` is a simple `pyo3` pyclass marked as "unsendable". This pyclass
# has a single field `other` that contains an optional `Py` reference to another
# `Unsendable` object, and standard implementations for the `__traverse__` and
# `__clear__` magic methods (see `src/lib.rs`).
from unsendable_gc._lib import Unsendable


def main(workaround=False):

    # Disable auto-GC so we control when it runs
    gc.disable()

    # Create two unsendable objects in a reference cycle. The `__traverse__` and
    # `__clear__` methods will be called when the objects are garbage collected.
    obj1, obj2 = Unsendable(), Unsendable()
    obj1.other = obj2
    obj2.other = obj1

    # Delete the local references to the objects such that only the cyclic
    # references remain and the objects are "unreachable".
    del obj1, obj2

    # Avoid the error by manually collecting garbage on the main thread. In a real
    # program (with the GC enabled), this step may or may not happen automatically.
    if workaround:
        gc.collect()

    # Trigger a GC cycle from a new thread. If a GC cycle has not occurred
    # to clean up the `Unsendable` objects yet, `pyo3` will think they were
    # sent between threads and cause the program to abort.
    threading.Thread(target=gc.collect).start()


if __name__ == '__main__':
    main(workaround='-w' in sys.argv)
