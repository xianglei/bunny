#!/usr/bin/env python3
# coding: utf-8

import uuid
from modules.grpc_module import api_pb2_grpc, api_pb2
import grpc
from concurrent import futures
from .utils import *
from .status import *
import json
from pwd import getpwnam
import hashlib
import binascii
import shutil


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


class ExecService(api_pb2_grpc.ExecServiceServicer, Logger):
    def __init__(self):
        Logger.__init__(self)

    def Exec(self, request, context):
        #print("exec_cmd: {}".format(request))
        exec_id = request.exec_id
        #cmd = ''.join(request.cmd)
        cmd = request.cmd
        self._logger.info("exec_cmd: {}".format(cmd))
        try:
            se = ShellExecutor()
            ret = se._executor(cmd, request.timeout)
            response = api_pb2.ExecResponse()
            response.exec_id = exec_id
            response.stdout = ret['stdout']
            response.stderr = ret['stderr']
            response.exit_code = ret['retcode']


            curdt = curdatetime(formatter='%Y%m%d%H%M%S')
            output = '------STDOUT------\n'
            output += ret['stdout'].decode() + '\n\n'
            output += '------STDERR------\n'
            output += ret['stderr'].decode() + '\n\n'
            output += '------EXIT_CODE------\n'
            output += str(ret['retcode']) + '\n\n'
            outfile = LOGS_DIR + 'execid_' + str(request.exec_id) + '_' + curdt + '.log'
            with open(outfile, 'w') as f:
                f.write(output)
                f.close()
            #print(response.exit_code)
            #print(exec_id, cmd, timeout)
            self._logger.info("stdout: " +response.stdout.decode())
            self._logger.info("stderr: " + response.stderr.decode())
            self._logger.info("exit code: " + response.exit_code)
            return response
        except:
            self._logger.fatal("exec_cmd: {}".format(cmd))


class RegistrationService(api_pb2_grpc.RegistrationServiceServicer, Logger):
    def __init__(self):
        Logger.__init__(self)

    def Register(self, request, context):
        self._logger.info("register: {}".format(request))
        uniq_id = uuid.uuid4()
        succeed = True
        #print(uniq_id, success)
        response = api_pb2.RegisterResponse()
        response.uniq_id = str(uniq_id)
        response.succeed = bool(succeed)
        #print(response.uniq_id)
        #print(response.succeed)
        return response

    def GetInfo(self, request, context):
        self._logger.info("getinfo: {}".format(request))
        uniq_id = request.uniq_id
        #print(uniq_id)
        local_uniq_id = read_uuid()
        #print(local_uniq_id)
        if uniq_id == local_uniq_id:
            response = api_pb2.InfoResponse()
            response.uniq_id = uniq_id
            '''
            In production, you should get the real info from the local machine
            '''
            response.payload = json.dumps({'a': 'b'}, indent=4, sort_keys=True)
            return response
        else:
            self._logger.fatal("Local uniq_id is not equal to server uniq_id")

    def register(self):
        version = SERVER_CONFIG['agent']['version']
        hostname = platform.node()
        ip = socket.gethostbyname(hostname)
        endpoint = ip
        if os.path.exists(RUN_DIR + 'bunny.uuid'):
            uid = read_uuid()
            self._logger.info("registered: {}".format(uid))
        else:
            try:
                channel = grpc.insecure_channel(SERVER_CONFIG['server']['host'] + ':' +
                                                str(SERVER_CONFIG['server']['server_rpc_port']))
                stub = api_pb2_grpc.RegistrationServiceStub(channel)
                response = stub.Register(api_pb2.RegistrationRequest(version=version, endpoint=endpoint))
                uniq_id = response.uniq_id
                succeed = response.succeed
                if succeed:
                    self._logger.info("register: {}".format(uuid))
                    write_uuid(uniq_id)
                else:
                    self._logger.fatal("register failed")
            except Exception as e:
                self._logger.fatal(e)


class FileService(api_pb2_grpc.FileServiceServicer, Logger):
    def __init__(self):
        Logger.__init__(self)
        """
        self.CODE = {
            "OK": 0,
            "DIR_NOT_EXISTS": 1,
            "CONTENT_CHECKSUM_ERROR": 2,
            "WRITE_NOT_ALLOWED": 3,
            "UNKNOWN_ERROR": 4,
        }
        """
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

    def Send(self, request, context):
        file_id = request.id
        file_name = request.filename
        dest_path = request.path
        checksum = request.checksum
        content = request.content
        # oct() will return a string type, so use eval() to convert it to int
        access_modes = eval(oct(int(request.access_modes, base=8)))
        owner = request.owner
        user = getpwnam(owner)
        uid = user.pw_uid
        gid = user.pw_gid
        # format is unused now
        format = request.format

        self._logger.info("send: {}".format(request))

        if dest_path[-1] == '/':
            full_filename = dest_path + file_name
        else:
            full_filename = dest_path + '/' + file_name

        if not os.path.exists(dest_path):
            self._return_code = self.CODE[1]
            self._logger.fatal("send: {}".format(self._return_code))
            try:
                os.mkdir(dest_path, 0o755)
            except OSError as e:
                self._logger.fatal(e)
                self._return_code = self.CODE[4]
        else:
            try:
                with open(full_filename, 'wb') as f:
                    f.write(content)
                    f.close()
                os.chmod(full_filename, access_modes)
                os.chown(full_filename, uid, gid)
                checksum_local = file_hash_md5(full_filename)
                self._logger.warn(checksum_local)
                self._logger.warn(checksum)
                if checksum_local != checksum:
                    self._return_code = self.CODE[2]
                    self._logger.fatal('File checksum not equally')
                else:
                    self._return_code = self.CODE[0]
                    self._logger.info('File checksum equally, file receive succeed')
            except OSError as e:
                self._logger.fatal(e)
                self._return_code = self.CODE[3]
        return api_pb2.FileResponse(status=self._return_code, message=self._return_code)


class BunnyGrpcServer(Logger):
    def __init__(self):
        Logger.__init__(self)

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        api_pb2_grpc.add_ExecServiceServicer_to_server(ExecService(), server)
        api_pb2_grpc.add_RegistrationServiceServicer_to_server(RegistrationService(), server)
        api_pb2_grpc.add_FileServiceServicer_to_server(FileService(), server)
        server.add_insecure_port('[::]:' + str(SERVER_CONFIG['agent']['agent_rpc_port']))
        self._logger.info('Starting bunny grpc server on port ' + str(SERVER_CONFIG['agent']['agent_rpc_port']))
        server.start()
        server.wait_for_termination()


#bgs = BunnyGrpcServer()
#bgs.serve()
