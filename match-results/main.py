import os
import datetime

from vikes_result import ksi, hsi
from vikes_result.utils import get_games
from vikes_result.uploader import upload_matches

RESULT_BUCKET = os.getenv('RESULT_BUCKET')


def handler(json_input, context):
    f = datetime.datetime.now() - datetime.timedelta(days=30)
    t = datetime.datetime.now()
    hsi_games = get_games(hsi, f, t)
    ksi_games = get_games(ksi, f, t)
    upload_matches(RESULT_BUCKET, hsi_games + ksi_games)


if __name__ == '__main__':
    handler(None, None)
