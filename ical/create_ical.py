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


def main(inputfile, outputfile, name=None, event_parser=None):
    if event_parser is None:
        event_parser = EventParser()
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
        for event in event_parser.get_events(ws):
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
    summary = date_start = date_end = location = ''
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, header, row):
        for i, cell in enumerate(row):
            field = constants.get(header[i])
            if field:
                setattr(self, field, cell.value)
        self.validate()
        self.location = self.stadium
        self.summary = '%s - %s' % (self.home, self.away)
        self.date_start = datetime.datetime.combine(self.date, self.time)
        self.date_end = self.date_start + datetime.timedelta(hours=2)

    def __str__(self):
        return '%s - %s - %s - %s' % (
            self.summary,
            self.date_start,
            self.date_end,
            self.location,
        )

    def get_ical_event(self):
        event = Event()
        event.add('summary', self.summary)
        event.add('dtstart', self.date_start)
        event.add('dtend', self.date_end)
        event['location'] = self.location
        event.add('status', 'TENTATIVE')
        return event

    def validate(self):
        # We should have all constants now
        assert all([hasattr(self, field) for field in constants.values()])


class EventParser:
    def __init__(self, filter_by=None, event_edit=None):
        self.filter_by = filter_by
        self.event_edit = event_edit

    def get_events(self, ws):
        header = []
        events = []
        for row in ws.rows:
            if header:
                event = XlsxEvent(header, row)
                self.override_event_info(event)
                if self.include_event(event):
                    events.append(event)
                    print('include %s' % (event))
                else:
                    print('not include %s' % (event))
            else:
                header = [str(cell.value) for cell in row]
        return events

    def include_event(self, event):
        return not self.filter_by or eval(self.filter_by, {'self': event})

    def override_event_info(self, event):
        if self.event_edit:
            for edit in self.event_edit.split(';'):
                exec(edit, {'self': event, 'datetime': datetime})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile')
    parser.add_argument('outputfile')
    parser.add_argument('--name')
    parser.add_argument('--filter_by')
    parser.add_argument('--event_edit')
    args = parser.parse_args()
    assert args.outputfile.endswith('ics')
    event_parser = EventParser(args.filter_by, args.event_edit)
    main(
        args.inputfile,
        args.outputfile,
        name=args.name,
        event_parser=event_parser
    )
