#!/usr/bin/env python
#
# Copyright 2010 Joakim Hamrén
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import datetime
import time
import random
import logging

from beaconpush import BeaconPush, logger

logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

def main():
    # Set up the beacon service
    bp = BeaconPush('api_key_here', 'api_secret_key_here')

    # Send some channel messages randomly every 0-10 seconds forever 
    while True:
        print "Sending message..."
        bp.channel_send_message("frontpage", {"time": str(datetime.datetime.now()), "msg": "This is a message pushed from the server"})
        time.sleep(random.randint(0, 10))

if __name__ == '__main__':
    main()