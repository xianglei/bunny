#!/usr/bin/env python3
# coding: utf-8

import platform
import uuid
from grpc_module import api_pb2_grpc, api_pb2
import grpc
from concurrent import futures
from utils import *


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

    def register(self):
        version = SERVER_CONFIG['agent']['version']
        hostname = platform.node()
        ip = socket.gethostbyname(hostname)
        endpoint = ip
        if os.path.exists(BASE_DIR + 'bunny.uuid'):
            pass
        else:
            try:
                channel = grpc.insecure_channel(SERVER_CONFIG['server']['host'] + ':' +
                                                str(SERVER_CONFIG['server']['server_rpc_port']))
                stub = api_pb2_grpc.RegistrationServiceStub(channel)
                response = stub.Register(api_pb2.RegistrationRequest(version=version, endpoint=endpoint))
                uniq_id = response.uniq_id
                success = response.success
                if success:
                    self._logger.info("register: {}".format(uuid))
                with open(CONFIG_DIR + 'bunny.uuid', 'w') as f:
                    f.write(str(uniq_id))
            except Exception as e:
                self._logger.fatal(e)


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
