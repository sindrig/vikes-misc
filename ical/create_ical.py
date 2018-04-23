import argparse
import datetime

import boto3
from openpyxl import load_workbook
from icalendar import Calendar, Event

constants = {
    'LEIKDAGUR': 'date',
    'KL': 'time',
    'MÓT': 'comp',
    'VÖLLUR': 'stadium',
    'HEIMALIÐ': 'home',
    'GESTIR': 'away',
}


def main(inputfile, outputfile, name=None):
    wb = load_workbook(inputfile)
    cal = Calendar()
    cal.add('version', '2.0')
    if name is None:
        name = input('Name of calendar: ')
    cal.add('name', name.strip())
    cal.add('x-wr-calname', name.strip())
    cal.add('x-wr-timezone', 'Atlantic/Reykjavik')
    cal.add('prodid', '-//Vikingur//Knattspyrnudeild//EN')
    for ws in wb.worksheets:
        for event in get_events(ws):
            cal.add_component(event.get_ical_event())
    if outputfile.startswith('s3://'):
        _, outputfile = outputfile.split('://')
        bucket, key = outputfile.split('/', 1)
        session = boto3.Session(profile_name='irdn')
        client = session.client('s3')
        client.put_object(
            Body=cal.to_ical(),
            Bucket=bucket,
            Key=key,
            ContentType='text/calendar'
        )
    else:
        with open(outputfile, 'wb') as f:
            f.write(cal.to_ical())


class XlsxEvent:
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, header, row):
        for i, cell in enumerate(row):
            field = constants.get(header[i])
            if field:
                setattr(self, field, cell.value)
        self.validate()

    def get_ical_event(self):
        event = Event()
        event.add('summary', self.get_summary())
        event.add('dtstart', self.get_date())
        event.add('dtend', self.get_date() + datetime.timedelta(hours=2))
        event['location'] = self.get_location()
        return event

    def validate(self):
        # We should have all constants now
        assert all([hasattr(self, field) for field in constants.values()])

    def get_location(self):
        return self.stadium

    def get_summary(self):
        return '%s - %s' % (self.home, self.away)

    def get_date(self):
        return datetime.datetime.combine(self.date, self.time)
        # date = 2018-04-28 00:00:00
        # time = 18:00:00
        # date = self.date.split(' ')[0]
        # dtstring = '%s %s' % (date, self.time)
        # return datetime.datetime.strptime(dtstring, self.DATE_FORMAT)


def get_events(ws):
    header = []
    events = []
    for row in ws.rows:
        if header:
            events.append(XlsxEvent(header, row))
        else:
            header = [str(cell.value) for cell in row]
    return events


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile')
    parser.add_argument('outputfile')
    parser.add_argument('--name')
    args = parser.parse_args()
    assert args.outputfile.endswith('ics')
    main(args.inputfile, args.outputfile, name=args.name)
