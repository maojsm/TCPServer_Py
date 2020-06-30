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



def calcChecksum(msgFull):
    # variavel de rrtorno
    res = 0
    # Testando se a mensagem recebida contem os limitadores de inicio e fim
    if '$' in msgFull and '*' in msgFull:
        # Pega os indices de inicio de fim da mensagem
        startId = msgFull.find('$')
        endId   = msgFull.find('*')

        # Calcula checksum
        for x in msgFull[startId:endId]:
            # print(x)
            res = res ^ ord(x)
    # retorna valor do checksum
    return res


while True:
    con, cliente = tcp.accept()
    print('Concetado por', cliente)
    while True:
        con.sendto(cmd.encode(), cliente)
        cnt_msg = cnt_msg + 1
        print(cnt_msg, ' - Mensagem Enviada: ', cmd)
        msg = con.recv(1024)
        if not msg: break

        msg_dec = msg.decode()

        print('\n', cliente, ' Recebido do Controlador: ', msg_dec)
        # Testando se a mensagem recebida contem os limitadores de inicio e fim
        if '$JSM,' in msg_dec and ';' in msg_dec and '*' in msg_dec:

            # Pega os indices de inicio de fim da mensagem
            iniId = msg_dec.find('$JSM,')
            endId = msg_dec.find(';')
            chkId = msg_dec.find('*')

            # Cria string com a mensagem completa, limpa e testada
            msgFull = msg_dec[iniId:endId]

            # separa o Checksum da mensagem
            chk = msg_dec[chkId+1:endId]

            # debug do Checksum
            print('Checksum: ', chk)
            print('Checksum calculado: ', calcChecksum(msgFull))

            # Testa se Checksum está correto
            if chk == calcChecksum(msgFull):
                # Cria uma nova string apenas com a mensagem entre os delimitadores
                msgParts = msg_dec[iniId:endId].split(',')

                print(msgParts)

        print('\n-------------------\n')
        time.sleep(2)

    print('Finalizando conexao do cliente', cliente)

    con.close()