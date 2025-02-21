from dataclasses import dataclass


@dataclass
class FuzzyDateProfile:
    flat = "0"
    central = "1"
    slowStart = "2"
    slowFinish = "3"


@dataclass
class FuzzyDateDetermination:
    unknown = "0"
    attested = "1"
    conjecture = "2"
    measurement = "3"
