from socket import *
import logging
from blockchain.common.config import config
from blockchain.common.services.status_listener import StatusListener

BROADCAST_ADDRESS = '255.255.255.255'
BUFFER_SIZE = 1024 * 1024

class Network:
    def __init__(self):
        pass

    def send_transaction(self, bytes):
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        s.sendto(bytes, (BROADCAST_ADDRESS, config.get('transaction_port')))

    def send_block_request_and_wait(self, bytes, host, port):
        logging.info('requesting new blocks from {}'.format(host))

        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        s.send(bytes)
        block_data = s.recv(BUFFER_SIZE)
        s.close()

        logging.debug('received new block data from {}:{} {}'.format(host, port, block_data))

        return block_data

    def find_host_to_sync(self, on_host_found, shutdown_event):
        status_listener_port = config.get('status_broadcast_port')
        listener = StatusListener(status_listener_port, shutdown_event, on_host_found)
        listener.start()
        return listener

