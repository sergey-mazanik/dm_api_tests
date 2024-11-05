"""curl -X 'POST' \
  'http://5.63.153.31:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "smazanik",
  "email": "smazanik@gmail.com",
  "password": "123456"
}'"""
"""
curl -X 'PUT' \
  'http://5.63.153.31:5051/v1/account/83c7a049-5dc0-4031-b96d-adcc3f97fa4f' \
  -H 'accept: text/plain'
"""

import requests
from pprint import pprint
#
# url = 'http://5.63.153.31:5051/v1/account'
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json',
# }
# json = {
#     "login": "smazanik1",
#     "email": "smazanik1@gmail.com",
#     "password": "123456"
# }
#
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json
# )


url = 'http://5.63.153.31:5051/v1/account/11c0a9de-0415-45f0-8607-a59c0ea5c297'
headers = {
    'accept': 'text/plain'
}
json = {
    "login": "smazanik1",
    "email": "smazanik1@gmail.com",
    "password": "123456"
}
response = requests.put(
    url=url,
    headers=headers
)

print(response.status_code)
pprint(response.json())
response_json = response.json()
print(response_json['resource']['rating']['quantity'])




