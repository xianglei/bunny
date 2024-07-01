#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.cp_module.cp_headers import *
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
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
                'tools.disable_content_length.on': True,
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.popargs('namenode_ip', 'namenode_port', 'namenode_args')
    def GET(self, namenode_ip, namenode_port=9870, namenode_args='Hadoop:service=NameNode,name=NameNodeInfo'):
        """
        Get HDFS status
        :return:
        """
        self._logger.info("Getting HDFS status...")
        try:
            url = f"http://{namenode_ip}:{namenode_port}/jmx?qry={namenode_args}"
            self._logger.debug(f"URL: {url}")
            response = requests.get(url, timeout=5).json()
            self._logger.debug(f"Response: {response}")
            return json.dumps(response, indent=4, sort_keys=True).encode('utf-8')
        except Exception as e:
            self._logger.error("HDFS status failed: {}".format(str(e)))
            return json.dumps({"status": "failed", "message": str(e)}, indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class HDFSJmxNamenodeAllMonitor(Logger):
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
    @cherrypy.popargs('namenode_ip', 'namenode_port')
    def GET(self, namenode_ip, namenode_port=9870):
        """
        Get HDFS status
        :return:
        """
        self._logger.info("Getting HDFS status...")
        try:
            url = f"http://{namenode_ip}:{namenode_port}/jmx"
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
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
                'tools.disable_content_length.on': True,
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.popargs('datanode_ip', 'datanode_port', 'datanode_args')
    def GET(self, datanode_ip, datanode_port=9864, datanode_args='Hadoop:service=DataNode,name=DataNodeInfo'):
        """
        Get HDFS status
        :return:
        """
        self._logger.info("Getting HDFS status...")
        try:
            url = f"http://{datanode_ip}:{datanode_port}/jmx?qry={datanode_args}"
            self._logger.debug(f"URL: {url}")
            response = requests.get(url, timeout=5).json()
            self._logger.debug(f"Response: {response}")
            return json.dumps(response, indent=4, sort_keys=True).encode('utf-8')
        except Exception as e:
            self._logger.error("HDFS status failed: {}".format(str(e)))
            return json.dumps({"status": "failed", "message": str(e)}, indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class HDFSJmxDatanodeAllMonitor(Logger):
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
    @cherrypy.popargs('datanode_ip', 'datanode_port')
    def GET(self, datanode_ip, datanode_port=9864):
        """
        Get HDFS status
        :return:
        """
        self._logger.info("Getting HDFS status...")
        try:
            url = f"http://{datanode_ip}:{datanode_port}/jmx"
            self._logger.debug(f"URL: {url}")
            response = requests.get(url, timeout=5).json()
            self._logger.debug(f"Response: {response}")
            return json.dumps(response, indent=4, sort_keys=True).encode('utf-8')
        except Exception as e:
            self._logger.error("HDFS status failed: {}".format(str(e)))
            return json.dumps({"status": "failed", "message": str(e)}, indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class HDFSJmxSecondaryNamenodeAllMonitor(Logger):
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
    @cherrypy.popargs('secondary_namenode_ip', 'secondary_namenode_port')
    def GET(self, secondary_namenode_ip, secondary_namenode_port=9868):
        """
        Get HDFS status
        :return:
        """
        self._logger.info("Getting HDFS status...")
        try:
            url = f"http://{secondary_namenode_ip}:{secondary_namenode_port}/jmx"
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
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
                'tools.disable_content_length.on': True,
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.popargs('secondary_namenode_ip', 'secondary_namenode_port', 'secondary_namenode_args')
    def GET(self, secondary_namenode_ip, secondary_namenode_port=9868, secondary_namenode_args='Hadoop:service=SecondaryNameNode,name=SecondaryNameNodeInfo'):
        """
        Get HDFS status
        :return:
        """
        self._logger.info("Getting HDFS status...")
        try:
            url = f"http://{secondary_namenode_ip}:{secondary_namenode_port}/jmx?qry={secondary_namenode_args}"
            self._logger.debug(f"URL: {url}")
            response = requests.get(url, timeout=5).json()
            self._logger.debug(f"Response: {response}")
            return json.dumps(response, indent=4, sort_keys=True).encode('utf-8')
        except Exception as e:
            self._logger.error("HDFS status failed: {}".format(str(e)))
            return json.dumps({"status": "failed", "message": str(e)}, indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class HDFSJmxJournalNodeAllMonitor(Logger):
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
    @cherrypy.popargs('journalnode_ip', 'journalnode_port')
    def GET(self, journalnode_ip, journalnode_port=8480):
        """
        Get HDFS status
        :return:
        """
        self._logger.info("Getting HDFS status...")
        try:
            url = f"http://{journalnode_ip}:{journalnode_port}/jmx"
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
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
                'tools.disable_content_length.on': True,
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.popargs('journalnode_ip', 'journalnode_port', 'journalnode_args')
    def GET(self, journalnode_ip, journalnode_port=8480, journalnode_args='Hadoop:service=JournalNode,name=JournalNodeInfo'):
        """
        Get HDFS status
        :return:
        """
        self._logger.info("Getting HDFS status...")
        try:
            url = f"http://{journalnode_ip}:{journalnode_port}/jmx?qry={journalnode_args}"
            self._logger.debug(f"URL: {url}")
            response = requests.get(url, timeout=5).json()
            self._logger.debug(f"Response: {response}")
            return json.dumps(response, indent=4, sort_keys=True).encode('utf-8')
        except Exception as e:
            self._logger.error("HDFS status failed: {}".format(str(e)))
            return json.dumps({"status": "failed", "message": str(e)}, indent=4, sort_keys=True).encode('utf-8')


















