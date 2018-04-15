import datetime

from vikes_result import ksi, hsi
from vikes_result.utils import get_games

if __name__ == '__main__':
    f = datetime.datetime.now() - datetime.timedelta(days=30)
    t = datetime.datetime.now()
    hsi_games = get_games(hsi, f, t)
    ksi_games = get_games(ksi, f, t)
    print(hsi_games)
    print(ksi_games)
