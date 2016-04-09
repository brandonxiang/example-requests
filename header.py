import requests

url = "http://www.baidu.com"
headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
response = requests.get(url,headers = headers)
print response.content