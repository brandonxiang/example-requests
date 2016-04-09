##Python 笔记七：Requests爬虫技巧

-------------------------------------

> 源码github地址在此，记得点星：
https://github.com/brandonxiang/requests-example

这篇笔记的灵感来自[Python爬虫：一些常用的爬虫技巧总结](http://my.oschina.net/jhao104/blog/647308?fromerr=LEc4jbps)，我这篇笔记也算是一篇山寨笔记，文中会大量引用他人文章。原因很简单，因为该文条理清晰，言简意赅。唯一一点我不太满意就是现在python的爬虫技巧应该专注于`Requests`和`BeautifulSoup`这样的第三方库。这两个库确实成为了python爬虫的**标配**，更符合python语法简洁的特点，替代了`urllib`和`re`等复杂的**老式爬虫手段**，可以说是，前所未有地实现了爬虫的快速开发模型。关于Requests的具体用法可以参考[官网](http://cn.python-requests.org/zh_CN/latest/)。

希望这篇文章也能给大家一个简单的认识，python就像一个**瑞士军刀**，而让爬虫这种本来繁琐的动作变得简单。


### 基本抓取网页
####get方法
```
import requests

url = 'http://www.baidu.com'
response = requests.get(url)
print response.content  # 网站内容
print response.status_code  # 状态码
print response.headers['content-type']  # header
print response.encoding  # 网页编码
```
####post方法
```
import requests

url = "http://abcde.com"
form = {'name': 'abc', 'password': '1234'}
response = requests.post(url, data=form)
print response.text
```
### 使用代理IP
>在开发爬虫过程中经常会遇到IP被封掉的情况，这时就需要用到代理IP

这个可以参考[python的扩展包requests的高级用法](http://www.ziliao1.com/Article/Show/05534046411C9B8866742DE312F126CB.html)

```
import requests

url = "http://www.baidu.com"
proxies = {
  "http": "http://10.10.1.10:3128",
  "https": "http://10.10.1.10:1080",
}
response = requests.get(url, proxies=proxies)
print response.content
```
###Cookies处理
> cookies是某些网站为了辨别用户身份、进行session跟踪而储存在用户本地终端上的数据(通常经过加密)

你可以提前用`Chrome Dev Tool`去获取对应的cookie，将其输入到该参数当中。`requests`自带`session`。

```
import requests

session = requests.Session()
response = session.get('http://httpbin.org/cookies', cookies={'from-my': 'browser'})
print(response.text)
```

###伪装成浏览器
>  某些网站反感爬虫的到访，于是对爬虫一律拒绝请求。所以用urllib2直接访问网站经常会出现HTTP Error 403: Forbidden的情况
对有些 header 要特别留意，Server 端会针对这些 header 做检查
  1.User-Agent 有些 Server 或 Proxy 会检查该值，用来判断是否是浏览器发起的 Request
  2.Content-Type 在使用 REST 接口时，Server 会检查该值，用来确定 HTTP Body 中的内容该怎样解析。

通过header让requests的程序去伪装浏览器，或者该网页的环境，可以有效避免服务器拒绝和跨域限制。

```
import requests

url = "http://www.baidu.com"
headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
response = requests.get(url,headers = headers)
print response.content
```

###页面解析

页面解析的最传统方法--正则表达式，参考[正则表达式入门](http://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html) 和[正则表达式在线测试](http://tool.oschina.net/regex/) 。关于解析库，有[lxml](http://my.oschina.net/jhao104/blog/639448)和[BeautifulSoup](http://cuiqingcai.com/1319.html)，他们的教程有很多，前者还是涉及到正则表达式 。
对于我再说，我不是大牛，想个正则表达式都要半天。还是用Beautifulsoup纯python实现，效率低，但是开发效率高，让电脑慢慢来吧。

### 验证码的处理

对于复杂的验证码识别可能有点难度，但是，简单的图形识别还是十分容易的，有兴趣的童鞋，请参考[Python验证码识别：利用pytesser识别简单图形验证码](http://mp.weixin.qq.com/s?__biz=MzA4MjEyNTA5Mw==&mid=404976285&idx=2&sn=3f3468cbcde49e7b905fb959b12d9781&scene=1&srcid=0331HhwonQhoinOiEDfXPEzE&from=singlemessage&isappinstalled=0#wechat_redirect)。

### gzip压缩
> 有没有遇到过某些网页，不论怎么转码都是一团乱码。哈哈，那说明你还不知道许多web服务具有发送压缩数据的能力，这可以将网络线路上传输的大量数据消减 60% 以上。这尤其适用于 XML web 服务，因为 XML 数据 的压缩率可以很高。

其实网页压缩有两种，一种是deflate，另一种是gzip。deflate已经在淘汰的边缘，但是国内一些老网站还在使用。具体请参考我的另一篇文章--[6入门爬虫坑--网页数据压缩(python deflate gzip)](http://www.jianshu.com/p/2c2781462902)。

###总结

该笔记描述那么多方面，好像只是讲了`requests`模块的参数而已。这也说明了它的强大，但是前提是你必须懂对应的原理。参数如下：

- json: json数据传到requests的body
- headers: HTTP Headers的字典传到requests的header 
- cookies: 可以使用字典或者CookieJar object
- files: 字典`{'name': file-tuple}` 来实现multipart encoding upload, 2参数元组 `('filename', fileobj)`, 3参数元组 `('filename', fileobj, 'content_type')`或者 4参数元组 `('filename', fileobj, 'content_type', custom_headers)`, 其中`'content-type'` 用于定于文件类型和`custom_headers`文件的headers
- auth: Auth元组定义用于Basic/Digest/Custom HTTP Auth
- timeout: 连接等待时长
- allow_redirects: 布尔型， True代表POST/PUT/DELETE只有的重定向是允许的
- proxies: 代理的地址
- verify: 用于认证SSL证书
- stream: `False`代表返回内容立刻下载
- cert: String代表ssl client证书地址(.pem) Tuple代表('cert', 'key')键值对

参考：
[Python爬虫学习系列教程](http://cuiqingcai.com/1052.html)

转载，请表明出处。[总目录Awesome GIS](http://www.jianshu.com/p/3b3efa92dd6d)
