import unittest
from ws4py.client.threadedclient import WebSocketClient


class DummyClient(WebSocketClient):
    def opened(self):
        pass

    def closed(self, code, reason=None):
        pass

    def received_message(self, message):
        pass


class WSTest(unittest.TestCase):
    def setUp(self):
        self.url = 'ws://localhost:7181/logs?logfile=/var/log/system.log'
        self.client = DummyClient(self.url)

    def test_connection(self):
        print(self.client.connection)
        self.assertTrue(self.client.connection is not None)

    def test_send_message(self):
        self.client.send('Hello')
        self.assertTrue(self.client.send('Hello'))

    def tearDown(self):
        self.client.close()


if __name__ == '__main__':
    unittest.main()
