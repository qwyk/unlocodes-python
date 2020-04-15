import csv
from timezonefinder import TimezoneFinder
import argparse
import progressbar

IGNORED_CHANGE_INDICATORS = ['=']
INCLUDE_TIMEZONE = True
COUNTRIES = {}

def loadData(filename):
    headers = []
    output = []
    with open(filename, 'r', encoding='utf-8-sig') as headersFile:
        reader = csv.reader(headersFile)
        for row in reader:
            headers = row
            break

    with open(filename, 'r', encoding='utf-8-sig') as inputFile:
        reader = csv.DictReader(inputFile, fieldnames=headers)

        for index, row in enumerate(reader):
            if index == 0:
                continue
            output.append(row)
    return output

def lookupCountryName(code):
    return COUNTRIES[code] if code in COUNTRIES else code

def getCoordinates(string):
    if string.strip() == '':
        return (None, None, None, None)
    lat, lng = string.split(' ')

    north = lat[-1] ==  'N'

    east = lng[-1] ==  'E'

    latdec = int(lat[0:2]) + (int(lat[2:4]) / 60)
    if not north:
        latdec = 0-latdec
    lngdec = int(lng[0:3]) + (int(lng[3:5]) / 60)
    if not east:
        lngdec = 0-lngdec

    return lat, lng, round(latdec*100)/100, round(lngdec*100)/100

def convertRow(data, tzFinder):

    lat, lng, latdec, lngdec = getCoordinates(data['coordinates'])
    timezone = None
    if INCLUDE_TIMEZONE and latdec and lngdec:
        try:
            timezone = tzFinder.timezone_at(lat=latdec, lng=lngdec)
        except:
            pass

    return {
        "locode": data['locode'],
        "iata": data['iata'],
        "name": data['name'],
        "display_name": ', '.join([data['name'], data['subdivision']]) if data['subdivision'] != '' else data['name'],
        "name_wo_diacritics": data['name_without_diacritics'],
        "display_name_wo_diacritics": ', '.join([data['name_without_diacritics'], data['subdivision']]) if data['subdivision'] != '' else data['name_without_diacritics'],
        "subdivision": data['subdivision'],
        "country_code": data['country_code'],
        "country_name": lookupCountryName(data['country_code']),
        "is_port": '1' if '1' in data['function'] else '',
        "is_rail_terminal": '1' if '2' in data['function']  else '',
        "is_road_terminal": '1' if '3' in data['function']  else '',
        "is_airport": '1' if '4' in data['function'] else '',
        "is_postal_exchange": '1' if '5' in data['function'] else '',
        "is_icd": '1' if '6' in data['function'] else '',
        "is_fixed_transport": '1' if '7' in data['function'] else '',
        "is_borderxing": '1' if 'B' in data['function'] else '',
        "latitude_dms": lat,
        "longitude_dms": lng,
        "latitude_dec": latdec,
        "longitude_dec": lngdec,
        "timezone": timezone
    }


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help="the path of the raw unlocode input")
    parser.add_argument('output_file', type=str, help="path of file to write or append the data to")
    parser.add_argument('-tz', '--timezones', action='store_true', help="tries to add timezones (takes long)")

    return parser.parse_args()

if __name__ == '__main__':

    args = parseArguments()
    INCLUDE_TIMEZONE = args.timezones

    COUNTRIES = {x['code2']: x['name'] for x in loadData('iso3166.csv')}

    data = loadData(args.input_file)
    print(len(data), 'locations loaded from file')
    tzFinder = None
    if INCLUDE_TIMEZONE:
        tzFinder = TimezoneFinder()
    filtered = [row for row in data if row['change_indicator'] not in IGNORED_CHANGE_INDICATORS]
    with open(args.output_file, 'w', encoding='utf-8-sig') as file:
        index = True
        try:
            for row in progressbar.progressbar(filtered):
                output = convertRow(row, tzFinder)
                if index:
                    writer = csv.DictWriter(file, fieldnames = output.keys())
                    writer.writeheader()
                    index = False
                writer.writerow(output)
        except KeyboardInterrupt:
            print('stopped')
            exit()