#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cherrypy
import json
import cherrypy_cors
from modules.kadm5 import *
cherrypy_cors.install()


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
        self._logger.debug('{}'.format(body))
        admin_principal = body['admin_principal']
        admin_password = body['admin_password']
        admin_keytab = body['admin_keytab']
        admin_keytab = None if admin_keytab == '' else admin_keytab
        admin_password = None if admin_password == '' else admin_password
        realm = body['realm']
        fqdn = body['fqdn']
        fqdn = None if fqdn == '' else fqdn
        user = body['user']
        try:
            krb5 = Kadmin5(admin_principal, admin_password, admin_keytab, realm)
            self._logger.info("Kadmin initialized")
            self._logger.info("Adding principal: " + user)
            if krb5.add_princ(user, fqdn) is True:
                return json.dumps({"principal": user, "status": "success", "message": "principal added"}, indent=4, sort_keys=True).encode('utf-8')
            else:
                return json.dumps({"principal": user, "status": "failed", "message": "Check agent log for details"}, indent=4, sort_keys=True).encode('utf-8')
        except Exception as e:
            self._logger.error("Principal add failed: {}".format(str(e)))
            return json.dumps({"principal": user, "status": "failed", "message": str(e)}, indent=4, sort_keys=True).encode('utf-8')

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
        self._logger.debug('{}'.format(body))
        admin_principal = body['admin_principal']
        admin_password = body['admin_password']
        admin_keytab = body['admin_keytab']
        admin_keytab = None if admin_keytab == '' else admin_keytab
        admin_password = None if admin_password == '' else admin_password
        realm = body['realm']
        fqdn = body['fqdn']
        fqdn = None if fqdn == '' else fqdn
        user = body['user']
        try:
            krb5 = Kadmin5(admin_principal, admin_password, admin_keytab, realm)
            self._logger.info("Kadmin initialized")
            self._logger.info("Deleting principal: " + user)
            if krb5.del_princ(user, fqdn):
                return json.dumps({"principal": user, "status": "success", "message": "principal removed"}, indent=4, sort_keys=True).encode('utf-8')
            else:
                return json.dumps({"principal": user, "status": "failed", "message": "Check agent log for details"}, indent=4, sort_keys=True).encode('utf-8')
        except Exception as e:
            self._logger.error("Principal delete failed: {}".format(str(e)))
            return json.dumps({"principal": user, "status": "failed", "message": str(e)}, indent=4, sort_keys=True).encode('utf-8')

    @cherrypy.tools.accept(media='application/json')
    def GET(self):
        self._logger.info("Listing principal...")
        cl = int(cherrypy.request.headers['Content-Length'])
        body = json.loads(cherrypy.request.body.read(cl))
        self._logger.debug('{}'.format(body))
        admin_principal = body['admin_principal']
        admin_password = body['admin_password']
        admin_keytab = body['admin_keytab']
        admin_keytab = None if admin_keytab == '' else admin_keytab
        admin_password = None if admin_password == '' else admin_password
        realm = body['realm']
        keyword = body['keyword']
        self._logger.info("Kadmin initializing...")
        try:
            krb5 = Kadmin5(admin_principal, admin_password, admin_keytab, realm)
            if keyword is not None:
                self._logger.info("Listing principal: " + keyword)
                return json.dumps({"principals": krb5.list_princs(keyword), "status": "success", "message": "principal list"}, indent=4, sort_keys=True).encode('utf-8')
            else:
                return json.dumps({"principals": krb5.list_princs(), "status": "success", "message": "principal list"}, indent=4, sort_keys=True).encode('utf-8')
        except Exception as e:
            self._logger.error("Principal list failed: {}".format(str(e)))
            return json.dumps({"status": "failed", "message": str(e)}, indent=4, sort_keys=True).encode('utf-8')


@cherrypy.expose()
class BunnyKadminKeytab(Logger):
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
        self._logger.debug('{}'.format(body))
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
        try:
            krb5 = Kadmin5(admin_principal, admin_password, admin_keytab, realm)
            self._logger.info("Kadmin initialized")
            self._logger.info("Adding keytab: " + user)
            if krb5.generate_keytab(user, keytab_path, fqdn):
                return json.dumps({"principal": user, "status": "success", "message": "keytab created", "keytab_path": keytab_path}, indent=4, sort_keys=True).encode('utf-8')
            else:
                return json.dumps({"principal": user, "status": "failed", "message": "keytab create failed, check agent log for details", "keytab_path": keytab_path}, indent=4, sort_keys=True).encode('utf-8')
        except Exception as e:
            self._logger.error("Keytab creation failed: {}".format(str(e)))
            return json.dumps({"principal": user, "status": "failed", "message": str(e), "keytab_path": keytab_path}, indent=4, sort_keys=True).encode('utf-8')

    @cherrypy.tools.accept(media='application/json')
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
        self._logger.debug('{}'.format(body))
        admin_principal = body['admin_principal']
        admin_password = body['admin_password']
        admin_keytab = body['admin_keytab']
        admin_keytab = None if admin_keytab == '' else admin_keytab
        admin_password = None if admin_password == '' else admin_password
        realm = body['realm']
        keytab_path = body['keytab_path']
        try:
            krb5 = Kadmin5(admin_principal, admin_password, admin_keytab, realm)
            self._logger.info("Kadmin initialized")
            self._logger.info("Deleting keytab: " + keytab_path)
            if krb5.remove_keytab(keytab_path):
                return json.dumps({"keytab": keytab_path, "status": "deleted"}, indent=4, sort_keys=True).encode('utf-8')
            else:
                return json.dumps({"keytab": keytab_path, "status": "failed"}, indent=4, sort_keys=True).encode('utf-8')
        except Exception as e:
            self._logger.error("Keytab delete failed: {}".format(str(e)))
            return json.dumps({"keytab": keytab_path, "status": "failed", "message": str(e)}, indent=4, sort_keys=True).encode('utf-8')
