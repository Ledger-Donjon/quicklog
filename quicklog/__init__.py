import json
import os
import random
import datetime
import numpy as np
import re
from typing import Optional


def gen_rand_id() -> bytes:
    """:return: A randomly generated 64-bit identifier"""
    return random.randint(0, 0xFFFFFFFFFFFFFFFF).to_bytes(8, "big")


session_id = gen_rand_id()


def new_record() -> dict:
    """
    :return: new record dict with a generated random Id, the current session
        Id, and a timestamp.
    """
    rec = {
        "session": session_id.hex(),
        "id": gen_rand_id().hex(),
        "timestamp": datetime.datetime.now().timestamp(),
    }
    return rec


def is_valid_rid(rid: str) -> bool:
    """
    :return: True if given string is a valid record id, i.e. it is a lowercase
        hexadecimal string with at least 10 characters.

    This method is used as a sanity check since record ids are used to create
    files and folders in the traces database.
    """
    return (len(rid) >= 10) and (re.fullmatch(r"[0-9a-f]+", rid) is not None)


def get_trace_path(rid: str) -> str:
    """
    :return: Path of a trace in the database, given the record Id.

    :param rid: Record Id. Must be a lowercase hexadecimal string with at
        minimum 10 characters.

    This requires the environment variable `TRACESDIR` to be set.
    """
    assert is_valid_rid(rid)
    traces_dir = os.environ["TRACESDIR"]
    return os.path.join(
        traces_dir, rid[0:2], rid[2:4], rid[4:6], rid[6:8], rid[8:] + ".npy"
    )


def save_trace(record, trace, sample_rate=None, position=None):
    """
    Save given trace in the trace database using given record Id, and set
    trace properties to the current record.

    :param record: Current experiment record
    :param trace: Trace data
    :param sample_rate: Trace sample rate
    :param position: Acquisition horizontal position
    """
    traces_dir = os.environ["TRACESDIR"]
    rid = record["id"]
    assert is_valid_rid(rid)
    trace_dir = os.path.join(traces_dir, rid[0:2], rid[2:4], rid[4:6], rid[6:8])
    if not os.path.exists(trace_dir):
        os.makedirs(trace_dir)
    trace_path = os.path.join(trace_dir, rid[8:] + ".npy")
    if sample_rate is not None:
        record["trace.sample_rate"] = sample_rate
    if position is not None:
        record["trace.position"] = position
    np.save(trace_path, trace)


class Log:
    def __init__(self, path: str = "log", append=True):
        self.file = open(path, "ab" if append else "wb")

    def append(self, data: dict):
        """
        :param data: Log record data.
        """
        encoded = json.dumps(data)
        self.file.write((encoded + "\n").encode())

    def flush(self):
        """Flush log file to force write on disk."""
        self.file.flush()


def read_log(path: str = "log"):
    """
    Generator which yields everyline of a log file, parsing lines as JSON data.
    """
    for line in open(path, "r"):
        yield json.loads(line)
