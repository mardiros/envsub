use pyo3::prelude::*;
use pyo3::types::PyAny;

mod subst;

#[pyclass]
struct RustTextIOWrapper {
    inner: Py<PyAny>,
}

#[pymethods]
impl RustTextIOWrapper {
    #[new]
    pub fn new(input: Py<PyAny>) -> Self {
        Self { inner: input }
    }

    fn read<'p>(slf: PyRef<'p, Self>, py: Python<'p>, _size: i32) -> PyResult<String> {
        let result = slf.inner.call0(py)?;
        let py_str: &str = result.extract(py)?;
        Ok(subst::substr(py_str))
    }

    fn __enter__<'p>(slf: PyRef<'p, Self>, _py: Python<'p>) -> PyResult<PyRef<'p, Self>> {
        Ok(slf)
    }

    fn __exit__(&mut self, _exc_type: PyObject, _exc_value: PyObject, _traceback: PyObject) {}
}

#[pyfunction]
fn sub<'py>(py: Python<'py>, input: Py<PyAny>) -> PyResult<RustTextIOWrapper> {
    let read_line: Py<PyAny> = input.getattr(py, "readline")?.into();
    let res = RustTextIOWrapper::new(read_line);
    Ok(res)
}

#[pymodule]
fn envsub(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sub, m)?)?;
    Ok(())
}
