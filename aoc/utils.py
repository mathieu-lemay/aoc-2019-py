#! /usr/bin/env python
import os


def _get_file_path(fn):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "input", fn)


def load_input(fn):
    with open(_get_file_path(fn)) as f:
        return f.read().strip()


def load_input_by_line(fn):
    with open(_get_file_path(fn)) as f:
        return [l.strip() for l in f.readlines()]


def split_list(lst: [], batch_size: int):
    for idx in range(0, len(lst), batch_size):
        yield lst[idx : idx + batch_size]
