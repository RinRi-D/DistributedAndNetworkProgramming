from argparse import ArgumentParser
from bisect import bisect_left, bisect_right
from threading import Thread
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

import traceback

M = 5
PORT = 1234
RING = [2, 7, 11, 17, 22, 27]


class Node:
    def __init__(self, node_id):
        """Initializes the node properties and constructs the finger table according to the Chord formula"""
        # Assuming that the program knows all the nodes and stores them in a sorted array RING
        self.node_id = node_id
        self.finger_table = []
        self.successor_id = RING[(RING.index(node_id) + 1) % len(RING)]
        self.predecessor_id = RING[RING.index(node_id) - 1]
        self.table = {}
        
        for i in range(M):
            self.finger_table.append(RING[bisect_left(RING, ((node_id + (2 ** i)) % (2 ** M))) % len(RING)])

        print(f"Node created! Finger table = {self.finger_table}, [pred, succ] = [{self.predecessor_id}, {self.successor_id}]")

    def closest_preceding_node(self, id):
        """Returns node_id of the closest preceeding node (from n.finger_table) for a given id"""
        for i in reversed(self.finger_table):
            if i == RING[-1]:
                idx = bisect_left([RING[0], RING[-1]], id)
                if idx == 0 or idx == 2:
                    return i
            elif self.node_id > i:
                idx = bisect_left([i, self.node_id], id)
                if idx == 1:
                    return i
            else:
                if i > self.node_id and i < id:
                    return i
        return self.finger_table[-1]

    def find_successor(self, id):
        """Recursive function returning the identifier of the node responsible for a given id"""

        if id == self.node_id:
            return id

        # Note the half-open interval and that L <= R does not necessarily hold
        if self.successor_id < self.node_id:
            idx = bisect_left([self.successor_id, self.node_id], id)
            if idx == 0 or idx == 2:
                return self.successor_id
        elif id in range(self.node_id, self.successor_id + 1):
            return self.successor_id

        # Forward the query to the closest preceding node in the finger table for n
        n0 = self.closest_preceding_node(id)
        print(f'Forwarding request to node {n0}')
        with ServerProxy(f'http://node_{n0}:{PORT}') as proxy:
            return proxy.find_successor(id)

    def put(self, key, value):
        """Stores the given key-value pair in the node responsible for it"""
        try:
            print(f"put({key}, {value})")

            if self.node_id < self.predecessor_id:
                idx = bisect_left([self.node_id, self.predecessor_id], key)
                if idx == 0 or idx == 2:
                    return self.store_item(key, value)
            elif key in range(self.predecessor_id, self.node_id + 1):
                return self.store_item(key, value)
                
            n0 = self.find_successor(key)
            if self.node_id == n0:
                return self.store_item(key, value)
            
            with ServerProxy(f'http://node_{n0}:{PORT}') as proxy:
                return proxy.store_item(key, value)
        except Exception as e:
            print(f"couldn't put({key}, {value})")
            print(traceback.format_exc())
            print(e)
            return False

    def get(self, key):
        """Gets the value for a given key from the node responsible for it"""
        try:
            print(f"get({key})")
            if self.node_id < self.predecessor_id:
                idx = bisect_left([self.node_id, self.predecessor_id], key)
                if idx == 0 or idx == 2:
                    return self.retrieve_item(key)
            elif key in range(self.predecessor_id, self.node_id + 1):
                return self.retrieve_item(key)
                
            n0 = self.find_successor(key)
            if self.node_id == n0:
                return self.retrieve_item(key)
            
            with ServerProxy(f'http://node_{n0}:{PORT}') as proxy:
                return proxy.retrieve_item(key)
        except Exception as e:
            print(f"couldn't get({key})")
            print(traceback.format_exc())
            print(e)
            return -1

    def store_item(self, key, value):
        """Stores a key-value pair into the data store of this node"""
        self.table[key] = value
        return True

    def retrieve_item(self, key):
        """Retrieves a value for a given key from the data store of this node"""
        if key in self.table:
            return self.table[key]
        return -1


if __name__ == '__main__':
    try:
        parser = ArgumentParser()
        parser.add_argument('node_id')
        args = parser.parse_args()
        node = Node(int(args.node_id))

        server = SimpleXMLRPCServer(('0.0.0.0', PORT))
        print("Listening on port 1234...")
        server.register_function(node.get, "get")
        server.register_function(node.put, "put")
        server.register_function(node.retrieve_item, "retrieve_item")
        server.register_function(node.store_item, "store_item")
        server.register_function(node.find_successor, "find_successor")
        server.serve_forever()
    except KeyboardInterrupt:
        print("node killed...")
        exit()

