import sys
import threading
import time
from rpyc.utils.server import ThreadedServer
from rpyc.core.service import ClassicService

def run_server():
    print("Starting RPyC Classic Server on Port 18812...")
    config = {'allow_all_attrs': True, 'allow_public_attrs': True, 'sync_request_timeout': 60}
    server = ThreadedServer(ClassicService, port=18812, protocol_config=config)
    server.start()

# Loop the thread for MT5 injection so the graphical terminal doesn't close
run_server()
