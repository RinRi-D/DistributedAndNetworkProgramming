import socket
import json

MSS = 20476  # MSS = Server buffer size (20480) - data header size (4)

class Query:
    type = ''
    key = ''

    def __init__(self, type, key):
        self.type = type
        self.key = key

    def json_str(self):
        return json.dumps(self.__dict__)

def await_response(s):
    data, addr = s.recvfrom(MSS)
    print(f'Server: {json.loads(data)}')

if __name__ == "__main__":
    server_ip, server_port = ('127.0.0.1', 50000)

    queries = (Query('A', 'example.com'),
               Query('PTR', '1.2.3.4'),
               Query('CNAME', 'moodle.com'))

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
        for query in queries:
            print(f'Performing query {query.json_str()}:')
            s.sendto(query.json_str().encode(), (server_ip, server_port))

            await_response(s)
        
