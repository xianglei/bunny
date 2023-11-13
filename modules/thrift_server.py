#!/usr/bin/env python3
# coding: utf-8

import uuid
import binascii
import os
import hashlib
from .utils import *
from .status import *
import json
from pwd import getpwnam
from modules.thrift_module.api import *
from modules.thrift_module.api.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


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


def file_hash_md5(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def file_hash_sha1(filename):
    md5 = hashlib.sha1()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def file_crc32(filename):
    crc32 = 0
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            crc32 = binascii.crc32(data, crc32)
    return crc32 & 0xffffffff


class ExecServiceHandler(Logger):
    def __init__(self):
        Logger.__init__(self)

    def __exec_command(self, request):
        exec_id = request.exec_id
        cmd = request.cmd
        timeout = request.timeout
        print(exec_id, cmd, timeout)
        resp = ExecResponse(exec_id, b'stdout', b'stderr', 0)
        return resp

    def Exec(self, request):
        resp = self.__exec_command(request)
        return resp


handler = ExecServiceHandler()
processor = ExecService.Processor(handler)
transport = TSocket.TServerSocket(host='localhost', port=9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
server.setNumThreads(10)
server.serve()




