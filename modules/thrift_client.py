#!/usr/bin/env python3
# coding: utf-8

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from modules.thrift_module.api import *
from modules.thrift_module.api.ttypes import *
from thrift.protocol import TMultiplexedProtocol

transport = TSocket.TSocket('localhost', 9090)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)

#client = ExecService.Client(protocol)
exec_protocol = TMultiplexedProtocol.TMultiplexedProtocol(protocol, 'ExecService')
file_protocol = TMultiplexedProtocol.TMultiplexedProtocol(protocol, 'FileService')
register_protocol = TMultiplexedProtocol.TMultiplexedProtocol(protocol, 'RegistrationService')

exec_client = ExecService.Client(exec_protocol)
file_client = FileService.Client(file_protocol)
register_client = RegistrationService.Client(register_protocol)

transport.open()
fileobj = FileService.FileRequest(id='1', filename='test', path='/tmp/test',
                                  checksum="e807f1fcf82d132f9bb018ca6738a19f", content='1234567890'.encode(),
                                  access_modes="755", owner='xianglei', group='xianglei', format=0)
print(fileobj)
res = file_client.Send(fileobj)
print(res)
#execobj = ExecService.ExecRequest(exec_id="1", cmd='ls -l', timeout=10)
#res = exec_client.Exec(execobj)
#print(res)

registerobj = RegistrationService.RegisterRequest(version='1.0.0', endpoint='10.0.1.1')
print(registerobj)
res = register_client.Register(registerobj)
print(res)

infoobj = RegistrationService.InfoRequest(uniq_id='1')
print(infoobj)
res = register_client.GetInfo(infoobj)
print(res.payload)
transport.close()
