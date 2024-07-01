#!/usr/bin/env python3
# coding: utf-8

from modules.cp_module.cp_headers import *
from modules.utils import *
import requests
import json
import cherrypy_cors
cherrypy_cors.install()


@cherrypy.expose()
class HBaseJmxMasterAllMonitor(Logger):
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
    @cherrypy.popargs('master_ip', 'master_port')
    def GET(self, master_ip, master_port=16010):
        try:
            url = f"http://{master_ip}:{master_port}/jmx"
            response = requests.get(url)
            data = response.json()
            return json.dumps(data)
        except Exception as e:
            return json.dumps({'error': str(e)})


@cherrypy.expose()
class HBaseJmxMasterWithArgsMonitor(Logger):
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
    @cherrypy.popargs('master_ip', 'master_port', 'args')
    def GET(self, master_ip, master_port=16010, args='Hadoop:service=Master,name=Master'):
        try:
            url = f"http://{master_ip}:{master_port}/jmx?qry={args}"
            response = requests.get(url)
            data = response.json()
            return json.dumps(data)
        except Exception as e:
            return json.dumps({'error': str(e)})


@cherrypy.expose()
class HBaseJmxRegionServerAllMonitor(Logger):
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
    @cherrypy.popargs('regionserver_ip', 'regionserver_port')
    def GET(self, regionserver_ip, regionserver_port=16030):
        try:
            url = f"http://{regionserver_ip}:{regionserver_port}/jmx"
            response = requests.get(url)
            data = response.json()
            return json.dumps(data)
        except Exception as e:
            return json.dumps({'error': str(e)})


@cherrypy.expose()
class HBaseJmxRegionServerWithArgsMonitor(Logger):
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
    @cherrypy.popargs('regionserver_ip', 'regionserver_port', 'args')
    def GET(self, regionserver_ip, regionserver_port=16030, args='Hadoop:service=RegionServer,name=RegionServer'):
        try:
            url = f"http://{regionserver_ip}:{regionserver_port}/jmx?qry={args}"
            response = requests.get(url)
            data = response.json()
            return json.dumps(data)
        except Exception as e:
            return json.dumps({'error': str(e)})


















