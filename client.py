import socket
import struct

server_addr = ('localhost', 10000)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(server_addr)

types = {'NZR-L', 'RZ', 'Manchester', 'DiffManchester'}

while True:
    signal = raw_input("signal >> ")
    code_type = raw_input("code type >> ")

    if signal != '' and code_type != '':
        if len(signal) <= 16 and code_type in types:
          packer = struct.Struct('16s 14s')
          packed_data = packer.pack(signal, code_type)
          client.sendall(packed_data)

        else:
            print 'Bad input'
            client.close()
            break

    data = client.recv(4096)
    print data

client.close()
