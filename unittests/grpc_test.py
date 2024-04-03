import unittest
import grpc

from modules.grpc_module import api_pb2_grpc, api_pb2


class GrpcFileSendTest(unittest.TestCase):
    def test_send_file(self):
        channel = grpc.insecure_channel('localhost:7182')
        stub = api_pb2_grpc.FileServiceStub(channel)
        with open('../test.txt', 'rb') as f:
            data = f.read()
            f.close()
        request = api_pb2.FileRequest(id='1', filename='../test.txt', path='/tmp/', checksum='d577273ff885c3f84dadb8578bb41399',
                                      content=data, access_modes='644', owner='xianglei', group='wheel', format='BASH')
        response = stub.Send(request)
        print(response.status)
        print(response.message)
        self.assertEqual(response.id, '1')
        self.assertEqual(response.status, 0)


class GrpcExecTest(unittest.TestCase):
    def test_exec(self):
        channel = grpc.insecure_channel('localhost:7182')
        stub = api_pb2_grpc.ExecServiceStub(channel)
        request = api_pb2.ExecRequest(exec_id='1', cmd='ls /tmp', timeout=120)
        response = stub.Exec(request)
        self.assertEqual(response.exec_id, '1')
        self.assertEqual(response.exit_code, 0)


if __name__ == '__main__':
    unittest.main()
