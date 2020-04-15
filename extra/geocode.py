import googlemaps
from pprint import pprint
from csv import DictReader, DictWriter
from timezonefinder import TimezoneFinder
from time import sleep
import sys
data = []
with open('output/database_geocoded.csv', 'r', encoding='utf-8-sig') as file:
    reader = DictReader(file)
    for row in reader:
        if 'tried_geocoding' not in row:
            row['tried_geocoding'] = False
        else:
            row['tried_geocoding'] = row['tried_geocoding'] == 'TRUE'
        data.append(row)




gmaps = googlemaps.Client(key=None)
tzFinder = TimezoneFinder()

countriesWeCareAbout = ['US'] #['BE', 'FR', 'NL', 'DE', 'SG', 'HK'] # , 'DE', 'CN', 'SG', 'HK', 'US', 'NL', 'BE']
placesWeCareAbout = ['CATOR', 'CAVAN', 'CAMTR', 'USDFW', 'USDET', 'USSEA', 'USLAX', 'USSFO', 'USEWR', 'USSFO']
counter = 0
with open('output/database_geocoded.csv', 'w', encoding='utf-8-sig') as file:
    writer = DictWriter(file, fieldnames = data[0].keys())
    writer.writeheader()

    for i, row in enumerate(data):
        try:

            if row['locode'] in placesWeCareAbout and row['latitude_dec'] == '' and not row['tried_geocoding']: # and row['is_port'] == '1' and row['is_airport'] == '1':
                counter += 1
                row['tried_geocoding'] = True
                geocode_results= gmaps.geocode(row['name_wo_diacritics'] + ', ' + row['subdivision'] + ', ' + row['country_name'])
                if len(geocode_results) > 0:
                    result = geocode_results[0]
                    if 'geometry' in result and 'location' in result['geometry']:
                        lat = result['geometry']['location']['lat']
                        lng = result['geometry']['location']['lng']
                        row['latitude_dec'] = lat
                        row['longitude_dec'] = lng
                        try:
                            timezone = tzFinder.timezone_at(lat=lat, lng=lng)
                            row['timezone'] = timezone
                        except:
                            pass

                print(str(counter).zfill(5), row['locode'])
                sleep(0.5)
            writer.writerow(row)
        except:
            writer.writerow(row)
            print(sys.exc_info()[0])