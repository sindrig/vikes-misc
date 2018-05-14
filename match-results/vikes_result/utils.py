import sys
from multiprocessing.pool import ThreadPool

from .models import Game


def _get_games(module, f, t, FelagNumer=None):
    result = module.client.service.FelogLeikir(
        FelagNumer=FelagNumer or module.VIKES,
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
            sex=game.MotKyn,
        )
        for game in result.ArrayFelogLeikir.FelogLeikir
    ]


def get_games(f, t, *modules):
    pool = ThreadPool(processes=1)
    async_results = {
        module: pool.apply_async(_get_games, (module, f, t))
        for module in modules
    }
    return {
        module: sorted(
            result.get(timeout=10),
            key=lambda x: x.date,
            reverse=True
        )
        for module, result in async_results.items()
    }
