#!/usr/bin/env python3
# coding: utf-8

import cherrypy
from modules.utils import *
import requests
import json
import cherrypy_cors
cherrypy_cors.install()


@cherrypy.expose()
class HBaseJmxMasterWithArgsMonitor(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    # @cherrypy.popargs('master_ip', 'master_port', 'args')
    # def GET(self, master_ip, master_port=16010, args='Hadoop:service=Master,name=Master'):
    def GET(self, *args, **kwargs):
        try:
            if len(args) >= 2:
                master_ip = args[0]
                master_port = args[1]
            else:
                raise cherrypy.HTTPError(400, "Missing required parameter: ip and port")

            if len(args) == 3:
                qry = args[2]
            else:
                qry = None
            if not qry or qry is None:
                url = f"http://{master_ip}:{master_port}/jmx"
            else:
                url = f"http://{master_ip}:{master_port}/jmx?qry={qry}"
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
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    # @cherrypy.popargs('regionserver_ip', 'regionserver_port', 'args')
    # def GET(self, regionserver_ip, regionserver_port=16030, args='Hadoop:service=RegionServer,name=RegionServer'):
    def GET(self, *args, **kwargs):
        try:
            if len(args) >= 2:
                regionserver_ip = args[0]
                regionserver_port = args[1]
            else:
                raise cherrypy.HTTPError(400, "Missing required parameter: ip and port")

            if len(args) == 3:
                qry = args[2]
            else:
                qry = None
            if not qry or qry is None:
                url = f"http://{regionserver_ip}:{regionserver_port}/jmx"
            else:
                url = f"http://{regionserver_ip}:{regionserver_port}/jmx?qry={qry}"
            response = requests.get(url)
            data = response.json()
            return json.dumps(data)
        except Exception as e:
            return json.dumps({'error': str(e)})


















