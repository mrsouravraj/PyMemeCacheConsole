PyMemeCacheConsole
===================

A minimal Python library and CLI client for Memcached.

Features
--------
- Simple CLI: set/get and additional storage verbs (add, replace, append, prepend)
- Defaults to host=localhost and port=11211
- Works as a module runner or installed console script `pmcc`

Requirements
------------
- Python 3.10+
- A running Memcached server

Installation (dev)
------------------
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

Usage
-----
Run as a module without installing:
```bash
python -m pymemecacheconsole.cli -?              # help
python -m pymemecacheconsole.cli -H localhost -p 11211 set mykey myvalue
python -m pymemecacheconsole.cli --host localhost --port 11211 get mykey
```

After installing, use the `pmcc` command:
```bash
pmcc -?  
pmcc -H your.memcached.host -p 12121 set testkey testvalue
pmcc -H your.memcached.host -p 12121 get testkey
```

Notes
-----
- Keys with a trailing slash are trimmed automatically (e.g., `testkey/` -> `testkey`).
- For storage commands, the client prints the raw server response (`STORED`, `NOT_STORED`, etc.).
- For retrieval, values are printed as `key => value` or `(nil)` if not found.

Development
-----------
Run tests:
```bash
source .venv/bin/activate
pytest -q
```

Project Layout
--------------
```
pymemecacheconsole/
  __init__.py
  cli.py
  client.py
  protocol.py
  models.py
tests/
  test_protocol.py
  test_client.py
  test_cli.py
```

License
-------
MIT

# PyMemeCacheConsole