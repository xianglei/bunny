#!/usr/bin/env python3
# coding: utf-8

from modules.utils import *
import kadmin


class Kadmin5(Logger):
    """
    keytab should be full path and name of the keytab file
    ex: keytab = "/etc/security/keytabs/hdfs.headless.keytab"
    """
    def __init__(self, admin_pricipal, admin_password=None, admin_keytab=None, realm="EXAMPLE.COM"):
        Logger.__init__(self)
        self._logger.info("kadmin5 module initialized")
        self._realm = realm
        self._kadmin = None
        self._admin_principal = admin_pricipal
        if admin_password is None and admin_keytab is None:
            self._logger.fatal("password or credential must be provided")
            raise ValueError("password or credential must be provided")
        self._admin_password = admin_password
        self._admin_keytab = admin_keytab
        self._logger.debug("admin_principal: {}, admin_password: {}, admin_keytab: {}, realm: {}".format(
            self._admin_principal, self._admin_password, self._admin_keytab, self._realm))
        if self._admin_password is not None:
            self._logger.debug("kadmin init with password")
            try:
                self._kadmin = kadmin.init_with_password(self._admin_principal, self._admin_password)
                self._logger.info("kadmin initialized with password")
            except Exception as e:
                self._logger.error("kadmin init with password failed: {}".format(e))
            #self._logger.info("kadmin initialized with password")
        if self._admin_keytab is not None:
            self._kadmin = kadmin.init_with_keytab(self._admin_principal, self._admin_keytab)
            self._logger.info("kadmin initialized with keytab")

    """
    def kadmin_init(self):
        if self._admin_password is not None:
            self._kadmin = kadmin.init_with_password(self._admin_principal, self._admin_password)
            return True
        if self._admin_keytab is not None:
            self._kadmin = kadmin.init_with_keytab(self._admin_principal, self._admin_keytab)
            return True
        return False
    """

    def add_princ(self, user, fqdn=None):
        if fqdn is None:
            fqdn, ip = self_ip_hostname()
        princ = user + '/' + fqdn + "@" + self._realm
        if self._kadmin.principal_exists(princ):
            self._logger.info("principal already exists")
            return False
        else:
            try:
                self._kadmin.ank(princ, None)
                self._logger.info("principal created")
                return True
            except kadmin.KAdminError as e:
                self._logger.error("create principal failed: {}".format(e))
                return False

    def del_princ(self, user, fqdn=None):
        if fqdn is None:
            fqdn, ip = self_ip_hostname()
        princ = user + '/' + fqdn + "@" + self._realm
        if self._kadmin.principal_exists(princ):
            self._logger.warning("Deleting principal: {}".format(princ))
            try:
                self._kadmin.delprinc(princ)
                return True
            except kadmin.KAdminError as e:
                self._logger.error("delete principal failed: {}".format(e))
                return False
        else:
            self._logger.error("principal does not exist")
            return False

    def generate_keytab(self, user, keytab_path, fqdn=None):
        if fqdn is None:
            fqdn, ip = self_ip_hostname()
        princ = user + '/' + fqdn + "@" + self._realm
        if self._kadmin.principal_exists(princ):
            keytab = self._kadmin.getprinc(princ)
            self._logger.debug("get keytab: {}".format(keytab))
            try:
                keytab.xst(keytab_path)
                uid, gid, group = get_user_uid_gid(user)
                self._logger.debug("uid: {}, gid: {}, group: {}".format(uid, gid, group))
                os.chown(keytab_path, uid, gid)
                os.chmod(keytab_path, 0o600)
                return True
            except Exception as e:
                self._logger.error("chown and chmod failed: {}".format(e))
                return False
        else:
            self._logger.error("principal does not exist")
            return False

    def remove_keytab(self, keytab_path):
        if os.path.exists(keytab_path):
            try:
                os.chmod(keytab_path, 0o777)
                os.remove(keytab_path)
            except OSError as e:
                self._logger.error("chmod and remove keytab failed: {}".format(e))
        else:
            self._logger.info("keytab does not exist")

    def list_princs(self, keyword=None):
        principals = self._kadmin.principals()
        ret = []
        for principal in principals:
            if 'admin' or 'krbtgt' or 'K/M' or 'kiprop' in principal:
                continue
            else:
                ret.append(principal)
        return self._kadmin.principals("*" + keyword + "*@" + self._realm)

    def get_princ(self, principal):
        return self._kadmin.getprinc(principal)
