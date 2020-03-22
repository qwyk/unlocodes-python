import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
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

def getCountryPage(countryCode, url):
    response = requests.get(url)
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

    return output[1:] #Ingore the first row, it has the header

if __name__ == '__main__':
    print('Fetching index...')
    countryIndex = getIndex('https://www.unece.org/cefact/locode/service/location')
    print('Fetched index', len(countryIndex), 'countries found')
    append = True
    start_from = 'AE'

    with open('raw_output.csv', 'a' if append else 'w', encoding='utf-8') as outputFile:
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
        for country in countryIndex:
            if country['countryCode'] == start_from:
                start = True
            if not start:
                continue
            print('Fetching', country['countryCode'])
            countryPageRecords = getCountryPage(country['countryCode'], country['pageUrl'])
            writer.writerows(countryPageRecords)
            print('Fetched country', country['countryCode'], len(countryPageRecords), 'places found and writen to file')
            total += len(countryPageRecords)
            sleep(1)
        print('Completed, writen ', total, 'places across', len(countryIndex), 'to raw_output.csv')