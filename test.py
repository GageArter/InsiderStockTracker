import requests

try:
    url = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"
    r = requests.get(url)
    data = ("HTML:\n", r.text)
except:
    print("Invalid URL or some error occured while making the GET request to the specified URL")

import json
with open('personal.json', 'w') as json_file:
    json.dump(data, json_file)