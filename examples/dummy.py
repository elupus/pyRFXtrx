import socket
import RFXtrx as rfxtrx

def recv_packet(s: socket.socket):
    l = s.recv(1, socket.MSG_WAITALL)
    if l is None:
        return None
    d = s.recv(l[0], socket.MSG_WAITALL)
    return [*l *d]

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 12345))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = recv_packet(conn)
                if not data:
                    break
                packet = rfxtrx.lowlevel.parse(data)
                print(packet)

                conn.sendall(b'\x0D\x01\x00\x01\x02\x53\x45\x00\x0C\x2F\x01\x01\x00\x00')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass