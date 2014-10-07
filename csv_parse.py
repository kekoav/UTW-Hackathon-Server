__author__ = 'kekoa'

import csv
import re

# "1st and 10 at BYU 45"
LOCATION_REGEX = re.compile(r'(?P<down>\d)[stndh]+ and (?P<distance>\d+) at (?P<team>.*) (?P<yard_line>\d+)')

def parse_data(filename):

    home_score = 0
    away_score = 0

    plays = []

    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        first_row = reader.next()

        for row in reader:
            dict = {}
            special_type = None
            type = None
            down = None
            distance = None

            for i in xrange(0, len(first_row)):
                key = first_row[i]
                value = row[i]

                if key == 'home_score':
                    if len(value) > 0:
                        home_score = int(value)

                    dict[key] = home_score

                elif key == 'away_score' and len(value) > 0:
                    away_score = int(value)

                    dict[key] = away_score

                elif key == 'result_description':

                    if value.lower().find('td') > 0:
                        special_type = 'touchdown'
                    if value.lower().find('fumble') > 0:
                        special_type = 'fumble'
                    if value.lower().find('kickoff') > 0:
                        type = 'kickoff'
                    if value.lower().find('pass') > 0:
                        type = 'pass'
                    if value.lower().find('run') > 0:
                        type = 'run'
                    if value.lower().find('punt') > 0:
                        type = 'punt'
                    if value.lower().find('safety') > 0:
                        special_type = 'safety'
                    if value.lower().find('1st down') > 0:
                        special_type = '1st_down'
                    if value.lower().find('timeout') > 0:
                        special_type = 'timeout'
                    if value.lower().find('touchback') > 0:
                        special_type = 'touchback'

                    dict[key] = value
                elif key == 'quarter' and len(value) > 0:
                    value = int(value)

                    dict[key] = value
                elif key == 'location_description':
                    # parse field location "1st and 10 at BYU 45"
                    result = LOCATION_REGEX.match(value)

                    if result:
                        value = result.groupdict()
                        down = int(value['down'])
                        distance = int(value['distance'])

                        team = value['team']
                        yard_line = int(value['yard_line'])

                        if team != 'BYU':
                            ## WARNING: hackathon hack -- byu is always the home team
                            yard_line *= -1

                        dict['yard_line'] = yard_line

                        # dict[key] = value
                else:
                    if key in ('posession'):
                        dict[key] = value

            if special_type:
                dict['special_type'] = special_type

            if down:
                dict['down'] = down
                dict['distance'] = distance

            dict['type'] = type


            plays.append(dict)

    print plays



if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        parse_data(sys.argv[1])
    else:
        print "ERROR: no filename given"