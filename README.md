# QuickLog

QuickLog is a tiny Python3 library for logging experimental results. It uses JSON to serialize log records into human readable text files. Appending new records to a log file does not require parsing the current log data, making logging performance scallable. Parsing log results may however require some time, but complexity is O(n) where n is the number of records in the log file.

QuickLog also features trace save to a traces database (which is a structured directory). Each trace is referenced in the log file via a unique random identifier. For this, the `TRACESDIR` environment variable must refer to the traces database directory.

This library is meant to be very simple to use.

## Logging example

    import quicklog

    log = quicklog.Log()
    for i in range(100):
        # new_record creates a dict with session Id, record Id and timestamp.
        record = quicklog.new_record()
        # Add experiment data
        record['result'] = do_experiment()
        log.append(record)

## Parsing log example

    import quicklog

    for record in quicklog.read_log():
        rid = record['id']
        result = record['result']
        print(f'{rid}: {result}')

## Installation

Clone the repository then use pip3 to install the package.

    pip3 install quicklog

