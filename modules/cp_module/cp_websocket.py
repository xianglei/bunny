#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ws4py.websocket import WebSocket
import threading
import cherrypy
from urllib.parse import urlparse, parse_qs
from modules.utils import *
import select

cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"


allowed_suffixes = ['.log', '.out']


class TailWebSocketHandler(WebSocket, Logger):
    def __init__(self, *args, **kwargs):
        super(TailWebSocketHandler, self).__init__(*args, **kwargs)
        Logger.__init__(self)
        self.filepath = None
        self.t = None

    def read_log(self, stop=False):
        try:
            cmd = ['tail', '-F', self.filepath]
            with subprocess.Popen(['tail', '-F', self.filepath],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE) as p:
                self._logger.debug('Tail process started with pid={} and cmd={} and args={}'.format(p.pid, ' '.join(cmd), p.args))
                if is_linux():
                    self._logger.info("Is linux, Using epoll")
                    select.epoll().register(p.stdout)
                while True:
                    line = p.stdout.readline()
                    if stop:
                        self._logger.info("read_log stopped")
                        break
                    else:
                        self.send(line)
        except Exception as e:
            self._logger.error(e)

    def opened(self):
        url = cherrypy.request.query_string
        self._logger.info('Connected, remote={}, url={}'.format(self.peer_address, url))
        try:
            try:
                parse_result = urlparse(url)
                self._logger.info('parse_result={}'.format(parse_result))
            except Exception:
                self._logger.error('Fail to parse URL')
                self.read_log(stop=True)
                self.send('<font color="red"><strong>Fail to parse URL</strong></font>')
                raise ValueError('Fail to parse URL')
            self.filepath = os.path.abspath(parse_qs(parse_result.path)['logfile'][0])
            self._logger.info('websocket log file_path={}'.format(self.filepath))
            allowed = False
            for suffix in allowed_suffixes:
                if self.filepath.endswith(suffix):
                    allowed = True
                    break
            self._logger.debug('allowed={}'.format(allowed))
            if not allowed:
                self._logger.error('File access not allowed')
                self.send('<font color="red"><strong>Not allowed</strong></font>')
            if not os.path.isfile(self.filepath):
                self._logger.error('File not found')
                self.send('<font color="red"><strong>File not found</strong></font>')
            self._logger.info('Start reading log file')
            self.read_log(stop=False)
        except ValueError as e:
            try:
                self.send('<font color="red"><strong>{}</strong></font>'.format(e))
                self._logger.error('Closed, remote={}, url={}, error={}'.format(self.peer_address, url, e))
                self.close()
            except Exception:
                pass
            self._logger.error('Closed, remote={}, url={}'.format(self.peer_address, url))
        except Exception as e:
            self._logger.error('Closed, remote={}, exception={}, url={}'.format(self.peer_address, e, url))
        else:
            self._logger.error('Closed, remote={}, url={}'.format(self.peer_address, url))

    def received_message(self, message):
        self.send(message.data, message.is_binary)

    def closed(self, code, reason=None):
        self.close()
        self.read_log(stop=True)
        if threading.current_thread().is_alive():
            self.t.join(timeout=1)
            self._logger.info("LogWebSocketHandler has been stopped")
        else:
            self._logger.info("LogWebSocketHandler has been closed")


class BunnyWebsocket(Logger):
    conf = {
        '/logs': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': TailWebSocketHandler
        }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.expose
    def logs(self, logfile=None, tail=None):
        pass
