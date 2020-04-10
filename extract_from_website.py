import csv
from time import sleep
import sys
import requests
from bs4 import BeautifulSoup
import argparse


def getIndex(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='contenttable')
    if not table:
        raise Exception('Content table at index page not found')

    rows = table.find('thead').find_all('tr')

    index = []

    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 1:
            countryCode  = cells[0].text
            linkElement = cells[1].find('a')
            if linkElement:
                index.append({"countryCode": countryCode, "pageUrl": linkElement['href']})

    return index


def getCountryPage(countryCode, url, tries=2):
    try:
        with requests.get(url) as response:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', height=None) # The table without an height element set holds the records
            if not table:
                print('Table not found for', countryCode, 'at', url)

            output = []
            for row in table.find_all('tr'):
                tableRow = [countryCode]
                for cell in row.find_all('td'):
                    tableRow.append((''.join(list(cell.stripped_strings))).replace(u'\xa0', ''))
                output.append(tableRow)
            return output[1:] #Ignore the first row, it has the header
    except:
        print('Failed to get {} with error: {}'.format(countryCode, sys.exc_info()[0]))
        if tries > 0:
            print('Retrying {} in 2 seconds'.format(countryCode))
            sleep(2)
            tries -=1
            return getCountryPage(countryCode, url, tries)
        else:
            print('Failed to fetch {} after multiple tries, upon completion you can run this script again with the --only argument to retry.'.format(countryCode))
            return None



def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_file', type=str, help="path of file to write or append the data to, without extension")
    parser.add_argument('-a', '--append', type=str, help="the 2 letter code for the country from which to start appending")
    parser.add_argument('-o', '--only', type=str, help="comma seperated 2 letter codes to append")
    return parser.parse_args()

if __name__ == '__main__':
    args = parseArguments()
    filename = args.output_file
    append = args.append is not None
    only = args.only is not None

    if append and only:
        raise Exception('--append and --only are mutually exclusive')


    startFrom = args.append

    if append and len(startFrom) != 2:
        raise Exception('Append must be 2 letter country code: {} is not valid'.format(startFrom ))

    onlyCountries = args.only
    if only:
        onlyCountries = onlyCountries.split(',')
        for i in onlyCountries:
            if len(i) != 2:
                raise Exception('Only must contain 2 letter country codes delimited by a comma: {} is not valid'.format(i))

    print('Fetching index...')
    countryIndex = getIndex('https://www.unece.org/cefact/locode/service/location')
    print('Fetched index', len(countryIndex), 'countries found')

    args = sys.argv



    with open(filename, 'a' if append else 'w', encoding='utf-8') as outputFile:
        writer =csv.writer(outputFile)
        if not append:
            writer.writerow([
                'country_code',
                'change_indicator',
                'locode',
                'name',
                'name_without_diacritics',
                'subdivision',
                'function',
                'status',
                'date',
                'iata',
                'coordinates',
                'remarks'
            ])
        total = 0
        start = not append
        countriesRun = 0
        failed = []
        for country in countryIndex:
            if country['countryCode'] == startFrom:
                start = True
            if not start:
                continue
            if only and country['countryCode'] not in onlyCountries:
                continue
            print('Fetching', country['countryCode'])
            countryPageRecords = getCountryPage(country['countryCode'], country['pageUrl'])
            if countryPageRecords:
                writer.writerows(countryPageRecords)
                print('Fetched country', country['countryCode'], len(countryPageRecords), 'places found and writen to file')
                total += len(countryPageRecords)
                countriesRun += 1
            else:
                failed.append(country)
            sleep(2)

        print("Completed, written {} places across {} countries to {}".format(total, countriesRun, filename))
        if len(failed) > 0:
            print("Failed for {}".format(', '.join(failed)))
