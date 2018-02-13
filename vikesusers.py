'''
Requires: ksi-stats
Usage:
    $ python main.py --teamid=103 --fromdate=1.1.2001 --todate=1.11.2009 \
        --flokkur=124 player_ids > ids.txt
    $ python main.py --teamid=103 --fromdate=1.1.2001 --todate=1.11.2009 \
        --flokkur=109 player_ids >> ids.txt
    $ python vikesusers.py ids.txt 1985 1990 > out.txt

Inputfile may now include the same player twice.
Result:
    A csv with "player_id_and_name; birthyear; minutes_played" for every
    player in inputfile (ids.txt) with minutes summed up that are
    born between 1985 and 1990 (inclusive) and played for the
    flokkar between fromdate and todate.

pdb is invoked if we can't find the birthyear of a player
'''
import argparse
from collections import defaultdict

import requests
from bs4 import BeautifulSoup


def main(inputfile, fromyear, toyear):
    d = defaultdict(int)
    with open(inputfile, 'r') as v:
        lines = v.readlines()
        for line in lines:
            key, m = line.split(': ')
            m = int(m)
            d[key] += m
    for k, v in d.items():
        id = k.split()[0]
        r = requests.get(
            'http://www.ksi.is/mot/motalisti/felagsmadur/',
            params={'pLeikmadurNr': id}
        )
        soup = BeautifulSoup(r.text, 'html.parser')
        for span in soup.find_all('span'):
            if span.previous.previous == 'Fæðingarár:':
                y = int(span.text)
                if 1985 <= y <= 1990:
                    print('%s; %s; %s' % (k, y, v))
                break
        else:
            import pdb; pdb.set_trace()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile')
    parser.add_argument('fromyear', type=int)
    parser.add_argument('toyear', type=int)
    args = parser.parse_args()
    main(args.inputfile, args.fromyear, args.toyear)
