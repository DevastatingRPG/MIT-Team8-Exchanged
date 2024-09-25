import requests

url = "https://openexchangerates.org/api/latest.json?app_id=2fbd225cbccb4d96a22e643903910c84"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)