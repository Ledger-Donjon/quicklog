# QuickLog

QuickLog is a tiny Python3 library for logging experimental results. It uses JSON to serialize log records into human readable text files. Appending new records to a log file does not require parsing the current log data, making logging performance scallable. Parsing log results may however require some time, but complexity is $O(n)$ where n is the number of records in the log file.

QuickLog also features trace save to a traces database (which is a structured directory). Each trace is referenced in the log file via a unique random identifier. For this, the `TRACESDIR` environment variable should refer to the traces database directory. If this environment variable is not defined,
`./traces` directory is used.

This library is meant to be very simple to use.

## Logging example

```python
import quicklog

log = quicklog.Log()
for i in range(100):
    # new_record creates a dict with session Id, record Id and timestamp.
    record = quicklog.new_record()
    # Add experiment data
    record['result'] = do_experiment()
    log.append(record)
```

## Parsing log example

```python
import quicklog

for record in quicklog.read_log():
    rid = record['id']
    result = record['result']
    print(f'{rid}: {result}')
```

## Installation

Quicklog is available on pypi. You can install it with `pip3`:

```bash
pip3 install donjon-quicklog
```

If you want to install the latest version from the repository,
clone the repository then use `pip3` to install the package.

```bash
pip3 install ./quicklog
```

## Licensing

Quicklog is released under GNU Lesser General Public Licence version 3 (LGPLv3).
See [COPYING](COPYING) and [COPYING.LESSER](COPYING.LESSER) for license details.
