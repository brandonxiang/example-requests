import requests

url = 'http://www.baidu.com'
response = requests.get(url)
print response.content  # 网站内容
print response.status_code  # 状态码
print response.headers['content-type']  # header
print response.encoding  # 网页编码
