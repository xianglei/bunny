#!/usr/bin/env python3
# coding: utf-8

from modules.utils import *
import re
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


def validate_principal(principal):
    PATTERN_GROUPUSER_NAME = (
        '(?!^[0-9]+$)^[a-zA-Z0-9_.][a-zA-Z0-9_.-]*[a-zA-Z0-9_.$-]?$'
    )
    PATTERN_REALM = '@?([a-zA-Z0-9.-]*)$'
    PATTERN_PRINCIPAL = '(' + PATTERN_GROUPUSER_NAME[:-1] + ')' + PATTERN_REALM
    PATTERN_SERVICE = '([a-zA-Z0-9.-]+)/([a-zA-Z0-9.-]+)' + PATTERN_REALM

    user_pattern = re.compile(PATTERN_PRINCIPAL)
    service_pattern = re.compile(PATTERN_SERVICE)
    if not isinstance(principal, str):
        raise RuntimeError('Invalid principal: not a string')
    if ('/' in principal) and (' ' in principal):
        raise RuntimeError('Invalid principal: bad spacing')
    else:
        # For a user match in the regex
        # username = match[1]
        # realm = match[2]
        match = user_pattern.match(principal)
        if match is None:
            match = service_pattern.match(principal)
            if match is None:
                raise RuntimeError('Invalid principal: cannot parse')
            else:
                # service = match[1]
                hostname = match[2]
                # realm = match[3]
                try:
                    validate_hostname(hostname)
                except ValueError as e:
                    raise RuntimeError(str(e))


def validate_hostname(hostname, check_fqdn=True, allow_underscore=False, allow_slash=False, maxlen=255):
    """ See RFC 952, 1123

    Length limit of 64 imposed by MAXHOSTNAMELEN on Linux.

    DNS and other operating systems has a max length of 255. Default to
    the theoretical max unless explicitly told to limit. The cases
    where a limit would be set might include:
     * *-install --hostname
     * ipa host-add

    The *-install commands by definition are executed on Linux hosts so
    the maximum length needs to be limited.

    :param hostname Checked value
    :param check_fqdn Check if hostname is fully qualified
    """
    if len(hostname) > maxlen:
        raise ValueError('cannot be longer that {} characters'.format(
            maxlen))

    if hostname.endswith('.'):
        hostname = hostname[:-1]

    if '..' in hostname:
        raise ValueError('hostname contains empty label (consecutive dots)')

    if '.' not in hostname:
        if check_fqdn:
            raise ValueError('not fully qualified')
        validate_dns_label(hostname, allow_underscore, allow_slash)
    else:
        validate_domain_name(hostname, allow_underscore, allow_slash)


def validate_dns_label(dns_label, allow_underscore=False, allow_slash=False):
    base_chars = 'a-z0-9'
    extra_chars = ''
    middle_chars = ''

    if allow_underscore:
        extra_chars += '_'
    if allow_slash:
        middle_chars += '/'

    middle_chars = middle_chars + '-' # has to be always the last in the regex [....-]

    label_regex = r'''^[%(base)s%(extra)s] # must begin with an alphanumeric
                                           # character, or underscore if
                                           # allow_underscore is True
        ([%(base)s%(extra)s%(middle)s]*    # can contain all allowed character
                                           # classes in the middle
        [%(base)s%(extra)s])*$             # must end with alphanumeric
                                           # character or underscore if
                                           # allow_underscore is True
        ''' % dict(base=base_chars, extra=extra_chars, middle=middle_chars)
    regex = re.compile(label_regex, re.IGNORECASE | re.VERBOSE)

    if not dns_label:
        raise ValueError('empty DNS label')

    if len(dns_label) > 63:
        raise ValueError('DNS label cannot be longer that 63 characters')

    if not regex.match(dns_label):
        chars = ', '.join("'%s'" % c for c in extra_chars + middle_chars)
        chars2 = ', '.join("'%s'" % c for c in middle_chars)
        raise ValueError("only letters, numbers, %(chars)s are allowed. "
                         "DNS label may not start or end with %(chars2)s"
                         % dict(chars=chars, chars2=chars2))


def validate_domain_name(
        domain_name, allow_underscore=False,
        allow_slash=False, entity='domain'
):
    if domain_name.endswith('.'):
        domain_name = domain_name[:-1]

    domain_name = domain_name.split(".")

    if len(domain_name) < 2:
        raise ValueError(
            'single label {}s are not supported'.format(entity))

    # apply DNS name validator to every name part
    for label in domain_name:
        validate_dns_label(label, allow_underscore, allow_slash)
