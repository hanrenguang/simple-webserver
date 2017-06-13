#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket, time

root = '.'

def getResponse(contentTp, path):
	Eol = "\r\n"
	spc = " "
	prot = "HTTP/1.1"
	status = "200"
	statusCode = "OK"
	htmlContentType = "text/html; charset=utf-8"
	cssContentType = "text/css"
	jsContentType = "application/javascript"
	contentType = ""
	content = ''

	if contentTp == 'html':
		contentType = htmlContentType
	elif contentTp == 'css':
		contentType = cssContentType
	elif contentTp == 'js':
		contentType = jsContentType

	try:
		f = open(root + path, 'r')
		while True:
			chunk = f.read(1024)
			if not chunk:
				f.close()
				break;
			content += chunk
	except:
		pass

	ret = prot + spc + status + spc + statusCode + Eol + "Content-Length: " + str(len(content)) + Eol + "Content-Type: " + contentType + Eol + Eol + content

	return ret

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
			ret = clientSk.recv(1024).decode().split("\r\n")
			requestSource = ret[0].split(" ")[1]
			contentTp = requestSource.split(".")[1]
			clientSk.sendall(getResponse(contentTp, requestSource).encode(encoding='UTF-8'))
			clientSk.close()
			time.sleep(1)
		except Exception as err:
			print(err)
			clientSk.close()


if __name__ == '__main__':
	serve()