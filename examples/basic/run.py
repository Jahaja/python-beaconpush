import datetime
import time
import random
import logging

from beaconpush import BeaconPush, logger

logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

def main():
    # Set up the beacon service
    bp = BeaconPush('your_api_key_here', 'your_api_secret_here')

    # Send some channel messages randomly every 0-10 seconds forever 
    while True:
        print "Sending message..."
        bp.channel_send_message("frontpage", {"time": str(datetime.datetime.now()), "msg": "This is a message pushed from the server"})
        time.sleep(random.randint(0, 10))

if __name__ == '__main__':
    main()