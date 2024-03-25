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


"""
TODO:
Kerberos Admin Server on Cherrypy
"""


@cherrypy.expose()
class BunnyKadminPrincipal(Logger):
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
        """
        Add principal
        {
        "admin_principal": "admin/admin@EXAMPLE.COM",
        "admin_password": "admin_password",
        "admin_keytab": "/etc/security/keytabs/admin.keytab",
        "realm": "EXAMPLE.COM",
        "user": "user"
        }
        :return:
        """
        self._logger.info("Adding principal...")
        cl = int(cherrypy.request.headers['Content-Length'])
        body = json.loads(cherrypy.request.body.read(cl))
        admin_principal = body['admin_principal']
        admin_password = body['admin_password']
        admin_keytab = body['admin_keytab']
        admin_keytab = None if admin_keytab == '' else admin_keytab
        admin_password = None if admin_password == '' else admin_password
        realm = body['realm']
        fqdn = body['fqdn']
        fqdn = None if fqdn == '' else fqdn
        user = body['user']
        krb5 = Kadmin5(admin_principal, admin_password, admin_keytab, realm)
        self._logger.info("Kadmin initialized")
        self._logger.info("Adding principal: " + user)
        if krb5.add_princ(user, fqdn) is True:
            return json.dumps({"principal": user, "status": "success", "message": "principal added"}, indent=4, sort_keys=True).encode('utf-8')
        else:
            return json.dumps({"principal": user, "status": "failed", "message": "Check agent log for details"}, indent=4, sort_keys=True).encode('utf-8')

    @cherrypy.tools.accept(media='application/json')
    def DELETE(self):
        """
        Delete principal
        {
        "admin_principal": "admin_principal",
        "admin_password": "admin_password",
        "admin_keytab": "admin_keytab",
        "realm": "EXAMPLE.COM",
        "user": "user"
        }
        """
        self._logger.info("Deleting principal...")
        cl = int(cherrypy.request.headers['Content-Length'])
        body = json.loads(cherrypy.request.body.read(cl))
        admin_principal = body['admin_principal']
        admin_password = body['admin_password']
        admin_keytab = body['admin_keytab']
        admin_keytab = None if admin_keytab == '' else admin_keytab
        admin_password = None if admin_password == '' else admin_password
        realm = body['realm']
        fqdn = body['fqdn']
        fqdn = None if fqdn == '' else fqdn
        user = body['user']
        krb5 = Kadmin5(admin_principal, admin_password, admin_keytab, realm)
        self._logger.info("Kadmin initialized")
        self._logger.info("Deleting principal: " + user)
        if krb5.del_princ(user, fqdn):
            return json.dumps({"principal": user, "status": "success", "message": "principal removed"}, indent=4, sort_keys=True).encode('utf-8')
        else:
            return json.dumps({"principal": user, "status": "failed", "message": "Check agent log for details"}, indent=4, sort_keys=True).encode('utf-8')

    @cherrypy.tools.accept(media='application/json')
    def GET(self):
        self._logger.info("Listing principal...")
        cl = int(cherrypy.request.headers['Content-Length'])
        body = json.loads(cherrypy.request.body.read(cl))
        admin_principal = body['admin_principal']
        admin_password = body['admin_password']
        admin_keytab = body['admin_keytab']
        admin_keytab = None if admin_keytab == '' else admin_keytab
        admin_password = None if admin_password == '' else admin_password
        realm = body['realm']
        keyword = body['keyword']
        self._logger.info("Kadmin initializing...")
        krb5 = Kadmin5(admin_principal, admin_password, admin_keytab, realm)
        if keyword is not None:
            self._logger.info("Listing principal: " + keyword)
            return json.dumps({"principals": krb5.list_princs(keyword), "status": "success", "message": "principal list"}, indent=4, sort_keys=True).encode('utf-8')
        else:
            return json.dumps({"principals": krb5.list_princs(), "status": "success", "message": "principal list"}, indent=4, sort_keys=True).encode('utf-8')


class BunnyKadminKeytab(Logger):
    conf = {
        '/':
            {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
    }

    def __init__(self):
        Logger.__init__(self)

    @cherrypy.expose()
    def POST(self):
        """
        Add keytab
        {
        "admin_principal": "admin_principal",
        "admin_password": "admin_password",
        "admin_keytab": "admin_keytab",
        "realm": "EXAMPLE.COM",
        "user": "user",
        "fqdn": "_HOST",
        "keytab_path": "/etc/security/keytabs/user.keytab"
        }
        """
        self._logger.info("Adding keytab...")
        cl = int(cherrypy.request.headers['Content-Length'])
        body = json.loads(cherrypy.request.body.read(cl))
        admin_principal = body['admin_principal']
        admin_password = body['admin_password']
        admin_keytab = body['admin_keytab']
        realm = body['realm']
        user = body['user']
        keytab_path = body['keytab_path']
        admin_keytab = None if admin_keytab == '' else admin_keytab
        admin_password = None if admin_password == '' else admin_password
        fqdn = body['fqdn']
        fqdn = None if fqdn == '' else fqdn
        krb5 = Kadmin5(admin_principal, admin_password, admin_keytab, realm)
        self._logger.info("Kadmin initialized")
        self._logger.info("Adding keytab: " + user)
        if krb5.generate_keytab(user, keytab_path, fqdn):
            return json.dumps({"principal": user, "status": "success", "message": "keytab created", "keytab_path": keytab_path}, indent=4, sort_keys=True).encode('utf-8')
        else:
            return json.dumps({"principal": user, "status": "failed", "message": "keytab create failed, check agent log for details", "keytab_path": keytab_path}, indent=4, sort_keys=True).encode('utf-8')

    def DELETE(self):
        """
        Delete keytab
        {
        "admin_principal": "admin_principal",
        "admin_password": "admin_password",
        "admin_keytab": "admin_keytab",
        "realm": "EXAMPLE.COM",
        "user": "user",
        "fqdn": "_HOST",
        "keytab_path": "/etc/security/keytabs/user.keytab"
        }
        """
        self._logger.info("Deleting keytab...")
        cl = int(cherrypy.request.headers['Content-Length'])
        body = json.loads(cherrypy.request.body.read(cl))
        admin_principal = body['admin_principal']
        admin_password = body['admin_password']
        admin_keytab = body['admin_keytab']
        admin_keytab = None if admin_keytab == '' else admin_keytab
        admin_password = None if admin_password == '' else admin_password
        realm = body['realm']
        keytab_path = body['keytab_path']
        krb5 = Kadmin5(admin_principal, admin_password, admin_keytab, realm)
        self._logger.info("Kadmin initialized")
        self._logger.info("Deleting keytab: " + keytab_path)
        if krb5.remove_keytab(keytab_path):
            return json.dumps({"keytab": keytab_path, "status": "deleted"}, indent=4, sort_keys=True).encode('utf-8')
        else:
            return json.dumps({"keytab": keytab_path, "status": "failed"}, indent=4, sort_keys=True).encode('utf-8')



