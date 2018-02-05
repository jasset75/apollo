import requests
import json

url = "http://localhost:5000/get-table"

payload = {
    "keyspace": "examples",
    "tablename": "mock_data",
    "filter": 'email like "%am%"',
    "sortby": [
        {"gender": "asc"},
        {"first_name": "asc"}
    ]
}

headers = {'content-type': 'application/json'}

response = requests.request("POST", url, data=json.dumps(payload),
                            headers=headers)

print(response.text)
