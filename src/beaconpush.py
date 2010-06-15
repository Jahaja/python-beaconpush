# coding=UTF-8
import httplib
import urllib
import logging

try:
    import simplejson as json
except ImportError:
    import json

class BeaconPushException(Exception):
    pass

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logger = logging.getLogger("BeaconPush")
logger.setLevel(logging.DEBUG)
logger.addHandler(NullHandler())
#logger.addHandler(logging.StreamHandler())

class BeaconPush(object):
    api_host = "beaconpush.com"
    api_version = "1.0.0"
    api_url = "/api/%(version)s/%(api_key)s/%(command)s"

    def __init__(self, api_key, secret_key, host=None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.host = self.api_host if not host else host

    def _get_url(self, command, *args):
        url = self.api_url % {"version": self.api_version, "api_key": self.api_key,
                              "command": command}
        if args:
            url += "/" + "/".join((str(x) for x in args))
        return url

    def _dump_data(self, data):
        if isinstance(data, (str, int, float)):
            data = [data]

        return json.dumps(data)

    def _request(self, method, url, data=None):
        try:
            connection = httplib.HTTPConnection(self.host)

            if data:
                data = self._dump_data(data)

            headers = {'X-Beacon-Secret-Key': self.secret_key}
            logger.debug("requesting rest-api url: %s" % url)
            logger.debug("data: %s" % data)
            connection.request(method, url, body=data, headers=headers)
            resp = connection.getresponse()

            # read and load response data
            if resp.status == httplib.OK:
                data = resp.read()
                if data:
                    data = json.loads(data, 'utf-8')
            else:
                data = None

            return (resp.status, data)
        except httplib.HTTPException, e:
            logger.error("HTTP Error: an exception occured while trying to request a beaconpush url")
            logger.exception(e)
            raise BeaconPushException()

    def get_number_of_users(self):
        """
        Get number of users
        """
        status, data = self._request("GET", self._get_url('users'))
        if status == httplib.OK:
            return data.get('online')
        else:
            logging.warning("didn't get 200 OK, returning -1.")
            return -1


    def get_users_in_channel(self, channel):
        """
        Get users in channel
        """
        status, data = self._request("GET", self._get_url('channels', channel))
        if status == httplib.OK:
            return data.get('users')
        else:
            logging.warning("get_users_in_channel, didn't get 200 OK (got %s), returning empty dict." % str(status))
            return []

    def channel_send_message(self, channel, message):
        """
        Send a message to given channel
        """
        status, data = self._request("POST", self._get_url('channels', channel), message)
        if status == httplib.OK:
            return data.get('messages_sent')
        else:
            logging.warning("didn't get 200 OK from channel %s, returning 0." % channel)
            return 0

    def user_send_message(self, user, message):
        """
        Send a message to given user
        """
        status, data = self._request("POST", self._get_url('users', user), message)
        if status == httplib.OK:
            return data.get('messages_sent')
        else:
            logging.warning("didn't get 200 OK from channel %s, returning 0." % channel)
            return 0

    def user_is_online(self, user):
        """
        Check if given user is online
        Returns boolean.
        """
        status, data = self._request("GET", self._get_url('users', user))
        if status == httplib.OK:
            return True
        else:
            return False

    def user_force_logout(self, user):
        """
        Force logout given user
        """
        status, = self._request("DELETE", self._get_url('users', user))
        if status == httplib.NO_CONTENT:
            return True
        else:
            return False


def test():
    beacon_push = BeaconPush('your_api_key_here', 'your_api_secrey_key_here')
    print "get users in channel response:", beacon_push.get_users_in_channel('mychannel')
    print "send channel message response:", beacon_push.channel_send_message('mychannel', 'Proper call, eh!')
    print "send user message response:", beacon_push.user_send_message('myuser', 'Proper call, eh!')
    print "get num of users response:", beacon_push.get_number_of_users()
    print "myuser is online response:", beacon_push.user_is_online('myuser')
    print "force logout myuser response:", beacon_push.user_is_online('myuser')

if __name__ == '__main__':
    test()