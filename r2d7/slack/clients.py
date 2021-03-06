"""
Stolen from https://github.com/BeepBoopHQ/starter-python-bot/

MIT Licensed
"""
import logging
import re
import time

from slacker import Slacker
from slackclient import SlackClient

logger = logging.getLogger(__name__)


class SlackClients(object):
    def __init__(self, token):
        self.token = token

        # Slacker is a Slack Web API Client
        self.web = Slacker(token)

        # SlackClient is a Slack Websocket RTM API Client
        self.rtm = SlackClient(token)

    def bot_user_id(self):
        return self.rtm.server.login_data['self']['id']

    def is_a_bot(self, user):
        is_bot = user in ( 'USLACKBOT', self.rtm.server.login_data['self']['id'])

        if is_bot:
            logger.debug('We don\'t serve their kind here!')
        return is_bot

    def is_bot_mention(self, message):
        bot_user_name = self.rtm.server.login_data['self']['id']
        return re.search("@{}".format(bot_user_name), message)

    def send_user_typing_pause(self, channel_id, sleep_time=3.0):
        user_typing_json = {"type": "typing", "channel": channel_id}
        self.rtm.server.send_to_websocket(user_typing_json)
        time.sleep(sleep_time)
