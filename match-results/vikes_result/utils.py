import sys
import itertools
from multiprocessing.pool import ThreadPool

from .models import Game


def _get_games(module, f, t):
    result = module.client.service.FelogLeikir(
        FelagNumer=module.VIKES,
        DagsFra=f,
        DagsTil=t,
        FlokkurNumer='',
        VollurNumer='',
        Kyn=''
    )
    if hasattr(result, 'Villa'):
        print(result.Villa)
        sys.exit(1)
    return [
        Game(
            group=game.Flokkur,
            home_team=game.FelagHeimaNafn,
            away_team=game.FelagUtiNafn,
            home_score=game.UrslitHeima,
            away_score=game.UrslitUti,
            date=game.LeikDagur,
            competition=game.MotNafn,
            ground=game.VollurNafn,
        )
        for game in result.ArrayFelogLeikir.FelogLeikir
        if game.UrslitHeima and game.UrslitUti
    ]

def get_games(f, t, *modules):
    pool = ThreadPool(processes=1)
    async_results = [
        pool.apply_async(_get_games, (module, f, t))
        for module in modules
    ]
    games = [result.get(timeout=10) for result in async_results]
    return sorted(itertools.chain(*games), key=lambda x: x.date, reverse=True)
