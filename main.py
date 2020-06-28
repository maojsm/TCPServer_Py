import socket
import time
import re

HOST = ''               # Endereco IP do Servidor
PORT = 12000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(5)

cmd = '$JSM,1,P,F6,1,1*69;'
cnt_msg = 0

while True:
    con, cliente = tcp.accept()
    print('Concetado por', cliente)
    while True:
        con.sendto(cmd.encode(), cliente)
        cnt_msg = cnt_msg + 1
        print(cnt_msg, ' - Mensagem Enviada: ', cmd)
        msg = con.recv(1024)
        if not msg: break
        print('\n', cliente, ' Recebido do Controlador: ', msg)

        # if re.search("$", msg.decode(), re.IGNORECASE):
          #  msg_split1 = msg.decode().split("$")
          #  if re.search(";", msg_split1[1], re.IGNORECASE):
          #      msg_split2 = msg_split1.split(";")
          #      print(msg_split2)

        print('\n-------------------\n')
        time.sleep(2)
    print('Finalizando conexao do cliente', cliente)
    con.close()