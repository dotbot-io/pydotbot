from json import dumps
from ws4py.client.threadedclient import WebSocketClient
import time

class DotBot(WebSocketClient):
    def __init__(self, address):
        WebSocketClient.__init__(self, address)
        self.connect()
        self._start_speed()
        self._start_leds()

    def _start_speed(self):
        msg = {'op': 'advertise', 'topic': '/robotoma/speed', 'type': 'robotoma_msgs/Speed'}
        self.send(dumps(msg))

    def _start_leds(self):
        msg = {'op': 'advertise', 'topic': '/robotoma/led', 'type': 'robotoma_msgs/Led'}
        self.send(dumps(msg))

    def set_speed(self, sx, dx):
        msg = {'op': 'publish', 'topic': '/robotoma/speed', 'msg': {'sx': sx, 'dx': dx}}
        self.send(dumps(msg))

    def set_leds(self, led1, led2, led3):
        msg = {'op': 'publish', 'topic': '/robotoma/led', 'msg': {'led1': led1, 'led2': led2, 'led3': led3}}
        self.send(dumps(msg))

    def closed(self, code, reason=None):
        print code, reason

    def opened(self):
        print "Connection opened..."

if __name__=="__main__":
     try:
         ws = DotBot('ws://127.0.0.1:9090/')
         sx = 0
         while(True):
             ws.set_speed(sx, 10)
             sx = sx + 1
             ws.set_leds(True, False, sx%2 is 0)
             time.sleep(0.1)
     except KeyboardInterrupt:
         ws.close()
