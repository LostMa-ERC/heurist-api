import re
from dataclasses import dataclass


@dataclass
class LogDetail:
    time: str
    level: str
    recType: int
    recID: int
    rule: str
    problem: str

    @classmethod
    def load_lines(cls, *block_lines) -> "LogDetail":
        l1, l2, l3, l4, l5 = block_lines
        for indented_line in [l2, l3, l4, l5]:
            assert indented_line.startswith("\t")
        return LogDetail(
            time=cls.parse_time(l1),
            level=cls.parse_level(l1),
            recType=cls.parse_number(l2),
            recID=cls.parse_number(l3),
            rule=l4.removeprefix("\t").strip(),
            problem=l5.removeprefix("\t").strip(),
        )

    @staticmethod
    def parse_number(line) -> int:
        parts = line.split()
        suffix: str = parts[-1]
        number = suffix.removesuffix("]")
        return int(number)

    @staticmethod
    def parse_time(l1: str) -> str:
        parts = l1.split(" - ")
        return parts[0].strip()

    @staticmethod
    def parse_level(l1: str) -> str:
        return re.search(r"[A-Z]+", l1).group(0).strip()
