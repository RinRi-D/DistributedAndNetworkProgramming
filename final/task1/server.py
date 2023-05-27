import socket
import json

IP_ADDR = "0.0.0.0"
PORT = 50000
MSS = 24000  # MSS = Server buffer size (20480) - data header size (4)

class RR:
    type = ''
    key = ''
    value = ''
    
    def __init__(self, type, key, value):
        self.type = type
        self.key = key
        self.value = value

    def json_str(self):
        return json.dumps(self.__dict__)

if __name__ == "__main__":
    server_port = PORT

    records = (RR('A', 'example.com', '1.2.3.4'), RR('PTR', '1.2.3.4', 'example.com'))

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
        s.bind((IP_ADDR, server_port))
        print(f'Listening on {IP_ADDR}:{server_port}...')
        
        try:
            while True:
                data, addr = s.recvfrom(MSS)
                query = json.loads(data)
                print(f'Client {query}')
                ok = False

                for record in records:
                    if record.type == query['type'] and record.key == query['key']:
                        print('Server: Record found. Sending answer.')
                        s.sendto(record.json_str().encode(), addr)
                        ok = True
                        break
                
                if ok == False:
                    print('Server: Record not found. Sending error.')
                    record = RR(query['type'], query['key'], 'NXDOMAIN')
                    s.sendto(record.json_str().encode(), addr)

        except KeyboardInterrupt:
            print('Server: Interrupted by user. Exiting')
            exit(0)
