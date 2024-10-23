use pyo3::prelude::*;
use pyo3::types::PyAny;

mod subst;

#[pyclass]
struct RustTextIOWrapper {
    inner: Py<PyAny>,
    buffer: String,
}

#[pymethods]
impl RustTextIOWrapper {
    #[new]
    pub fn new(input: Py<PyAny>) -> Self {
        Self {
            inner: input,
            buffer: String::new(),
        }
    }

    #[pyo3(signature = (size=-1))]
    pub fn read<'p>(mut slf: PyRefMut<'p, Self>, py: Python<'p>, size: i32) -> PyResult<String> {
        loop {
            if size > 0 {
                let unsize = size as usize;
                if slf.buffer.len() >= unsize {
                    break;
                }
            }
            let result = slf.inner.call0(py)?;
            let py_str: &str = result.extract(py)?;
            if py_str.len() == 0 {
                break;
            }
            let resp = subst::substr(py_str);
            slf.buffer.push_str(resp.as_str());
        }
        if size > 0 {
            let resp = std::mem::replace(&mut slf.buffer, String::new());
            Ok(resp)
        } else {
            let unsize = size as usize;
            let unsize = unsize.min(slf.buffer.len());
            let resp = slf.buffer[..unsize].to_string();
            slf.buffer = slf.buffer[unsize..].to_string();
            Ok(resp)
        }
    }
    #[pyo3(signature = ())]
    pub fn readline<'p>(mut slf: PyRefMut<'p, Self>, py: Python<'p>) -> PyResult<String> {
        let result = slf.inner.call0(py)?;
        let py_str: &str = result.extract(py)?;
        let resp = subst::substr(py_str);
        slf.buffer.push_str(resp.as_str());
        let lastchar = slf.buffer.find('\n');
        match lastchar {
            Some(pos) => {
                let resp = slf.buffer[..pos + 1].to_string();
                slf.buffer = slf.buffer[pos + 1..].to_string();
                Ok(resp)
            }
            None => {
                let resp = std::mem::replace(&mut slf.buffer, String::new());
                Ok(resp)
            }
        }
    }

    pub fn __enter__<'p>(slf: PyRef<'p, Self>, _py: Python<'p>) -> PyResult<PyRef<'p, Self>> {
        Ok(slf)
    }

    pub fn __exit__(&mut self, _exc_type: PyObject, _exc_value: PyObject, _traceback: PyObject) {}
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
