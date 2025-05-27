from typing import Generator

from .model import LogDetail


def yield_log_blocks(lines: list[str]) -> Generator[LogDetail, None, None]:
    line_iterator = iter(lines)
    l1 = next(line_iterator, None)
    while l1 is not None:
        if l1 and not l1.startswith("\t"):
            l2 = next(line_iterator)
            l3 = next(line_iterator)
            l4 = next(line_iterator)
            l5 = next(line_iterator)
            yield LogDetail.load_lines(l1, l2, l3, l4, l5)
        l1 = next(line_iterator, None)
