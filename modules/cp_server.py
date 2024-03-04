#!/usr/bin/env python3
# coding: utf-8

from modules.utils import *
from modules.status import *
import json
import cherrypy


class BunnyHttpService(Logger):
    def __init__(self):
        Logger.__init__(self)

    @cherrypy.expose()
    def index(self):
        return "Hello Bunny!"

    @cherrypy.expose()
    def status(self):
        return json.dumps(retrieve_info(), indent=4, sort_keys=True)

    @cherrypy.expose()
    def ping(self):
        return json.dumps({"ping": "pong"}, indent=4, sort_keys=True)

    @cherrypy.expose()
    def installer(self):
        return json.dumps(get_installer(), indent=4, sort_keys=True)

    @cherrypy.expose()
    def system(self):
        return json.dumps(get_system_info(), indent=4, sort_keys=True)

    @cherrypy.expose()
    def network(self):
        return json.dumps(get_net_if_info(), indent=4, sort_keys=True)

    @cherrypy.expose()
    def disk(self):
        return json.dumps(get_disk_info(), indent=4, sort_keys=True)

    @cherrypy.expose()
    def memory(self):
        return json.dumps(get_memory_info(), indent=4, sort_keys=True)

    @cherrypy.expose()
    def cpu(self):
        return json.dumps(get_cpu_info(), indent=4, sort_keys=True)


class BunnyCherrypyServer(Logger):
    def __init__(self):
        Logger.__init__(self)

    def start(self):
        cherrypy.tree.mount(BunnyHttpService(), '/')
        try:
            self._logger.info("Unregistering previous server...")
            cherrypy.server.unsubscribe()
            self._logger.info("Registering new server...")
            HTTP_SERVER = cherrypy._cpserver.Server()
            HTTP_SERVER.socket_host = SERVER_CONFIG['agent']['bind']
            HTTP_SERVER.socket_port = SERVER_CONFIG['agent']['agent_http_port']
            HTTP_SERVER.thread_pool = SERVER_CONFIG['agent']['agent_http_thread_pool']
            HTTP_SERVER.max_request_body_size = 300 * 1024 * 1024
            HTTP_SERVER.subscribe()
            self._logger.info("Registering http server...")
            cherrypy.engine.start()
            self._logger.info("Blocking http threads...")
            cherrypy.engine.block()
        except Exception as e:
            self._logger.fatal(e)
            exit(1)

#bcp = BunnyCherrypyServer()
#bcp.start()


