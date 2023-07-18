#!/usr/bin/env python3
# coding: utf-8

import uuid
from grpc_module import api_pb2_grpc, api_pb2
import grpc
from concurrent import futures
from utils import *
from status import *
import json


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


class ExecService(api_pb2_grpc.ExecServiceServicer, Logger):
    def __init__(self):
        Logger.__init__(self)

    def Exec(self, request, context):
        #print("exec_cmd: {}".format(request))
        exec_id = request.exec_id
        cmd = ''.join(request.cmd)
        self._logger.info("exec_cmd: {}".format(cmd))
        try:
            se = ShellExecutor()
            ret = se._executor(cmd, request.timeout)
            response = api_pb2.ExecResponse()
            response.exec_id = exec_id
            response.stdout = ret['stdout']
            response.stderr = ret['stderr']
            response.exit_code = ret['retcode']
            #print(response.exit_code)
            #print(exec_id, cmd, timeout)
            #print(response)
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
        print(response.uniq_id)
        print(response.succeed)
        return response

    def GetInfo(self, request, context):
        self._logger.info("getinfo: {}".format(request))
        uniq_id = request.uniq_id
        print(uniq_id)
        local_uniq_id = read_uuid()
        print(local_uniq_id)
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

    def Send(self, request, context):
        self._logger.info("send: {}".format(request))


class BunnyGrpcServer(Logger):
    def __init__(self):
        Logger.__init__(self)

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        api_pb2_grpc.add_ExecServiceServicer_to_server(ExecService(), server)
        api_pb2_grpc.add_RegistrationServiceServicer_to_server(RegistrationService(), server)
        server.add_insecure_port('[::]:' + str(SERVER_CONFIG['agent']['agent_rpc_port']))
        self._logger.info('Starting bunny grpc server on port ' + str(SERVER_CONFIG['agent']['agent_rpc_port']))
        server.start()
        server.wait_for_termination()


bgs = BunnyGrpcServer()
bgs.serve()
