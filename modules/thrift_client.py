#!/usr/bin/env python3
# coding: utf-8

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from modules.thrift_module.api import *
from modules.thrift_module.api.ttypes import *

transport = TSocket.TSocket('localhost', 9090)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)

client = ExecService.Client(protocol)
transport.open()
exec = ExecService.ExecRequest('1', 'ls -l', 120)
res = client.Exec(exec)
print(res)
transport.close()
