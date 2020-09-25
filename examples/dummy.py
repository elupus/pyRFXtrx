import socket
import RFXtrx as rfxtrx

def recv_packet(s: socket.socket):
    l = s.recv(1, socket.MSG_WAITALL)
    if not l:
        return None
    d = s.recv(l[0], socket.MSG_WAITALL)
    if not d:
        return None
    res = bytearray()
    res.extend(l)
    res.extend(d)
    return res

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 12345))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = recv_packet(conn)
                    if not data:
                        break
                    packet = rfxtrx.lowlevel.parse(data)
                    print(packet)
                    if type(packet) == rfxtrx.lowlevel.InterfaceControl:
                        conn.sendall(b'\x0D\x01\x00\x01\x02\x53\x45\x00\x0C\x2F\x01\x01\x00\x00')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass