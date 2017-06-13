#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket

# 资源根目录
root = '.'

# def getResponse(contentTp, path):
#   Eol = "\r\n"
#   spc = " "
#   prot = "HTTP/1.1"
#   status = "200"
#   statusCode = "OK"
#   htmlContentType = "text/html; charset=utf-8"
#   cssContentType = "text/css"
#   jsContentType = "application/javascript"
#   contentType = ""
#   content = ''

#   if contentTp == 'html':
#       contentType = htmlContentType
#   elif contentTp == 'css':
#       contentType = cssContentType
#   elif contentTp == 'js':
#       contentType = jsContentType

#   try:
#       f = open(root + path, 'r')
#       while True:
#           chunk = f.read(1024)
#           if not chunk:
#               f.close()
#               break;
#           content += chunk
#   except:
#       pass

#   ret = prot + spc + status + spc + statusCode + Eol + "Content-Length: " + str(len(content)) + Eol + "Content-Type: " + contentType + Eol + Eol + content

#   return ret

# 解析请求报文
def parseReq(reqList):
    # 保存解析结果
    parseRet = {}

    method = reqList[0].split(' ')[0]
    sourcePath = reqList[0].split(' ')[1]

    parseRet['method'] = method
    parseRet['sourcePath'] = sourcePath

    i = len(reqList) - 1

    while i:
        if len(reqList[i].split(':')) == 1:
            i = i - 1
            continue

        idx = reqList[i].find(':')
        key, value = reqList[i][0:idx], reqList[i][idx+1:]
        parseRet['{0}'.format(key)] = value.strip()
        i = i - 1

    return parseRet


# 开启服务器
def serve():
    sk = socket.socket(
        socket.AF_INET, 
        socket.SOCK_STREAM
    )

    host = '127.0.0.1'
    port = 8888

    sk.bind((host, port))
    sk.listen(5)

    while True:
        try:
            clientSk, addr = sk.accept()
            print("address is: %s" % str(addr))

            requestList = clientSk.recv(1024).decode().split("\r\n")
            # 解析HTTP请求报文
            ret = parseReq(requestList)

            # 返回HTTP响应报文
            # clientSk.sendall(response.encode(encoding='UTF-8'))
            clientSk.close()

        except Exception as err:
            print(err)
            clientSk.close()


if __name__ == '__main__':
    serve()