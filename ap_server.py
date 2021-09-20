import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),1024))
s.listen(5)
while True:
    clt,adr = s.accept()
    msg = clt.recv(20)
    msg = msg.decode('utf-8')
    if msg == '3':
        break
    print(msg)
