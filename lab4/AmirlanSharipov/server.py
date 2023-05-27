import sqlite3
from concurrent.futures import ThreadPoolExecutor

import grpc
import schema_pb2 as stub
import schema_pb2_grpc as service

SERVER_ADDR = '0.0.0.0:1234'


class Database(service.DatabaseServicer):
    def PutUser(self, request, context):
        try:
            con = sqlite3.connect('db.sqlite')
            cur = con.cursor()
            print(request.user_id, request.user_name)
            cur.execute("INSERT OR REPLACE INTO User (id, name) VALUES (?, ?)",
                        (request.user_id, request.user_name))
            con.commit()
            con.close()
            return stub.Response(status=1)
        except Exception as inst:
            con.close()
            return stub.Response(status=0)

    def GetUsers(self, request, context):
        try:
            con = sqlite3.connect('db.sqlite')
            cur = con.cursor()
            res = cur.execute('SELECT id, name FROM User')
            users = []

            for user in res.fetchall():
                users.append({'user_id': user[0], 'user_name': user[1]})

            con.commit()
            con.close()
            return stub.UsersResponse(users=users)
        except Exception:
            con.close()
            return stub.UsersResponse(users=[])

    def DeleteUser(self, request, context):
        try:
            con = sqlite3.connect('db.sqlite')
            cur = con.cursor()
            cur.execute('DELETE FROM User WHERE id=?', (request.user_id, ))
            con.commit()
            con.close()
            return stub.Response(status=1)
        except Exception:
            con.close()
            return stub.Response(status=0)


def create_table():
    try:
        con = sqlite3.connect('db.sqlite')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS User(id INTEGER PRIMARY KEY, name TEXT)')
        con.commit()
        con.close()
        print('Created a table')
    except Exception:
        print('DOESNT WORK')


if __name__ == '__main__':
    create_table()
    try:
        server = grpc.server(ThreadPoolExecutor(max_workers=30))
        service.add_DatabaseServicer_to_server(Database(), server)
        server.add_insecure_port(SERVER_ADDR)
        server.start()
        print(f'listening on {SERVER_ADDR}')
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('Interrupted by user. Shutting down...')
