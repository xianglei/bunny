#!/usr/bin/env python3
# coding: utf-8

from modules.cp_module.cp_sysmonitor import *
from modules.cp_module.cp_kadmin import *
from modules.cp_module.cp_websocket import *
from modules.cp_module.monitors.cp_hdfs import *
from modules.cp_module.monitors.cp_yarn import *
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool


class DisableContentLengthTool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'before_request_body', self.check_content_length, priority=10)

    def check_content_length(self):
        if 'Content-Length' not in cherrypy.request.headers:
            cherrypy.request.headers['Content-Length'] = 0


cherrypy.tools.disable_content_length = DisableContentLengthTool()


class BunnyCherrypyServer(Logger):
    def __init__(self):
        Logger.__init__(self)

    def start(self):
        # cherrypy.tree.mount(BunnyHttpService(), '/sys')
        global_conf = {
                'cors.expose.on': True,
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
                'request.show_tracebacks': True,
                'tools.response_headers.headers': [
                    ('Content-Type', 'application/json'),
                    ('Access-Control-Allow-Origin', '*'),
                    ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE'),
                    ('Access-Control-Allow-Headers', 'Content-Type'),
                    ('Server', 'Bunny/0.1.0 (Cherrypy/18.6.0)'),
                ],
                'tools.disable_content_length.on': True,
                'cherrypy.max_request_body_size': 300 * 1024 * 1024,
            }
        # cherrypy.tree.mount(BunnyKadminService(), '/kadmin')
        # ws://10.10.10.13:7181/logs?logfile=/var/log/dnf.log
        cherrypy.tree.mount(BunnyWebsocket(), '/', BunnyWebsocket.conf)
        cherrypy.tree.mount(BunnySysStatus(), '/mon/sys', BunnySysStatus.conf)
        """
        cherrypy.tree.mount(BunnySysCpu(), '/mon/sys/cpu', BunnySysCpu.conf)
        cherrypy.tree.mount(BunnySysMemory(), '/mon/sys/memory', BunnySysMemory.conf)
        cherrypy.tree.mount(BunnySysStorage(), '/mon/sys/storage', BunnySysStorage.conf)
        cherrypy.tree.mount(BunnySysNetwork(), '/mon/sys/network', BunnySysNetwork.conf)
        cherrypy.tree.mount(BunnySysInstaller(), '/mon/sys/installer', BunnySysInstaller.conf)
        cherrypy.tree.mount(BunnySysSystem(), '/mon/sys/system', BunnySysSystem.conf)
        cherrypy.tree.mount(BunnyOsDist(), '/mon/sys/osinfo', BunnyOsDist.conf)
        """
        # POST only
        cherrypy.tree.mount(BunnySysServices(), '/mon/sys/services', BunnySysServices.conf)
        cherrypy.tree.mount(BunnySysPing(), '/mon/sys/ping', BunnySysPing.conf)
        # POST only
        cherrypy.tree.mount(BunnySysService(), '/mon/sys/service', BunnySysService.conf)
        cherrypy.tree.mount(BunnyKadminPrincipal(), '/kadmin/principal', BunnyKadminPrincipal.conf)
        cherrypy.tree.mount(BunnyKadminKeytab(), '/kadmin/keytab', BunnyKadminKeytab.conf)

        # /mon/hdfs/namenode/192.168.14.12/9870/(optional):Hadoop:service=NameNode,name=NameNodeInfo/
        cherrypy.tree.mount(HDFSJmxNamenodeWithArgsMonitor(), '/mon/hdfs/namenode', HDFSJmxNamenodeWithArgsMonitor.conf)
        # /mon/hdfs/datanode/192.168.14.13/9864/(optional):Hadoop:service=DataNode,name=DataNodeInfo/
        cherrypy.tree.mount(HDFSJmxDatanodeWithArgsMonitor(), '/mon/hdfs/datanode', HDFSJmxDatanodeWithArgsMonitor.conf)
        #cherrypy.tree.mount(HDFSJmxJournalnodeMonitor(), '/mon/hdfs/journalnode', HDFSJmxJournalnodeMonitor.conf)
        #cherrypy.tree.mount(HDFSJmxNamenodeHAStateMonitor(), '/mon/hdfs/ha', HDFSJmxNamenodeHAStateMonitor.conf)
        #cherrypy.tree.mount(HDFSJmxNamenodeHAHealthMonitor(), '/mon/hdfs/ha/health', HDFSJmxNamenodeHAHealthMonitor.conf)
        #cherrypy.tree.mount(HDFSJmxNamenodeHAStateMonitor(), '/mon/hdfs/ha/state', HDFSJmxNamenodeHAStateMonitor.conf)
        cherrypy.tree.mount(HDFSJmxSecondaryNamenodeWithArgsMonitor(), '/mon/hdfs/secondary', HDFSJmxSecondaryNamenodeWithArgsMonitor.conf)
        cherrypy.tree.mount(HDFSJmxJournalNodeWithArgsMonitor(), '/mon/hdfs/journalnode', HDFSJmxJournalNodeWithArgsMonitor.conf)
        cherrypy.tree.mount(YARNJmxResourceManagerWithArgsMonitor(), '/mon/yarn/resourcemanager', YARNJmxResourceManagerWithArgsMonitor.conf)
        cherrypy.tree.mount(YARNJmxNodeManagerWithArgsMonitor(), '/mon/yarn/nodemanager', YARNJmxNodeManagerWithArgsMonitor.conf)
        cherrypy.tree.mount(YARNJmxHistoryserverWithArgsMonitor(), '/mon/yarn/jobhistoryserver', YARNJmxHistoryserverWithArgsMonitor.conf)
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
            WebSocketPlugin(cherrypy.engine).subscribe()
            cherrypy.tools.websocket = WebSocketTool()
            self._logger.info("Registering http server...")
            cherrypy.engine.start()
            self._logger.info("Blocking http threads...")
            cherrypy.engine.block()
        except Exception as e:
            self._logger.fatal(e)
            exit(1)

#bcp = BunnyCherrypyServer()
#bcp.start()


