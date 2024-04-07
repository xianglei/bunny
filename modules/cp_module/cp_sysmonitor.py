#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cherrypy
from modules.status import *
import json
import cherrypy_cors
from modules.kadm5 import *
cherrypy_cors.install()


@cherrypy.expose()
class BunnySysStatus(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    def GET(self):
        self._logger.info("Retrieving system status...")
        return json.dumps(retrieve_info(), indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class BunnySysCpu(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    def GET(self):
        self._logger.info("Retrieving cpu status...")
        return json.dumps(get_cpu_info(), indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class BunnySysMemory(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    def GET(self):
        self._logger.info("Retrieving memory status...")
        return json.dumps(get_memory_info(), indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class BunnySysStorage(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    def GET(self):
        self._logger.info("Retrieving storage status...")
        return json.dumps(get_disk_info(), indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class BunnySysNetwork(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    def GET(self):
        self._logger.info("Retrieving network status...")
        return json.dumps(get_net_if_info(), indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class BunnySysInstaller(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    def GET(self):
        self._logger.info("Retrieving installer status...")
        return json.dumps(get_installer(), indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class BunnySysSystem(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    def GET(self):
        self._logger.info("Retrieving system status...")
        return json.dumps(get_system_info(), indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class BunnySysServices(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    def POST(self):
        self._logger.info("Retrieving services status...")
        cl = int(cherrypy.request.headers['Content-Length'])
        body = json.loads(cherrypy.request.body.read(cl))
        if 'services' in body:
            procs = body['services']
            # proc should be a list of strings
            # ["namenode", "datanode"]
            if len(procs) > 0:
                # 第一次查询写入 run/services.rpc.cache 文件保存当前状态, 未来版本用于grpc心跳上报
                cache_file = RUN_DIR + 'services.rpc.cache'
                if not os.path.exists(cache_file):
                    self._logger.debug("Creating cache file: " + cache_file)
                    with open(cache_file, 'wb') as f:
                        pack_string(procs, f)
                else:
                    # 如果缓存状态中的进程名与发送来的不一样, 则写入新的状态
                    with open(cache_file, 'rb') as f:
                        self._logger.debug("Reading cache file: " + cache_file)
                        old_procs = unpack_binary(f)
                        if old_procs != procs:
                            self._logger.debug("Writing new cache file: " + cache_file)
                            with open(cache_file, 'wb') as g:
                                pack_string(procs, g)
                            g.close()
                    f.close()
                checked_procs = []
                for proc in procs:
                    self._logger.debug("Checking service: " + proc)
                    exists, pid = check_process_exists(proc)
                    self._logger.debug("Service: " + proc + " exists: " + str(exists) + " pid: " + str(pid))
                    if exists and pid != -1:
                        self._logger.info("Service: " + proc + " is running")
                        checked_procs.append({"service": proc, "status": True, "pid": pid})
                    else:
                        self._logger.info("Service: " + proc + " is not running")
                        checked_procs.append({"service": proc, "status": False, "pid": pid})
                return json.dumps(checked_procs, indent=4, sort_keys=True).encode('utf-8')
            else:
                return json.dumps([{"service": None}], indent=4, sort_keys=True).encode('utf-8')
        else:
            return json.dumps([{"service": None}], indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class BunnySysPing(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    def GET(self):
        return json.dumps({"ping": "pong"}, indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class BunnySysService(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.tools.accept(media='application/json')
    def POST(self):
        self._logger.info("Retrieving single service status...")
        cl = int(cherrypy.request.headers['Content-Length'])
        body = json.loads(cherrypy.request.body.read(cl))
        if 'service' in body:
            proc = body['service']
            exists, pid = check_process_exists(proc)
            if exists and pid != -1:
                self._logger.info("Service: " + proc + " is running")
                return json.dumps({"service": proc, "status": True, "pid": pid}, indent=4, sort_keys=True).encode('utf-8')
            else:
                self._logger.info("Service: " + proc + " is not running")
                return json.dumps({"service": proc, "status": False, "pid": -1}, indent=4, sort_keys=True).encode('utf-8')
        else:
            return json.dumps({"service": None}, indent=4, sort_keys=True)


class BunnyHttpService(Logger):
    def __init__(self):
        Logger.__init__(self)

    @cherrypy.expose()
    def index(self):
        return "Say Hello to little Bunny!".encode('utf-8')
