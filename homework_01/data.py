from dataclasses import dataclass


@dataclass
class Data:
    url: str
    time_list: list[float]
    count: int = 1
    count_perc: float = 0
    time_sum: float = 0
    time_perc: float = 0
    time_avg: float = 0
    time_max: float = 0
    time_med: float = 0

    def get_dict(self):
        return {"url": self.url,
                "count": self.count,
                "count_perc": f'{self.count_perc:.3f}',
                "time_sum": f'{self.time_sum:.3f}',
                "time_perc": f'{self.time_perc:.3f}',
                "time_avg": f'{self.time_avg:.3f}',
                "time_max": f'{self.time_max:.3f}',
                "time_med": f'{self.time_med:.3f}',
                }
