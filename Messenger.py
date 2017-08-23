"""Messenger"""
from __future__ import print_function
import sys
from MessageProcessor import ProcessorClient
sys.path.append("..")
from wxBot.wxbot import WXBot


class Messenger(WXBot):#pylint: disable=too-few-public-methods
    """inherited WXBot"""

    client = ProcessorClient()

    def handle_msg_all(self, msg):
        """override"""
        print(msg)
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            self.send_msg_by_uid(self.client.handlemessage(msg), msg['user']['id'])

def main():
    """entrance"""
    themessenger = Messenger()
    themessenger.debug()
    themessenger.conf['qr'] = 'png'
    themessenger.run()


if __name__ == '__main__':
    main()
