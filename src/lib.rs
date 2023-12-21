use pyo3::{prelude::*, gc};


/// Simple unsendable pyclass with GC integration
/// - see https://pyo3.rs/v0.19.1/class/protocols.html#garbage-collector-integration
#[pyclass(unsendable)]
pub struct Unsendable {
    #[pyo3(set)]
    other: Option<Py<Self>>,
}
#[pymethods]
impl Unsendable {
    #[new]
    fn __new__() -> Self {
        Unsendable { other: None }
    }
    fn __traverse__(&self, visit: gc::PyVisit<'_>) -> Result<(), gc::PyTraverseError> {
        match &self.other {
            Some(obj) => visit.call(obj),
            _ => Ok(()),
        }
    }
    fn __clear__(&mut self) -> () {
        self.other = None;
    }
}

#[pymodule]
fn _lib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Unsendable>()?;
    Ok(())
}
