from pydantic import BaseModel, computed_field


class HistoricalDate(BaseModel):
    year: int
    month: int | None = None
    day: int | None = None

    @computed_field
    @property
    def iso(self) -> str:
        month = self.month or 1
        day = self.day or 1

        if self.year < 0:
            year_str = f"-{abs(self.year):04d}"
        else:
            year_str = f"{self.year:04d}"

        return f"{year_str}-{month:02d}-{day:02d}"

    def __str__(self) -> str:
        return self.iso