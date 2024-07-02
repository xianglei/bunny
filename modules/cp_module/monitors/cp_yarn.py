#!/usr/bin/env python3
# coding: utf-8


import cherrypy
import json
from modules.utils import *
import cherrypy_cors
import requests
cherrypy_cors.install()


@cherrypy.expose()
class YARNJmxResourceManagerWithArgsMonitor(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    # @cherrypy.popargs('resourcemanager_ip', 'resourcemanager_port', 'args')
    # def GET(self, resourcemanager_ip, resourcemanager_port=8088, args='Hadoop:service=ResourceManager,name=RMNMInfo'):
    def GET(self, *args, **kwargs):
        try:
            if len(args) >= 2:
                resourcemanager_ip = args[0]
                resourcemanager_port = args[1]
            else:
                raise cherrypy.HTTPError(400, "Missing required parameter: ip and port")

            if len(args) == 3:
                qry = args[2]
            else:
                qry = None
            if not qry or qry is None:
                url = f"http://{resourcemanager_ip}:{resourcemanager_port}/jmx"
            else:
                url = f"http://{resourcemanager_ip}:{resourcemanager_port}/jmx?qry={qry}"
            response = requests.get(url, timeout=5)
            data = response.json()
            return json.dumps(data)
        except Exception as e:
            return json.dumps({'error': str(e)})


@cherrypy.expose()
class YARNJmxNodeManagerWithArgsMonitor(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    # @cherrypy.popargs('nodemanager_ip', 'nodemanager_port', 'args')
    # def GET(self, nodemanager_ip, nodemanager_port, args='Hadoop:service=NodeManager,name=NodeManagerMetrics'):
    def GET(self, *args, **kwargs):
        try:
            if len(args) >= 2:
                nodemanager_ip = args[0]
                nodemanager_port = args[1]
            else:
                raise cherrypy.HTTPError(400, "Missing required parameter: ip and port")

            if len(args) == 3:
                qry = args[2]
            else:
                qry = None
            if not qry or qry is None:
                url = f"http://{nodemanager_ip}:{nodemanager_port}/jmx"
            else:
                url = f"http://{nodemanager_ip}:{nodemanager_port}/jmx?qry={qry}"
            response = requests.get(url, timeout=5)
            data = response.json()
            return json.dumps(data)
        except Exception as e:
            return json.dumps({'error': str(e)})


@cherrypy.expose()
class YARNJmxHistoryserverWithArgsMonitor(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    # @cherrypy.popargs('historyserver_ip', 'historyserver_port', 'args')
    # def GET(self, historyserver_ip, historyserver_port=19888, args=None):
    def GET(self, *args, **kwargs):
        try:
            if len(args) >= 2:
                historyserver_ip = args[0]
                historyserver_port = args[1]
            else:
                raise cherrypy.HTTPError(400, "Missing required parameter: ip and port")

            if len(args) == 3:
                qry = args[2]
            else:
                qry = None
            if not qry or qry is None:
                url = f"http://{historyserver_ip}:{historyserver_port}/jmx"
            else:
                url = f"http://{historyserver_ip}:{historyserver_port}/jmx?qry={qry}"
            response = requests.get(url, timeout=5)
            data = response.json()
            return json.dumps(data)
        except Exception as e:
            return json.dumps({'error': str(e)})



