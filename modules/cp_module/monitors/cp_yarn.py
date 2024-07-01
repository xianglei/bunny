#!/usr/bin/env python3
# coding: utf-8


from modules.cp_module.cp_headers import *
import json
from modules.utils import *
import cherrypy_cors
import requests
cherrypy_cors.install()


@cherrypy.expose()
class YARNJmxResourceManagerAllMonitor(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
                'tools.disable_content_length.on': True,
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.popargs('resourcemanager_ip', 'resourcemanager_port')
    def GET(self, resourcemanager_ip, resourcemanager_port=8088):
        try:
            url = f"http://{resourcemanager_ip}:{resourcemanager_port}/jmx"
            response = requests.get(url)
            data = response.json()
            return json.dumps(data)
        except Exception as e:
            return json.dumps({'error': str(e)})


@cherrypy.expose()
class YARNJmxResourceManagerWithArgsMonitor(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
                'tools.disable_content_length.on': True,
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.popargs('resourcemanager_ip', 'resourcemanager_port', 'args')
    def GET(self, resourcemanager_ip, resourcemanager_port=8088, args='Hadoop:service=ResourceManager,name=RMNMInfo'):
        try:
            url = f"http://{resourcemanager_ip}:{resourcemanager_port}/jmx?qry={args}"
            response = requests.get(url)
            data = response.json()
            return json.dumps(data)
        except Exception as e:
            return json.dumps({'error': str(e)})


@cherrypy.expose()
class YARNJmxNodeManagerAllMonitor(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
                'tools.disable_content_length.on': True,
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.popargs('nodemanager_ip', 'nodemanager_port')
    def GET(self, nodemanager_ip, nodemanager_port):
        try:
            url = f"http://{nodemanager_ip}:{nodemanager_port}/jmx"
            response = requests.get(url)
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
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
                'tools.disable_content_length.on': True,
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.popargs('nodemanager_ip', 'nodemanager_port', 'args')
    def GET(self, nodemanager_ip, nodemanager_port, args='Hadoop:service=NodeManager,name=NodeManagerMetrics'):
        try:
            url = f"http://{nodemanager_ip}:{nodemanager_port}/jmx?qry={args}"
            response = requests.get(url)
            data = response.json()
            return json.dumps(data)
        except Exception as e:
            return json.dumps({'error': str(e)})


@cherrypy.expose()
class YARNJmxHistoryserverAllMonitor(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
                'tools.disable_content_length.on': True,
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.popargs('historyserver_ip', 'historyserver_port')
    def GET(self, historyserver_ip, historyserver_port=19888):
        try:
            url = f"http://{historyserver_ip}:{historyserver_port}/jmx"
            response = requests.get(url)
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
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
                'tools.disable_content_length.on': True,
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.popargs('historyserver_ip', 'historyserver_port', 'args')
    def GET(self, historyserver_ip, historyserver_port=19888, args='Hadoop:service=JobHistoryServer,name=MetricsSystem,sub=Stats'):
        try:
            url = f"http://{historyserver_ip}:{historyserver_port}/jmx?qry={args}"
            response = requests.get(url)
            data = response.json()
            return json.dumps(data)
        except Exception as e:
            return json.dumps({'error': str(e)})



