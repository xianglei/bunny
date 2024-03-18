#!/usr/lib/exadoop/python/bin/python
# coding: utf-8
# author: xianglei

import hashlib
from modules.config_parser import *
import string
import logging
import logzero
from logzero import logger, loglevel, logfile
import datetime
import time
import subprocess
import socket
import base64
import os
from Crypto.Cipher import AES, DES3
from Crypto import Random
from Crypto.Hash import MD5, SHA, SHA224, SHA256, SHA384, SHA512, HMAC
from Crypto.PublicKey import RSA
from fabric import Connection, SerialGroup
import shlex
import subprocess2
import binascii
import pickle


class UnitFormat:
    def __init__(self):
        self.byte_factor = 1
        self.bit_factor = 1

    def byte_formatter(self, number, precision=2):
        byte = self.byte_factor
        kb = byte * 1024
        mb = kb * 1024
        gb = mb * 1024
        tb = gb * 1024
        pb = tb * 1024
        eb = pb * 1024
        zb = eb * 1024
        yb = zb * 1024
        bb = yb * 1024
        number = int(number)
        if number >= bb:
            number = str(round(number/bb, precision)) + 'BB'
        elif number >= yb:
            number = str(round(number/yb, precision)) + 'YB'
        elif number >= zb:
            number = str(round(number/zb, precision)) + 'ZB'
        elif number >= eb:
            number = str(round(number/eb, precision)) + 'EB'
        elif number >= pb:
            number = str(round(number/pb, precision)) + 'PB'
        elif number >= tb:
            number = str(round(number/tb, precision)) + 'TB'
        elif number >= gb:
            number = str(round(number/gb, precision)) + 'GB'
        elif number >= mb:
            number = str(round(number/mb, precision)) + 'MB'
        elif number >= kb:
            number = str(round(number/kb, precision)) + 'KB'
        else:
            number = str(round(number, precision)) + 'Byte'
        return number

    def bit_formatter(self, number, precision=2):
        bit = self.bit_factor
        kb = bit * 1000
        mb = kb * 1000
        gb = mb * 1000
        tb = gb * 1000
        pb = tb * 1000
        eb = pb * 1000
        zb = eb * 1000
        yb = zb * 1000
        bb = yb * 1000
        number = int(number)
        if number >= bb:
            number = str(round(number/bb, precision)) + 'Bb'
        elif number >= yb:
            number = str(round(number/yb, precision)) + 'Yb'
        elif number >= zb:
            number = str(round(number/zb, precision)) + 'Zb'
        elif number >= eb:
            number = str(round(number/eb, precision)) + 'Eb'
        elif number >= pb:
            number = str(round(number/pb, precision)) + 'Pb'
        elif number >= tb:
            number = str(round(number/tb, precision)) + 'Tb'
        elif number >= gb:
            number = str(round(number/gb, precision)) + 'Gb'
        elif number >= mb:
            number = str(round(number/mb, precision)) + 'Mb'
        elif number >= kb:
            number = str(round(number/kb, precision)) + 'Kb'
        else:
            number = str(round(number, precision)) + 'Bits'
        return number

    def bit_2_byte(self, bit):
        byte = self.byte_formatter(round(int(bit)/8))
        return byte

    def byte_2_bit(self, byte):
        bit = self.bit_formatter(round(int(byte)*8))
        return bit


class switch(object):
    """
    switch case in python
    for case in switch(variable):
        case('a'):
            do something
            break
        case('b'):
            do something
            break
        case():
            do default
    """
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


class IsText:
    def __init__(self):
        self.text = "".join(map(chr, range(32, 127))) + "\n\r\t\b"
        self._null_trans = string.maketrans("", "")
        self.threshold = 0.30

    def istext(self, s):
        _null_trans = self._null_trans
        text = self.text
        threshold = self.threshold
        if '\0' in s:
            return False
        if not s:
            return True
        t = string.translate(s, _null_trans, text)
        return len(t)/(len(s) * 1.0) <= threshold


class Logger():
    def __init__(self):
        if SERVER_CONFIG['agent']['log_level'] == "INFO":
            loglevel(logging.INFO)
        elif SERVER_CONFIG['agent']['log_level'] == "DEBUG":
            loglevel(logging.DEBUG)
        elif SERVER_CONFIG['agent']['log_level'] == "WARNING":
            loglevel(logging.WARNING)
        elif SERVER_CONFIG['agent']['log_level'] == "ERROR":
            loglevel(logging.ERROR)
        elif SERVER_CONFIG['agent']['log_level'] == "CRITICAL":
            loglevel(logging.CRITICAL)
        else:
            loglevel(logging.DEBUG)
        format = logging.Formatter('%(asctime)s %(levelname)s %(filename)s: %(funcName)s: [line:%(lineno)d]'
                                   ' - %(message)s')
        logzero.formatter(format)
        logfile(LOGS_DIR + SERVER_CONFIG['agent']['log_file'],
                maxBytes=SERVER_CONFIG['agent']['log_file_max_size'],
                backupCount=SERVER_CONFIG['agent']['log_file_backup_count'])
        self._logger = logger

    def logger(self):
        return self._logger


class SSH(Logger):
    def __init__(self, ip, port, username, password, timeout=30):
        Logger.__init__(self)
        self._ip = ip
        self._port = port
        self._username = username
        self._password = password
        self._timeout = timeout

    def connect(self):
        self._logger.info('Connecting to %s:%s as %s' % (self._ip, self._port, self._username,))
        try:
            conn = Connection(self._ip, port=self._port, user=self._username,
                              connect_kwargs={'password': self._password},
                              connect_timeout=self._timeout)
        except Exception as e:
            self._logger.error(e)
            conn = None
        return conn

    def group_connect(self, hosts):
        self._logger.info('Connecting to %s as %s' % (hosts, self._username,))
        try:
            conn = SerialGroup(*hosts, user=self._username,connect_kwargs={'password': self._password},
                               connect_timeout=self._timeout)
        except Exception as e:
            self._logger.error(e)
            conn = None
        return conn

    def test_connection(self):
        conn = self.connect()
        if conn:
            try:
                ret = conn.sudo('hostname')
                self._logger.info(ret.stdout.strip())
                return True
            except Exception as e:
                self._logger.error(e)
                return False
        else:
            return False


class ShellExecutor(Logger):
    def __init__(self):
        Logger.__init__(self)

    def _executor(self, cmd, timeout):
        """
        阻塞执行命令, 并将执行结果写入exec_id_id_date.log文件
        :param cmd: string
        :param exec_id: string
        :param timeout: int
        :return: exec_id in string, stdout and stderr in bytes, exit_code in int
        """
        try:
            self._logger.info('Executing shell command %s' % cmd)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=False,
                                 shell=True, preexec_fn=os.setsid, env=os.environ.copy(), bufsize=0)
            stdout, stderr = p.communicate(timeout=timeout)
            retcode = p.wait()
            if not os.path.exists(LOGS_EXEC_DIR):
                try:
                    os.mkdir(LOGS_EXEC_DIR, mode=0o777)
                except OSError as e:
                    self._logger.error(e)
            self._logger.info('Shell command execution result: retcode %s, stdout %s, stderr %s' %
                              (retcode, stdout, stderr,))
            return {'retcode': retcode, 'stdout': stdout, 'stderr': stderr, 'cmd': cmd}
        except IOError as e:
            self._logger.error(e)
            return e

    def _executor_blocking(self, cmd, timeout, exec_id):
        """
        阻塞执行命令, 并将执行结果写入exec_id_id_date.log文件
        :param cmd: string
        :param exec_id: string
        :param timeout: int
        :return: exec_id in string, stdout and stderr in bytes, exit_code in int
        """
        try:
            self._logger.info('Executing shell command %s' % cmd)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=False,
                                 shell=True, preexec_fn=os.setsid, env=os.environ.copy(), bufsize=0)
            stdout, stderr = p.communicate(timeout=timeout)
            retcode = p.wait()
            curdt = curdatetime(formatter='%Y%m%d%H%M%S')
            if not os.path.exists(LOGS_EXEC_DIR):
                try:
                    os.mkdir(LOGS_EXEC_DIR, mode=0o777)
                except OSError as e:
                    self._logger.error(e)
            self._logger.info('Shell command execution result: retcode %s, stdout %s, stderr %s' %
                              (retcode, stdout, stderr,))
            try:
                with open(LOGS_EXEC_DIR + 'execid_' + str(exec_id) + '_' + curdt + '.out', 'w') as out_file:
                    out_file.write(stdout.decode())
                with open(LOGS_EXEC_DIR + 'execid_' + str(exec_id) + '_' + curdt + '.err', 'w') as err_file:
                    err_file.write(stderr.decode())
            except IOError as e:
                self._logger.error(e)
            finally:
                out_file.close()
                err_file.close()
            return retcode, curdt
        except IOError as e:
            self._logger.error(e)
            return e

    def _executor_non_blocking(self, cmd, exec_id):
        """
        非阻塞执行命令, 并将执行结果以stream方式写入exec_id_id_date.out和.err文件
        :param cmd:
        :param exec_id:
        :return: exec_id in string, stdout and stderr in bytes, exit_code in int
        """
        try:
            self._logger.info('Executing shell command %s' % cmd)
            p = subprocess2.Popen(shlex.split(cmd), stdout=subprocess2.PIPE, stderr=subprocess2.PIPE, close_fds=False,
            preexec_fn=os.setsid, env=os.environ.copy())
            p.runInBackground()
            curdt = curdatetime(formatter='%Y%m%d%H%M%S')
            if not os.path.exists(LOGS_EXEC_DIR):
                try:
                    os.mkdir(LOGS_EXEC_DIR, mode=0o777)
                except OSError as e:
                    self._logger.error(e)
            out_file = open(LOGS_EXEC_DIR + 'execid_' + str(exec_id) + '_' + curdt + '.out', 'w')
            err_file = open(LOGS_EXEC_DIR + 'execid_' + str(exec_id) + '_' + curdt + '.err', 'w')
            while True:
                stdout = p.stdout.readline()
                stderr = p.stderr.readline()
                if stdout:
                    out_file.write(stdout.strip().decode() + '\n')
                if stderr:
                    err_file.write(stderr.strip().decode() + '\n')
                if p.returncode is not None:
                    retcode = p.returncode
                    break
            out_file.close()
            err_file.close()
            return retcode, curdt

        except IOError as e:
            self._logger.error(e)
            return e


class Crypto(Logger):
    """
    A simple crypto class with calc mysql PASSWORD()-ed password and a simple encrypt decrypt method by using bit offset
    """
    def __init__(self):
        Logger.__init__(self)
        self.BLOCK_SIZE = 32
        self.key = hashlib.sha256(SERVER_CONFIG['server']['secret'].encode()).digest()

    def _pad(self, s):
        return s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * \
            chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    def _generate_rsa_keypair(self):
        keypair = RSA.generate(2048, e=65537)
        public_rsa_key = keypair.publickey().exportKey('PEM')
        private_rsa_key = keypair.exportKey('PEM')
        return public_rsa_key, private_rsa_key

    def _get_rsa_keys(self):
        pub_file = SERVER_CONFIG + 'conf/rsa.pub'
        priv_file = SERVER_CONFIG + 'conf/rsa'
        if not os.path.exists(pub_file) or not os.path.exists(priv_file):
            try:
                os.remove(pub_file)
                os.remove(priv_file)
            except OSError as e:
                print('Remove standalone key file')
            public, private = self._generate_rsa_keypair()
            with open(pub_file, 'wb') as pub:
                pub.write(public)
            pub.close()
            with open(priv_file, 'wb') as priv:
                priv.write(private)
            priv.close()
        else:
            with open(pub_file, 'rb') as pub:
                public = pub.read()
            pub.close()
            with open(priv_file, 'rb') as priv:
                private = priv.read()
            priv.close()

        return {'public_key': public, 'private_key': private}

    def encrypt_aes(self, s, mode=AES.MODE_CBC):
        s = self._pad(s)
        iv = Random.new().read(AES.block_size)
        self._logger.debug('AES iv encrypt and the length is %d' % (len(iv),))
        cipher = AES.new(self.key, mode, iv)
        return base64.b64encode(iv + cipher.encrypt(s))

    def decrypt_aes(self, s, mode=AES.MODE_CBC):
        s = base64.b64decode(s)
        iv = s[:AES.block_size]
        self._logger.debug('AES iv decrypt and the length is %d' % (len(iv),))
        cipher = AES.new(self.key, mode, iv)
        return self._unpad(cipher.decrypt(s[AES.block_size:])).decode('utf-8')

    def encrypt_des3(self, s, mode=DES3.MODE_CBC):
        s = self._pad(s)
        iv = Random.new().read(DES3.block_size)
        self._logger.debug('DES3 encrypt and the length is %d' % (len(iv),))
        cipher = DES3.new(self.key[16:], mode, iv)
        return base64.b64encode(iv + cipher.encrypt(s))

    def decrypt_des3(self, s, mode=DES3.MODE_CBC):
        s = base64.b64decode(s)
        iv = s[:DES3.block_size]
        self._logger.debug('DES3 decrypt and the length is %d' % (len(iv),))
        cipher = DES3.new(self.key[16:], mode, iv)
        return self._unpad(cipher.decrypt(s[DES3.block_size:])).decode('utf-8')

    @staticmethod
    def cacl_mysql_passwd(passwd):
        password = '*' + hashlib.sha1(hashlib.sha1(passwd).digest()).hexdigest().upper()
        return password

    @staticmethod
    def encrypt_shift(s):
        key = 16
        b = bytearray(str(s).encode("utf-8"))
        n = len(b)
        c = bytearray(n*2)
        j = 0
        for i in range(0, n):
            b1 = b[i]
            b2 = b1 ^ key    # b1 = b2^ key
            c1 = b2 % 16
            c2 = b2 // 16    # b2 = c2*16 + c1
            c1 = c1 + 65
            c2 = c2 + 65
            c[j] = c1
            c[j + 1] = c2
            j = j + 2
        return c.decode("utf-8").lower()

    @staticmethod
    def decrypt_shift(s):
        key = 16
        c = bytearray(str(s).encode("utf-8").upper())
        n = len(c)
        if n % 2 != 0:
            return ""
        n = n // 2
        b = bytearray(n)
        j = 0
        for i in range(0, n):
            c1 = c[j]
            c2 = c[j + 1]
            j = j + 2
            c1 = c1 - 65
            c2 = c2 - 65
            b2 = c2 * 16 + c1
            b1 = b2 ^ key
            b[i] = b1
        try:
            return b.decode("utf-8")
        except Exception as e:
            return "failed: " + str(e)

    def hmac(self, s, upper=False):
        salt = SERVER_CONFIG['server']['secret']
        hmac = HMAC.new(salt)
        hmac.update(s)
        if upper is False:
            return hmac.hexdigest()
        else:
            return hmac.hexdigest().upper()

    def md5(self, s, upper=False):
        salt = SERVER_CONFIG['server']['secret']
        md5 = MD5.new(salt)
        md5.update(s)
        if upper is False:
            return md5.hexdigest()
        else:
            return md5.hexdigest().upper()

    def sha1(self, s, upper=False):
        salt = SERVER_CONFIG['server']['secret']
        sha = SHA.new(salt)
        sha.update(s)
        if upper is False:
            return sha.hexdigest()
        else:
            return sha.hexdigest().upper()

    def sha224(self, s, upper=False):
        salt = SERVER_CONFIG['server']['secret']
        sha = SHA224.new(salt)
        sha.update(s)
        if upper is False:
            return sha.hexdigest()
        else:
            return sha.hexdigest().upper()

    def sha256(self, s, upper=False):
        salt = SERVER_CONFIG['server']['secret']
        sha = SHA256.new(salt)
        sha.update(s)
        if upper is False:
            return sha.hexdigest()
        else:
            return sha.hexdigest().upper()

    def sha384(self, s, upper=False):
        salt = SERVER_CONFIG['server']['secret']
        sha = SHA384.new(salt)
        sha.update(s)
        if upper is False:
            return sha.hexdigest()
        else:
            return sha.hexdigest().upper()

    def sha512(self, s, upper=False):
        salt = SERVER_CONFIG['server']['secret']
        sha = SHA512.new(salt)
        sha.update(s)
        if upper is False:
            return sha.hexdigest()
        else:
            return sha.hexdigest().upper()


def curdatetime(formatter='%Y-%m-%d %H:%M:%S'):
    """
    :param formatter: time format
    :return: formatted time ex: 2018-01-09 14:32:22
    """
    return datetime.datetime.now().strftime(formatter)


def unix_timestamp(dtstring=None):
    """
    :param dtstring: datetime in string
    :return: unix timestamp
    """
    if dtstring is None:
        dtstamp = datetime.datetime.now()
        ut = time.mktime(dtstamp.timetuple())
    else:
        timep = time.strptime('%Y-%m-%d %H:%M:%S')
        ut = int(time.mktime(timep))
    return ut


def timestamp_datetime(timestamp=None, formatter='%Y-%m-%d %H:%M:%S'):
    """
    :param timestamp: unix timestamp
    :param formatter: date time format string
    :return: formatted given time
    """
    if timestamp is None:
        timestamp = time.time()
        timep = time.localtime(int(timestamp))
        return time.strftime(formatter, timep)


def curtimestemp(precision=None):
    """
    :param precision: second or milli precision, default second
    :return: unix time stamp
    """
    for case in switch(precision):
        if case('second'):
            ts = int(time.time())
            break
        if case('milli'):
            ts = float(int(round(time.time() * 1000))/1000)
            break
        if case(None):
            ts = int(time.time())
            break
        if case():
            ts = int(time.time())
    return ts


def networktools_ip_hostname(nodename):
    """
    :param nodename: hostname or ipaddr
    :return: full qualified domain name and ip address
    """
    fqdn = socket.getfqdn(nodename)
    ip = socket.gethostbyname(fqdn)
    return fqdn, ip


def self_ip_hostname():
    """
    :return: full qualified domain name and ip address
    """
    fqdn = socket.getfqdn()
    ip = socket.gethostbyname(fqdn)
    return fqdn, ip


def file_crc32(filename):
    crc32 = 0
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            crc32 = binascii.crc32(data, crc32)
    return crc32 & 0xffffffff


def file_hash_sha1(filename):
    md5 = hashlib.sha1()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def file_hash_md5(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def read_uuid():
    if os.path.exists(RUN_DIR + 'bunny.uuid'):
        try:
            with open(RUN_DIR + 'bunny.uuid', 'r') as f:
                uid = f.read().strip()
                f.close()
        except Exception as e:
            print(e)
            uid = None
        return uid
    else:
        return None


def write_uuid(uid):
    try:
        with open(RUN_DIR + 'bunny.uuid', 'w') as f:
            f.write(uid)
            f.close()
    except Exception as e:
        print(e)


def check_process_exists(proc_keyword):
    import psutil
    for proc in psutil.process_iter(['name']):
        if proc_keyword.lower() in proc.info['name'].lower():
            return True, proc.pid
    return False, -1


def pack_string(s, fobj):
    #return binascii.hexlify(s.encode('utf-8'))
    return pickle.dump(s, fobj)


def unpack_binary(fobj):
    #return binascii.unhexlify(b).decode('utf-8')
    return pickle.load(fobj)


def get_bunny_user():
    import getpass
    return getpass.getuser()


def get_user_uid_gid(username):
    import pwd
    import grp
    try:
        user = pwd.getpwnam(username)
        group = grp.getgrgid(user.pw_gid)
        group_name = group.gr_name
        return user.pw_uid, user.pw_gid, group_name
    except KeyError as e:
        print(e)
        return None, None, None





