#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cherrypy
import json
from modules.utils import *
import cherrypy_cors
import requests
cherrypy_cors.install()


@cherrypy.expose()
class HDFSJmxNamenodeWithArgsMonitor(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.popargs('namenode_ip', 'namenode_port', 'qry')
    def GET(self, *args, **kwargs):
        """
        Get HDFS status
        :return:
        """
        self._logger.info("Getting HDFS status...")
        try:
            if len(args) >= 2:
                namenode_ip = args[0]
                namenode_port = args[1]
            else:
                raise cherrypy.HTTPError(400, "Missing required parameter: ip and port")

            if len(args) == 3:
                qry = args[2]
            else:
                qry = None
            if not qry or qry is None:
                url = f"http://{namenode_ip}:{namenode_port}/jmx"
            else:
                url = f"http://{namenode_ip}:{namenode_port}/jmx?qry={qry}"
            self._logger.debug(f"URL: {url}")
            response = requests.get(url, timeout=5).json()
            self._logger.debug(f"Response: {response}")
            return json.dumps(response, indent=4, sort_keys=True).encode('utf-8')
        except Exception as e:
            self._logger.error("HDFS status failed: {}".format(str(e)))
            return json.dumps({"status": "failed", "message": str(e)}, indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class HDFSJmxDatanodeWithArgsMonitor(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    #@cherrypy.popargs('datanode_ip', 'datanode_port', 'qry')
    def GET(self, *args, **kwargs):
        """
        Get HDFS status
        :return:
        """
        self._logger.info("Getting HDFS status...")
        try:
            if len(args) >= 2:
                datanode_ip = args[0]
                datanode_port = args[1]
            else:
                raise cherrypy.HTTPError(400, "Missing required parameter: ip and port")

            if len(args) == 3:
                qry = args[2]
            else:
                qry = None

            if not qry or qry is None:
                url = f"http://{datanode_ip}:{datanode_port}/jmx"
            else:
                url = f"http://{datanode_ip}:{datanode_port}/jmx?qry={qry}"
            self._logger.debug(f"URL: {url}")
            response = requests.get(url, timeout=5).json()
            self._logger.debug(f"Response: {response}")
            return json.dumps(response, indent=4, sort_keys=True).encode('utf-8')
        except Exception as e:
            self._logger.error("HDFS status failed: {}".format(str(e)))
            return json.dumps({"status": "failed", "message": str(e)}, indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class HDFSJmxSecondaryNamenodeWithArgsMonitor(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    #@cherrypy.popargs('secondary_namenode_ip', 'secondary_namenode_port', 'qry')
    def GET(self, *args, **kwargs):
        """
        Get HDFS status
        :return:
        """
        self._logger.info("Getting HDFS status...")
        try:
            if len(args) >= 2:
                secondary_namenode_ip = args[0]
                secondary_namenode_port = args[1]
            else:
                raise cherrypy.HTTPError(400, "Missing required parameter: ip and port")

            if len(args) == 3:
                qry = args[2]
            else:
                qry = None
            if not qry or qry is None:
                url = f"http://{secondary_namenode_ip}:{secondary_namenode_port}/jmx"
            else:
                url = f"http://{secondary_namenode_ip}:{secondary_namenode_port}/jmx?qry={qry}"
            self._logger.debug(f"URL: {url}")
            response = requests.get(url, timeout=5).json()
            self._logger.debug(f"Response: {response}")
            return json.dumps(response, indent=4, sort_keys=True).encode('utf-8')
        except Exception as e:
            self._logger.error("HDFS status failed: {}".format(str(e)))
            return json.dumps({"status": "failed", "message": str(e)}, indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class HDFSJmxJournalNodeWithArgsMonitor(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    def GET(self, *args, **kwargs):
        """
        Get HDFS status
        :return:
        """
        self._logger.info("Getting HDFS status...")
        try:
            if len(args) >= 2:
                journalnode_ip = args[0]
                journalnode_port = args[1]
            else:
                raise cherrypy.HTTPError(400, "Missing required parameter: ip and port")

            if len(args) == 3:
                qry = args[2]
            else:
                qry = None

            if not qry or qry is None:
                url = f"http://{journalnode_ip}:{journalnode_port}/jmx"
            else:
                url = f"http://{journalnode_ip}:{journalnode_port}/jmx?qry={qry}"
            self._logger.debug(f"URL: {url}")
            response = requests.get(url, timeout=5).json()
            self._logger.debug(f"Response: {response}")
            return json.dumps(response, indent=4, sort_keys=True).encode('utf-8')
        except Exception as e:
            self._logger.error("HDFS status failed: {}".format(str(e)))
            return json.dumps({"status": "failed", "message": str(e)}, indent=4, sort_keys=True).encode('utf-8')


















