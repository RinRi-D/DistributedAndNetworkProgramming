import random
import sched
import socket
import time
from threading import Thread
from argparse import ArgumentParser
from enum import Enum
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

PORT = 1234
CLUSTER = [1, 2, 3]
ELECTION_TIMEOUT = (6, 8)
HEARTBEAT_INTERVAL = 5


class NodeState(Enum):
    """Enumerates the three possible node states (follower, candidate, or leader)"""
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3


class Node:
    def __init__(self, node_id):
        """Non-blocking procedure to initialize all node parameters and start the first election timer"""
        self.node_id = node_id
        self.state = NodeState.FOLLOWER
        self.term = 0
        self.votes = {}
        self.log = []
        self.pending_entry = ''
        self.sched = sched.scheduler()
        self.event = ''
        # TODO: start election timer for this node
        self.reset_election_timer()
        print(f"Node started! State: {self.state}. Term: {self.term}")

    def is_leader(self):
        """Returns True if this node is the elected cluster leader and False otherwise"""
        if self.state == NodeState.LEADER:
            return True
        return False

    def reset_election_timer(self):
        """Resets election timer for this (follower or candidate) node and returns it to the follower state"""
        self.state = NodeState.FOLLOWER

        q = self.sched.queue
        for event in q:
            self.sched.cancel(event)

        #if (self.node_id == 1 or self.node_id == 3):
        #    self.sched.enter(0, 1, self.hold_election, ())
        #    return
        self.sched.enter(random.uniform(ELECTION_TIMEOUT[0], ELECTION_TIMEOUT[1]), 1, self.hold_election, ())

    def reset_heartbeat_timer(self):
        q = self.sched.queue
        for event in q:
            self.sched.cancel(event)

        self.sched.enter(HEARTBEAT_INTERVAL, 1, self.append_entries, ())

    def hold_election(self):
        """Called when this follower node is done waiting for a message from a leader (election timeout)
            The node increments term number, becomes a candidate and votes for itself.
            Then call request_vote over RPC for all other online nodes and collects their votes.
            If the node gets the majority of votes, it becomes a leader and starts the hearbeat timer
            If the node loses the election, it returns to the follower state and resets election timer.
        """
        self.term = self.term + 1
        self.state = NodeState.CANDIDATE
        self.votes = {}
        self.votes[self.node_id] = True
        print(f'New election term {self.term}. State: {self.state}')

        for n0 in CLUSTER:
            if node == self.node_id:
                continue

            try:
                print(f'Requesting vote from node {n0}')
                with ServerProxy(f'http://node_{n0}:{PORT}') as proxy:
                    if proxy.request_vote(self.term, self.node_id):
                        self.votes[n0] = True
                    else:
                        self.votes[n0] = False
            except Exception as e:
                print(f"couldn't request_vote from {n0}")
                print(traceback.format_exc())
                print(e)

        if sum(self.votes.values()) > len(CLUSTER) / 2:
            self.state = NodeState.LEADER
            self.reset_heartbeat_timer()

        print(f"New election term {self.term}. State: {self.state}")

    def request_vote(self, term, candidate_id):
        """Called remotely when a node requests voting from other nodes.
            Updates the term number if the received one is greater than `self.term`
            A node rejects the vote request if it's a leader or it already voted in this term.
            Returns True and update `self.votes` if the vote is granted to the requester candidate and False otherwise.
        """

        print(f"Got a vote request from {candidate_id} (term={term})")
        self.reset_election_timer()

        if term > self.term:
            self.term = term
            self.votes = {}

        if self.is_leader() or len(self.votes) > 0:
            return False

        self.votes[candidate_id] = True
        return True

    def append_entries(self):
        """Called by leader every HEARTBEAT_INTERVAL, sends a heartbeat message over RPC to all online followers.
            Accumulates ACKs from followers for a pending log entry (if any)
            If the majority of followers ACKed the entry, the entry is committed to the log and is no longer pending
        """
        print("Sending a heartbeat to followers")

        acks = 0
        for n0 in CLUSTER:
            if n0 == self.node_id:
                continue

            try:
                with ServerProxy(f'http://node_{n0}:{PORT}') as proxy:
                    if proxy.heartbeat(self.pending_entry):
                        acks = acks + 1
            except Exception as e:
                print(f"couldn't heartbeat {n0}")
                print(traceback.format_exc())
                print(e)

        if self.pending_entry != '' and acks > len(CLUSTER) / 2:
            self.log.append(self.pending_entry)
            print(f'Leader commited \'{self.pending_entry}\'')
            self.pending_entry = ''

        self.reset_heartbeat_timer()

    def heartbeat(self, leader_entry):
        """Called remotely from the leader to inform followers that it's alive and supply any pending log entry
            Followers would commit an entry if it was pending before, but is no longer now.
            Returns True to ACK the heartbeat and False on any problems.
        """
        print(f"Heartbeat received from leader (entry='{leader_entry}')")
        try:
            self.reset_election_timer()
            if self.pending_entry != '' and leader_entry != self.pending_entry:
                self.log.append(self.pending_entry)
                print(f'Follower commited \'{self.pending_entry}\'')

            self.pending_entry = leader_entry

            return True
        except Exception as e:
            return False

    def leader_receive_log(self, log):
        """Called remotely from the client. Executed only by the leader upon receiving a new log entry
            Returns True after the entry is committed to the leader log and False on any problems
        """
        print(f"Leader received log \'{log}\' from client")
        while self.pending_entry != '':
            time.sleep(1)

        self.pending_entry = log
        time.sleep(7)
        if self.pending_entry == '' and self.log[-1] == log:
            return True
        return False


if __name__ == '__main__':
    # TODO: Parse one integer argument (node_id), then create the node with that ID.
    # TODO: Start RPC server on 0.0.0.0:PORT and expose the node instance
    # TODO: Run the node scheduler in an isolated thread.
    # TODO: Handle KeyboardInterrupt and terminate gracefully.
    try:
        parser = ArgumentParser()
        parser.add_argument('node_id')
        args = parser.parse_args()
        node = Node(int(args.node_id))

        t = Thread(target=node.sched.run)
        t.start()

        server = SimpleXMLRPCServer(('0.0.0.0', PORT), logRequests=False)
        print(f"Listening on port {PORT}...")
        server.register_function(node.leader_receive_log, "leader_receive_log")
        server.register_function(node.heartbeat, "heartbeat")
        server.register_function(node.request_vote, "request_vote")
        server.register_function(node.is_leader, "is_leader")
        server.serve_forever()
    except KeyboardInterrupt:
        print("node killed...")
        exit()

