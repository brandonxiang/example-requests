import requests

url = "http://abcde.com"
form = {'name': 'abc', 'password': '1234'}
response = requests.post(url, data=form)
print response.text
