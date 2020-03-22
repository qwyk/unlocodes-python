import csv

IGNORE_CHANGE_INDICATORS = ['=']

def loadData(filename):
    headers = []
    output = []
    with open(filename, 'r', encoding='utf-8') as headersFile:
        reader = csv.reader(headersFile)
        for row in reader:
            headers = row
            break

    with open(filename, 'r') as inputFile:
        reader = csv.DictReader(inputFile, fieldnames=headers)

        for index, row in enumerate(reader):
            if index == 0:
                continue
            output.append(row)
    return output

def lookupCountryName(code):
    return code

def getCoordinates(string):
    if string.strip() == '':
        return (None, None)
    lat, lng = string.split(' ')

    north = lat[-1] ==  'N'
    print(north)
    east = lng[-1] ==  'E'
    print(east)

    print(lat, lng)
    latdec = None
    lngdec = None

    return lat, lng, latdec, lngdec

def convertRow(data):

    lat, lng, latdec, lngdec = getCoordinates(data['coordinates'])
    timezone = None
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
        "latitude_dev": latdec,
        "longitude_dec": lngdec,
        "timezone": timezone
    }


if __name__ == '__main__':
    data = loadData('raw_output.csv')
    print(len(data), 'locations loaded from file')
    output = [convertRow(row) for row in data[0:1] if row['change_indicator'] not in IGNORE_CHANGE_INDICATORS]
    print(output)
    exit()
    with open('database.csv', 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames = output[0].keys())
        writer.writeheader()
        writer.writerows(output)