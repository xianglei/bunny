#!/usr/bin/env python3
# coding: utf-8

import grpc
import platform
from utils import *
from grpc_module import api_pb2_grpc, api_pb2

def exec():
    channel = grpc.insecure_channel(SERVER_CONFIG['server']['host'] + ':' +
                                    str(SERVER_CONFIG['server']['server_rpc_port']))
    stub = api_pb2_grpc.ExecServiceStub(channel)
    response = stub.Exec(api_pb2.ExecRequest(exec_id='1', cmd='ls -l', timeout=120))
    print("Exec cli exec_id " + response.exec_id)
    print("Exec cli stdout " + response.stdout)
    print("Exec cli stderr " + str(response.stderr))
    print("Exec cli exit_code" + str(response.exit_code))


def register():
    version = SERVER_CONFIG['agent']['version']
    hostname = platform.node()
    #print(version)
    ip = socket.gethostbyname(hostname)
    #print(ip)
    endpoint = ip
    if os.path.exists(BASE_DIR + 'bunny.uuid'):
        pass
    else:
        try:
            channel = grpc.insecure_channel(SERVER_CONFIG['server']['host'] + ':' +
                                            str(SERVER_CONFIG['server']['server_rpc_port']))
            stub = api_pb2_grpc.RegistrationServiceStub(channel)
            response = stub.Register(api_pb2.RegisterRequest(version=version, endpoint=endpoint))
            #print(response)
            uniq_id = response.uniq_id
            print(uniq_id)
            succeed = response.succeed
            print(succeed)
        except Exception as e:
            print(e)


def getinfo():
    channel = grpc.insecure_channel(SERVER_CONFIG['server']['host'] + ':' +
                                    str(SERVER_CONFIG['server']['server_rpc_port']))
    stub = api_pb2_grpc.RegistrationServiceStub(channel)
    response = stub.GetInfo(api_pb2.InfoRequest(uniq_id='1'))
    print("GetInfo cli uniq_id " + response.uniq_id)
    print("GetInfo cli payload " + response.payload)


def sendfile():
    channel = grpc.insecure_channel(SERVER_CONFIG['server']['host'] + ':' +
                                    str(SERVER_CONFIG['server']['server_rpc_port']))
    stub = api_pb2_grpc.FileServiceStub(channel)
    with open('test.txt', 'rb') as f:
        content = f.read()
        f.close()
    response = stub.Send(api_pb2.FileRequest(id='1', filename='test.txt',
                                             path='/tmp/', checksum='d8e8fca2dc0f896fd7cb4cb0031ba249',
                                             content=content, access_modes='644',
                                             owner='xianglei', group='wheel',
                                             format='BASH'))
    print("SendFile cli status " + str(response.status))
    print("SendFile cli message " + str(response.message))

sendfile()
