# simple-webserver

> 基于 `Python3` 写的极简版 `webserver`。用于学习 `HTTP协议`，及 `WEB服务器` 工作原理。笔者对 `WEB服务器` 的工作原理理解的比较粗浅，仅是基于个人的理解来写的，存在很多不足和漏洞，目的在于给大家提供一个写 `webserver` 的思路。

## WEB服务器原理

学过计网的同学应该都知道 `HTTP协议` 是在 `TCP协议` 之上实现的。浏览器与服务器之间的通信首先是建立 `TCP` 连接，再进行请求和响应报文的传输。服务器是属于被动的一方，当浏览器发起请求的时候，服务器才能和浏览器通信，在此之前，服务器都处于一个等待监听的状态。

### socket连接

实现服务器的第一步是建立一个 `socket` 连接，`socket` 套接字是对 `TCP/UDP协议` 的一个封装，`Python` 就自带有 `socket` 模块，所以使用起来很方便。

```Python
import socket

sk = socket.socket(
    socket.AF_INET, 
    socket.SOCK_STREAM
)

# 监听本地 8888 端口
host = '127.0.0.1'
port = 8888

sk.bind((host, port))
sk.listen(5)

while True:
    try:
        clientSk, addr = sk.accept()
        print("address is: %s" % str(addr))

        req = clientSk.recv(1024)

        clientSk.sendall('...')
        clientSk.close()

    except Exception as err:
        print(err)
        clientSk.close()
```

这是一个极简的 `socket-server`，需要注意的是，我们仅实现了 `TCP协议` 的部分。

### 解析HTTP请求

拿到浏览器的请求很简单，`clientSk.recv()` 即可获取请求报文，而些数据我们无法直接拿来用，因为它是基于 `HTTP协议` 封装的数据，在我们进行下一步操作前，需要对请求报文“解封”。而在此之前，我们需要了解请求报文的格式。最快捷的方式呢，是打开浏览器（以 `chrome` 为例），随便打开百度啥的，`F12` 打开开发者工具，在 `Network` 一栏就可以观察到。大概长下面这样：

```bash
GET / HTTP/1.1
Host: xxx
Connection: xxx
Cache-Control: xxx
Upgrade-Insecure-Requests: xxx
User-Agent: xxx
Accept: xxx
Accept-Encoding: xxx
Accept-Language: xxx
Cookie: xxx
```

我们把关注点放在第一行，`GET` 方法，请求的资源路径为 `/`，使用的协议是 `HTTP1.1`，之后就是一回车换行符 `\r\n`。所以我们对报文的解析如下（存在许多不足之处）：

```Python
# 第一步先对数据进行解码 decode()，
# 再以行为单位进行分割
requestList = clientSk.recv(1024).decode().split("\r\n")

# 调用写好的函数对其进行解析
parseReq(requestList)

# 解析请求报文
def parseReq(reqList):
    # 保存解析结果
    parseRet = {}

    # 请求的方法，如 GET
    method = reqList[0].split(' ')[0]
    # 请求的资源路径，如 '/'
    sourcePath = reqList[0].split(' ')[1]

    parseRet['method'] = method
    parseRet['sourcePath'] = sourcePath

    i = len(reqList) - 1

    # 以 key: value 的形式保存解析结果
    while i:
        if len(reqList[i].split(':')) == 1:
            i = i - 1
            continue

        idx = reqList[i].find(':')
        key, value = reqList[i][0:idx], reqList[i][idx+1:]
        parseRet[key] = value.strip()
        i = i - 1
    
    return parseRet
```

### 构造响应报文

拿到了请求报文并将其解析后，我们可以开始构造响应报文的内容了，以请求静态资源为例，假设请求报文第一行为 `GET /index.html HTTP/1.1`。那么我首先要做的就是先获取路径为 `/index.html` 的文件内容：

```Python
# 获取资源内容
try:
    f = open(path, 'r')
    while True:
        chunk = f.read(1024)
        if not chunk:
            f.close()
            break;
        content += chunk
except:
    pass
```

那接下来就是构造响应报文了，同理可以观察 `HTTP` 响应报文的格式，在此就不举例了，直接上代码：

```Python
try:
    f = open(path, 'r')
    while True:
        chunk = f.read(1024)
        if not chunk:
            f.close()
            break;
        content += chunk
except:
    pass

# 省略了大部分头部信息
headers = 'HTTP/1.1 200 OK\r\n'
contentType = 'Content-Type: text/html; charset=utf-8\r\n'
contentLen = 'Content-Length: ' + str(len(content)) + '\r\n'

# 组合成响应报文 res
res = headers + contentType + contentLen + '\r\n' + content

# 编码后发送给浏览器，
# 至此，本次通信结束
clientSk.sendall(res.encode(encoding='UTF-8'))
clientSk.close()
```

## 示例

下载本项目到本地，双击 `server.py`，并访问 [http://localhost:8888/index.html](http://localhost:8888/index.html)，你应该会看到十分亲切的 `Hello world!`。