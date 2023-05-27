import argparse
import math
import os
import socket

IP_ADDR = "0.0.0.0"
MSS = 24000  # MSS = Server buffer size (20480) - data header size (4)


def await_ack(packet, addr):
    s.settimeout(1)
    while True:
        try:
            data, addr = s.recvfrom(MSS)
            return (data, addr)
        except KeyboardInterrupt:
            print("Server: Exiting...")
            exit()
        except socket.timeout:
            print("Server: Retransmitting...")
            s.sendto(packet, addr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=str)
    args = parser.parse_args()

    server_port = args.port
    server_port = int(server_port)

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 30000)
        s.bind((IP_ADDR, server_port))
        print(f'Listening on {IP_ADDR}:{server_port}...')

        data, addr = s.recvfrom(MSS)
        columns = data.decode('utf-8', 'replace').split('|')
        print(columns)
        if os.path.isfile(f'./{columns[2]}'):
            print(f'file {columns[2]} exists. Overwriting...')
        f = open(columns[2], 'wb')

        if columns[0] == 's':
            message = f'a|{(int(columns[1])+1)%2}'
            s.sendto(message.encode(), addr)
            data, addr = await_ack(message.encode(), addr)

            bytes_received = 0
            last = b'0'
            while bytes_received < int(columns[3]):
                new_columns = data.split(b'|')
                if new_columns[0] != b'd':
                    data, addr = await_ack(message.encode(), addr)
                    continue
                if new_columns[1] == last:
                    data, addr = await_ack(message.encode(), addr)
                    continue

                last = new_columns[1]

                bindata = new_columns[2]
                for i in new_columns[3:]:
                    bindata = bindata + (b'|') + i
                f.write(bindata)
                bytes_received += len(bindata)
                print(f'Received: {bytes_received}/{columns[3]}')

                message = f'a|{(int(new_columns[1])+1)%2}'
                s.sendto(message.encode(), addr)
                data, addr = await_ack(message.encode(), addr)

            print(f'file {columns[2]} was successfully uploaded. Exiting...')
        else:
            exit(1)
