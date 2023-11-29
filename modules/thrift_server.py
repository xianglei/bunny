#!/usr/bin/env python3
# coding: utf-8

import uuid
import binascii
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
from thrift.TMultiplexedProcessor import TMultiplexedProcessor


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
        self._logger.info("exec_cmd: {}, timeout: {}, exec_id: {}".format(cmd, timeout, exec_id))
        try:
            se = ShellExecutor()
            ret = se._executor(cmd, timeout)
            curdt = curdatetime(formatter='%Y%m%d%H%M%S')
            output = '------STDOUT------\n'
            output += ret['stdout'].decode() + '\n\n'
            output += '------STDERR------\n'
            output += ret['stderr'].decode() + '\n\n'
            output += '------EXIT_CODE------\n'
            output += str(ret['retcode']) + '\n\n'
            output += '------EXEC_ID------\n'
            output += str(exec_id) + '\n\n'
            outfile = LOGS_DIR + 'execid_' + str(request.exec_id) + '_' + curdt + '.log'
            with open(outfile, 'w') as f:
                f.write(output)
                f.close()
            self._logger.info("stdout: " + ret['stdout'].decode())
            self._logger.info("stderr: " + ret['stderr'].decode())
            self._logger.info("exit code: " + str(ret['retcode']))
            resp = ExecResponse(exec_id, ret['stdout'], ret['stderr'], ret['retcode'])
        except Exception as e:
            self._logger.fatal(str(e))
            resp = ExecResponse(exec_id, b'', b'ExecutionError', 255)
        return resp

    def Exec(self, request):
        resp = self.__exec_command(request)
        return resp


class FileServiceHandler(Logger):
    def __init__(self):
        Logger.__init__(self)
        self.CODE = [
            'OK', 'DIR_NOT_EXISTS', 'CONTENT_CHECKSUM_ERROR', 'WRITE_NOT_ALLOWED', 'UNKNOWN_ERROR'
        ]
        self.FILE_FORMAT = {
            "JSON": 0,
            "INI": 1,
            "XML": 2,
            "YAML": 3,
            "BASH": 4,
        }
        self._return_code = None

    def Send(self, request):
        file_id = request.id
        file_name = request.filename
        dest_path = request.path
        checksum = request.checksum
        content = request.content
        access_mode = eval(oct(int(request.access_modes, base=8)))
        owner = request.owner
        user = getpwnam(owner)
        uid = user.pw_uid
        gid = user.pw_gid
        group = request.group
        file_format = request.format
        self._logger.info("id: {}, filename: {}, path: {}, checksum: {}, "
                          "access_mode: {}, owner: {}, group: {}, format: {}".
                          format(file_id, file_name, dest_path, checksum,
                                 access_mode, owner, group, file_format))

        if dest_path[-1] == '/':
            full_filename = dest_path + file_name
        else:
            full_filename = dest_path + '/' + file_name

        if not os.path.exists(dest_path):
            self._return_code = 1
            self._logger.fatal("send: {}".format(self._return_code))
            try:
                os.mkdir(dest_path, 0o755)
            except OSError as e:
                self._logger.fatal(e)
                self._return_code = 4
        try:
            with open(full_filename, 'wb') as f:
                f.write(content)
                f.close()
            os.chmod(full_filename, access_mode)
            os.chown(full_filename, uid, gid)
            checksum_local = file_hash_md5(full_filename)
            print(checksum_local)
            self._logger.warn(checksum_local)
            self._logger.warn(checksum)
            if checksum_local != checksum:
                self._return_code = 2
                self._logger.fatal('File checksum not equally')
            else:
                self._return_code = 0
                self._logger.info('File checksum equally, file receive succeed')
        except OSError as e:
            self._logger.fatal(e)
            self._return_code = 3
        #print(self._return_code)
        resp = FileResponse(id=file_id, status=self._return_code, message=str(self.CODE[self._return_code]))
        return resp


class RegistrationServiceHandler(Logger):
    def __init__(self):
        Logger.__init__(self)

    def Register(self, request):
        self._logger.info("register: {}".format(request))
        uniq_id = uuid.uuid4()
        succeed = True
        response = RegisterResponse()
        response.uniq_id = str(uniq_id)
        response.succeed = succeed
        return response

    def GetInfo(self, request):
        self._logger.info("info_request: {}".format(request))
        uniq_id = request.uniq_id
        local_uniq_id = read_uuid()
        print(uniq_id, local_uniq_id)
        response = InfoResponse()
        if uniq_id == local_uniq_id:
            #payload = retrieve_info()
            payload = {'a': 1, 'b': 2}
            response.payload = json.dumps(payload, indent=4, sort_keys=True)
            response.uuid = uniq_id
            return response
        else:
            self._logger.fatal("Local uniq_id is not equal to server uniq_id")
            return None


class BunnyThriftServer(Logger):
    def serve(self):
        exec_handler = ExecServiceHandler()
        exec_processor = ExecService.Processor(exec_handler)
        file_handler = FileServiceHandler()
        file_processor = FileService.Processor(file_handler)
        register_handler = RegistrationServiceHandler()
        register_processor = RegistrationService.Processor(register_handler)

        transport = TSocket.TServerSocket(host=SERVER_CONFIG['agent']['bind'], port=SERVER_CONFIG['agent']['agent_rpc_port'])
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        processor = TMultiplexedProcessor()
        processor.registerProcessor('ExecService', exec_processor)
        processor.registerProcessor('FileService', file_processor)
        processor.registerProcessor('RegistrationService', register_processor)

        server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
        server.setNumThreads(10)
        self._logger.info('Starting bunny thrift server on port ' + str(SERVER_CONFIG['agent']['agent_rpc_port']))
        server.serve()





