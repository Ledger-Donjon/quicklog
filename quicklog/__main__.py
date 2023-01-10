from . import *
import click
import json
import progressbar


@click.group()
def cli():
    pass


@cli.command(help="Show information about traces from a given log file")
@click.argument("log", type=click.File("r"))
def info(log):
    total_size = 0
    trace_count = 0
    existing = 0
    lines = log.readlines()
    for line in progressbar.progressbar(lines):
        record = json.loads(line)
        rid = record["id"]
        if is_valid_rid(rid):
            trace_count += 1
            trace_path = get_trace_path(rid)
            try:
                size = os.path.getsize(trace_path)
                total_size += size
                existing += 1
            except OSError as e:
                pass
    print(f"{len(lines)} records")
    print(f"{trace_count} traces")
    print(f"{existing} trace files found")
    size_gb = total_size / (1024**3)
    print(f"{size_gb:.3f} GB in traces database")


@cli.command(help="Delete traces recorded in a log file")
@click.argument("log", type=click.File("r"))
def rmtraces(log):
    confirmation = input("Delete traces from log? (y/n) ")
    if confirmation != "y":
        return
    total_size = 0
    count = 0
    lines = log.readlines()
    for line in progressbar.progressbar(lines):
        record = json.loads(line)
        rid = record["id"]
        if is_valid_rid(rid):
            trace_path = get_trace_path(rid)
            try:
                size = os.path.getsize(trace_path)
                os.remove(trace_path)
                count += 1
                total_size += size
            except OSError as e:
                pass
    print(f"{count} files removed")
    size_gb = total_size / (1024**3)
    print(f"{size_gb:.3f} GB freed")


if __name__ == "__main__":
    cli()
