import os
import sys
import datetime

import uploader
from vikes_result import ksi, hsi
from vikes_result.formatter import get_html
from vikes_result.utils import get_games

from result_page.generator import generate_page

RESULT_BUCKET = os.getenv('RESULT_BUCKET')


def create_result_box_page():
    f = datetime.datetime.now() - datetime.timedelta(days=30)
    t = datetime.datetime.now() + datetime.timedelta(days=30)
    games = get_games(f, t, hsi, ksi)
    uploader.upload_file(RESULT_BUCKET, 'index.html', get_html(games))


def create_result_page():
    html = generate_page()
    uploader.upload_file(RESULT_BUCKET, 'matchpage.html', html)


def handler(json_input, context):
    create_result_box_page()
    create_result_page()


if __name__ == '__main__':
    if 'create_result_page' in sys.argv:
        create_result_page()
    elif 'create_result_box_page' in sys.argv:
        create_result_box_page()
    else:
        handler(None, None)
