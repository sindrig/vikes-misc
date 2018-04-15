import os

from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'templates',
)
environment = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True
)


def dateformat(value, frmt='%d-%m-%Y'):
    return value.strftime(frmt)


def timeformat(value, frmt='%H:%M'):
    return value.strftime(frmt)


environment.filters['dateformat'] = dateformat
environment.filters['timeformat'] = timeformat


def get_html(matches):
    return environment.get_template('matches.html').render(matches=matches)
