# matrix-include-trace

Expand bounded literal axes and emit a provenance trace for exclusions, merges into originals and independent appended combinations.

## User and task

CI maintainers reviewing how literal matrix includes and excludes change job coverage. An include can overwrite an earlier added value while being forbidden to overwrite original axes; appended jobs are not merged by later includes.

## Install and first useful result

Python 3.10+ and pip. Git source install; no external-registry release is claimed.

```sh
git clone https://github.com/nripankadas07/matrix-include-trace.git
cd matrix-include-trace
python -m venv .venv
# POSIX: . .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install .
matrix-include-trace example.json
```

The example excludes windows/python3.14, adds coverage to the three originals, overwrites it on linux only and appends one macos/python3.14 job: four jobs total. The example is synthetic. JSON goes to stdout. Exit0 means analyzed with no review findings; exit 1 means review findings; exit 2 means malformed/unsupported input or an IO error. Differences explicitly labeled informational do not alone trigger exit 1. Help: `matrix-include-trace --help`.

## Input contract

Required axes object with up to8 axes; optional include/exclude arrays up to256 objects each. Axis lists are nonempty with up to32 distinct scalar values. Scalars: null, boolean, signed64-bit integer or string<=256 characters. Types compare distinctly. Axis/key names use ASCII letters/underscore followed by letters/digits/underscore/hyphen, up to64 characters. Object values, floats, duplicate axis values and expression syntax are unsupported. Original product and expanded jobs are each capped at256. Exclude entries must be nonempty and name existing axes; partial objects match originals before includes. Includes merge only into surviving original rows if original values are not overwritten; added values can be overwritten by later includes. Entries incompatible with every surviving original become independent appended jobs, never later merge targets. Empty axes with nonempty include supports include-only matrices.

Every object rejects unknown keys. CLI input is UTF-8 JSON, read with a 2 MiB cap before parsing; duplicate keys/nonfinite values fail. Default arrays allow at most 512 entries, strings1..256 characters and nonnegative integers up to2^63-1 except where a tighter/different bound is documented. The example shows the complete input shape. JSON output includes the supplied identities; review it before sharing sensitive inputs.

## Validate

```sh
python -m unittest -v
python -m compileall -q matrix_include_trace.py
python -m pip wheel --no-deps --wheel-dir dist .
python -m venv /tmp/matrix-include-trace-installed
/tmp/matrix-include-trace-installed/bin/python -m pip install --no-index --no-deps dist/*.whl
python test_installed_cli.py /tmp/matrix-include-trace-installed/bin/python
```

The last commands show the Linux/POSIX path; use the equivalent Scripts/python.exe path on Windows. Remote configured CI uses Linux Python 3.10/3.12/3.14. [Validation](VALIDATION.md) records actual preparation checks and limits; a workflow configuration is not itself proof of a passing run.

## Scope and limitations

Literal JSON subset only, not YAML or a complete GitHub Actions evaluator. No expressions, object axes, reusable workflows, job if/needs, runner resolution, fail-fast, concurrency, secret handling or execution. Exact scalar typing and rejected duplicate axes are declared limits; do not treat this as a platform conformance certificate.

No runtime third-party packages. Setuptools is a build dependency. Original implementation developed with AI assistance, MIT licensed; no competitor code, prose or branding copied. [Research](RESEARCH.md), [contribution](CONTRIBUTING.md), [support](SUPPORT.md) and [security](SECURITY.md) guidance are included.
