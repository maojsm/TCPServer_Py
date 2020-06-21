import socket
import time

HOST = ''              # Endereco IP do Servidor
PORT = 12000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

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
        print('\n-------------------\n')
        time.sleep(2)
    print('Finalizando conexao do cliente', cliente)
    con.close()