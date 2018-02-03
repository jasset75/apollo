import requests

url = "http://localhost:5000/get-table"

payload = "{\n\t\"keyspace\": \"examples\",\n\t\"tablename\":\"mock_data\",\n\t\"filter\": \"email like \\\"%am%\\\"\",\n\t\"sortby\": [\n\t\t{\"gender\": \"asc\"},\n\t\t{\"first_name\": \"asc\"}\n\t]\n}"
headers = {'content-type': 'application/json'}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)