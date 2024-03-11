import numpy
import quicklog


def do_experiment(i) -> str:
    return f"Result {i}"


def test_logging():
    log = quicklog.Log()
    for i in range(100):
        # new_record creates a dict with session Id, record Id and timestamp.
        record = quicklog.new_record()
        # create a random trace of 100 floats and save it.
        quicklog.save_trace(record, numpy.random.random(size=100))
        # Add experiment data
        record["result"] = do_experiment(record["id"])
        log.append(record)


def test_parsing():
    for record in quicklog.read_log():
        rid = record["id"]
        result = record["result"]
        assert result == do_experiment(rid)
        # To show the output with pytest, pass the "-s" argument
        print(f"{rid}: {result}")
