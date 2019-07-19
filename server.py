import struct
import socket
import select

server_address = ('localhost', 10000)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(server_address)

server.listen(1)

inputs = [server]

def diffManchesster(signal):
    inputs = map(int, signal)
    result = []
    prev = 0
    for i in range(len(inputs)):
        if inputs[i] == 1 and prev == 1:
            result.append((1,0))
            prev = 0
        elif inputs[i] == 1 and prev == 0:
            result.append((0,1))
            prev = 1
        elif inputs[i] == 0 and prev == 0:
            result.append((1,0))
            prev = 0
        elif inputs[i] == 0 and prev == 1:
            result.append((0,1))
            prev = 1
    
    return result


def manchester(signal):
    clock = ''.join(('01') * len(signal))

    cnt = 0
    tmp = []
    result = []
    for i in range(len(signal)):
        for j in range(len(clock)):
            xor = int(signal[i]) ^ int(clock[j])
            tmp.append(xor)
            cnt += 1
            if(cnt == 2):
                result.append((tmp[0], tmp[1]))
                tmp = []
                cnt = 0
                break

    return result


def rz(signal):
    inputs = map(int, signal)
    inputs = [0 if i == 0 else 1 for i in inputs]
    result = []

    for i in range(len(inputs)):
        result.append((inputs[i], 0))
    return result


def nrzl(signal):
    inputs = map(int, signal)
    result = []
    for i in range(len(inputs)):
        if inputs[i] == 1:
            result.append((inputs[i], 1))
        else:
            result.append((inputs[i], 0))
    
    return result


def handleType(s, c_type, signal):
    result = []
    if c_type == 'NZR-L':
        result = nrzl(signal)
    elif c_type == 'RZ':
        result = rz(signal)
    elif c_type == 'Manchester':
        result = manchester(signal)
    else:
        result = diffManchesster(signal)
    
    s.sendall(str(result))

while inputs:
    timeout = 1
    read, write, excpt = select.select(inputs, inputs, inputs, timeout)
    unpacker = struct.Struct('16s 14s')

    for s in read:
        if s is server:
            connection, client_address = s.accept()
            inputs.append(connection)
            print "New Client: ", ":".join(str(el) for el in client_address)
        else:
            try:
                data = s.recv(4096)

                if data:
                    unpacked = unpacker.unpack(data)
                    signal = unpacked[0].rstrip('\x00')
                    c_type = unpacked[1].rstrip('\x00')

                    handleType(s, c_type, signal)
                    #print signal , c_type
                else:
                    s.close()
                    inputs.remove(s)
                    print "Kliens kilepett"
            except socket.error, m:
                print m
                s.close()
                inputs.remove(s)
                print "Kliens hibaval lepett ki"


server.close()



