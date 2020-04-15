from csv import DictReader, DictWriter

data = []
with open('output/database.csv', 'r', encoding='utf-8-sig') as file:
    reader = DictReader(file)
    for row in reader:
        data.append(row)

for index, row in enumerate(data):
    if row['country_code'] == 'CN' and row['name'][-3:] == ' Pt' and row['latitude_dms'] == '':
        key = row['name'][:-3] + row['subdivision'] + row['country_code']
        print(key)
        try:
            find = next((entry for entry in data if entry['name'] + entry['subdivision'] + entry['country_code'] == key))
            if find:
                print('Match')
                data[index]['latitude_dms'] = find['latitude_dms']
                data[index]['longitude_dms'] = find['longitude_dms']
                data[index]['timezone'] = find['timezone']
                data[index]['latitude_dec'] = find['latitude_dec']
                data[index]['longitude_dec'] = find['longitude_dec']
        except:
            print('No Match')
            pass
with open('output/database_cn_resolved.csv', 'w', encoding='utf-8-sig') as file:
    writer = DictWriter(file, fieldnames = data[0].keys())
    writer.writeheader()
    writer.writerows(data)