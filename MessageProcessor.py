"""A chain implementator of message processor."""
import urllib
import json
from abc import ABCMeta, abstractmethod

class AbstractMessageProcessor(object): #pylint: disable=too-few-public-methods
    """AbstractMessageProcessor"""
    __metaclass__ = ABCMeta

    def __init__(self, nextProcessor=None):
        self._nextprocessor = nextProcessor

    def process(self, message):
        """chain process"""
        if self._support(message):
            return self._doprocess(message)
        return self._nextprocessor.process(message)

    @abstractmethod
    def _support(self, message):
        """Judge if the processor support this kind of message"""
        pass

    @abstractmethod
    def _doprocess(self, message):
        """Process the message"""
        pass

class ProcessorClient(object): #pylint: disable=too-few-public-methods
    """client"""

    def __init__(self):
        self.handler = GreetingsProcessor(CarwashProcessor(DefualtProcessor()))

    def handlemessage(self, message):
        """will handle all message"""
        return self.handler.process(message)

class DefualtProcessor(AbstractMessageProcessor): #pylint: disable=too-few-public-methods
    """Default"""
    def _support(self, message):
        return True

    def _doprocess(self, message):
        return u"default answer:" + message['content']['data']
        #return message['content']['data']

class GreetingsProcessor(AbstractMessageProcessor): #pylint: disable=too-few-public-methods
    """Greetings inherits"""
    greetingsVolcabulary = {'hello', 'hi'}

    def _support(self, message):
        for word in self.greetingsVolcabulary:
            if message['content']['data'].find(word) != -1:
                return True
        return False

    def _doprocess(self, message):
        return u'Hello, I am a bot.'

class CarwashProcessor(AbstractMessageProcessor):
    """car wash inherits. Using yahoo apis"""

    def __init__(self, next_processor=None):
        super(CarwashProcessor, self).__init__(next_processor)
        self.caredays = 7

    def _support(self, message):
        return message['content']['data'].find('carwash') != -1

    def _doprocess(self, message):
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = 'select * from weather.forecast where woeid in (2157249) and u="c"'
        yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
        result = urllib.urlopen(yql_url).read()
        data = json.loads(result)
        forcast_list = data['query']['results']['channel']['item']['forecast']
        count = 0
        for theforcast in forcast_list:
            count = count+1
            if count <= self.caredays and not self.is_clear(theforcast):
                return "Please don't wash your car. Cause it may be {} on {} {}" \
                    .format(theforcast['text'], theforcast['date'], theforcast['day'])
        return "You can wash your car today."

    @classmethod
    def is_clear(cls, forcast):
        """see if it is clear on that day"""
        const_keywords = {"rain", "shower", "snow", "sleet", "drizzle",
                          "storm", "tornado", "hurricane"}
        for keyword in const_keywords:
            if forcast['text'].find(keyword) != -1:
                return False
        return True
