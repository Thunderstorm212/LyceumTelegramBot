import time
from utils import Colors


class ProgressBar:
    def __init__(self, current, total, bar_length=20, fill='█', non_fill='░', color="#000000"):
        self.fill = Colors(fill, color)
        self.progress = int(current / total * bar_length)
        self.percent = int(current / total * 100)
        self.bar = '▌' + fill * self.progress + non_fill * (bar_length - self.progress) + '▐'
        print(f'\r{self.percent}% {self.bar}', end='', flush=True)


def progress_bar(current, total, bar_length=20, fill='█'):
    progress = int(current / total * bar_length)
    percent = int(current / total * 100)
    bar = '▌' + fill * progress + '░' * (bar_length - progress) + '▐'
    print(f'\r{percent}% {bar}', end='', flush=True)


class StatusBar:
    def __init__(self, text, status_range: int):
        fill_list = ["⠃", "⠆", "⠤", "⠰", "⠘", "⠉"]
        for i in range(status_range):
            for j in fill_list:
                time.sleep(0.2)
                print(f"\r{text}", j, end='', flush=True)


#
# total = 100
# for i in range(total + 1):
#     time.sleep(0.1)
#     ProgressBar(i, total)
