import os
import datetime

from vikes_result import ksi, hsi
from vikes_result.utils import get_games
from vikes_result.uploader import upload_matches

RESULT_BUCKET = os.getenv('RESULT_BUCKET')


def handler(json_input, context):
    f = datetime.datetime.now() - datetime.timedelta(days=30)
    t = datetime.datetime.now() + datetime.timedelta(days=30)
    games = get_games(f, t, hsi, ksi)
    upload_matches(RESULT_BUCKET, games)


if __name__ == '__main__':
    handler(None, None)
