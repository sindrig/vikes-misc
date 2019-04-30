import datetime
import locale
import os

from jinja2 import Environment, FileSystemLoader

try:
    locale.setlocale(locale.LC_TIME, 'is_IS')
except locale.Error:
    print('Could not set locale to is')

TEMPLATE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'templates',
)
environment = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True
)
now = datetime.datetime.now()


def dateformat(value, frmt='%a %d %b'):
    return value.strftime(frmt)


def timeformat(value, frmt='%H:%M'):
    return value.strftime(frmt)


environment.filters['dateformat'] = dateformat
environment.filters['timeformat'] = timeformat


def want_group(group_name):
    if group_name.startswith('Meistara'):
        return True
    elif group_name[0].isdigit():
        return int(group_name[0]) < 4
    return False


def filter_matches(matches):
    return [
        match for match in matches
        if want_group(match.group)
    ]


def upcoming_matches(all_matches):
    return reversed(filter_matches(
        [match for match in all_matches if match.date > now]
    )[-5:])


def past_matches(all_matches):
    return filter_matches(
        [
            match for match in all_matches
            if match.date < now and match.home_score and match.away_score
        ]
    )[:5]


def get_html(matches):
    return environment.get_template('matches.html').render(
        matches={
            module: (
                past_matches(module_matches),
                upcoming_matches(module_matches)
            )
            for module, module_matches in matches.items()
        },
        now=now,
    )
