from dataclasses import asdict, dataclass


@dataclass
class BaseFilter:
    def filter_criteria(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}
