import os
import shutil
from operator import itemgetter
from os import name

from msgspec import json
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher
StealthyFetcher.adaptive = True
page = StealthyFetcher.fetch(
    'https://www.dofusbook.net/fr/equipement/22464401-db/objets',
    headless=True,
    network_idle=True
)

itemBlocks = page.xpath(
    '//*[@id="app"]/div/div/div[2]/div[4]/div[2]/div/div[1]/div/div[1]/div[2]/div/div/div'
)

equipmentName = str(page.css('.title > span')[0].text)

result = {
    'Name': equipmentName,
    'stats': [],
    'exo': [],
    'items': []
}

for img in itemBlocks[0].find_all('img'):
    result['items'].append({
        'name': str(img.attrib.get('alt'))
    })
    print(f"Item: {img.attrib.get('alt')}")

statsNamesElem = page.css('.label-stat')

ExoStatsNames = ['PA', 'PM', 'PO']

# statsNames = [elem.text for elem in statsNamesElem]
for elem in statsNamesElem:
    statsNames = str(elem.text)
    numberStatElem = elem.parent.css('.number-stat')
    statsValue = str(numberStatElem[0].text)
    result['stats'].append({
        'name': statsNames,
        'value': statsValue
    })

    if statsNames in ExoStatsNames:
        exoElem = elem.parent.parent.css('button')
        exoValue = str(exoElem[0].text)
        result['exo'].append({
            'name': statsNames,
            'value': exoValue
        })

# print("Done. Result:")
encoded_json = json.encode(result)
raw_json = json.format(encoded_json)
pretty_json = json.format(encoded_json, indent=4)
# print(pretty_json.decode('utf-8'))

# delete folder var/<equipmentName> if it exists, then recreate
folder_path = f"../var/{equipmentName}"
if os.path.exists(folder_path):
    shutil.rmtree(folder_path)
os.makedirs(folder_path)

# save inline.json and pretty.json
with open(f"{folder_path}/inline.json", 'wb') as f:
    f.write(encoded_json)
with open(f"{folder_path}/pretty.json", 'wb') as f:
    f.write(pretty_json)