#!/usr/bin/env python3
# coding: utf-8

from modules.utils import *
import cherrypy
from modules.cp_module.cp_apis import *


def cors():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"


class BunnyCherrypyServer(Logger):
    def __init__(self):
        Logger.__init__(self)

    def start(self):
        # cherrypy.tree.mount(BunnyHttpService(), '/sys')
        global_conf = {
                'tools.cors.on': True,
                'cors.expose.on': True,
                'tools.websocket.on': True,
                'cors.allow.origin': '*',
                'cors.allow.methods': 'GET, POST, PUT, DELETE, PATCH, SEARCH',
                #'environment': 'production',
                'log.screen': False,
                'log.access_file': LOGS_DIR + 'cp_access.log',
                'log.error_file': LOGS_DIR + 'cp_error.log',
                'tools.sessions.on': True,
                'tools.encode.on': True,
                'tools.encode.encoding': 'utf-8',
                'tools.response_headers.on': True,
                'request.methods_with_bodies': ('POST', 'PUT', 'PATCH', 'GET', 'DELETE', 'SEARCH',),
                'tools.response_headers.headers': [
                    ('Content-Type', 'application/json'),
                    ('Access-Control-Allow-Origin', '*'),
                    ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE'),
                    ('Access-Control-Allow-Headers', 'Content-Type'),
                    ('Server', 'Bunny/0.1.0 (Cherrypy/18.6.0)'),
                ],
                'cherrypy.max_request_body_size': 300 * 1024 * 1024,
            }
        # cherrypy.tree.mount(BunnyKadminService(), '/kadmin')
        cherrypy.tree.mount(BunnyHttpService(), '/')
        cherrypy.tree.mount(BunnySysStatus(), '/sys', BunnySysStatus.conf)
        cherrypy.tree.mount(BunnySysCpu(), '/sys/cpu', BunnySysCpu.conf)
        cherrypy.tree.mount(BunnySysMemory(), '/sys/memory', BunnySysMemory.conf)
        cherrypy.tree.mount(BunnySysStorage(), '/sys/storage', BunnySysStorage.conf)
        cherrypy.tree.mount(BunnySysNetwork(), '/sys/network', BunnySysNetwork.conf)
        cherrypy.tree.mount(BunnySysInstaller(), '/sys/installer', BunnySysInstaller.conf)
        cherrypy.tree.mount(BunnySysSystem(), '/sys/system', BunnySysSystem.conf)
        # POST only
        cherrypy.tree.mount(BunnySysServices(), '/sys/services', BunnySysServices.conf)
        cherrypy.tree.mount(BunnySysPing(), '/sys/ping', BunnySysPing.conf)
        # POST only
        cherrypy.tree.mount(BunnySysService(), '/sys/service', BunnySysService.conf)
        # cherrypy.tree.mount(BunnyKadminPrincipal(), '/kadmin/principal', BunnyKadminPrincipal.conf)
        # cherrypy.tree.mount(BunnyKadminKeytab(), '/kadmin/keytab', BunnyKadminKeytab.conf)
        # cherrypy.tree.mount(BunnyLogTailerHandler(), '/logs', BunnyLogTailerHandler.conf)
        try:
            self._logger.info("Unregistering previous server...")
            cherrypy.server.unsubscribe()
            self._logger.info("Registering new server...")
            cherrypy.config.update(global_conf)
            HTTP_SERVER = cherrypy._cpserver.Server()
            HTTP_SERVER.socket_host = SERVER_CONFIG['agent']['bind']
            HTTP_SERVER.socket_port = SERVER_CONFIG['agent']['agent_http_port']
            HTTP_SERVER.thread_pool = SERVER_CONFIG['agent']['agent_http_thread_pool']
            #if os.path.exists(BASE_DIR + 'ssl/server.crt') and os.path.exists(BASE_DIR + 'ssl/server.key'):
            #    HTTP_SERVER.ssl_module = 'builtin'
            #    HTTP_SERVER.ssl_certificate = BASE_DIR + 'ssl/cert.pem'
            #    HTTP_SERVER.ssl_private_key = BASE_DIR + 'ssl/privkey.pem'
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


