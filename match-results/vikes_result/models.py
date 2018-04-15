from collections import namedtuple

Game = namedtuple(
    'Game',
    ('group', 'home_team', 'away_team', 'home_score', 'away_score', 'date')
)
