#!/usr/bin/env python3
# coding: utf-8
import sudo

from modules.grpc_module import api_pb2_grpc, api_pb2
import grpc
from concurrent import futures
from modules.utils import *
from modules.status import *
import math
import pwd
import grp


class HeartbeatService(api_pb2_grpc.HeartbeatServiceServicer, Logger):
    def __init__(self):
        Logger.__init__(self)

    def Heartbeat(self, request, context):
        self._logger.debug("heartbeat: {}".format(request))
        response = api_pb2.HeartbeatResponse()
        if request.ping == "ping":
            response.pong = "pong"
        else:
            response.pong = "pong pong pong"
        response.timestamp_millis = math.floor(datetime.datetime.now().timestamp() * 1000)
        response.machine_uniq_id = request.machine_uniq_id
        return response


class ExecService(api_pb2_grpc.ExecServiceServicer, Logger):
    def __init__(self):
        Logger.__init__(self)
        self.OutputType = (
            'STDOUT',
            'STDERR',
        )

    def Exec(self, request, context): # blocking executor
        #print("exec_cmd: {}".format(request))
        exec_id = request.exec_id
        #cmd = ''.join(request.cmd)
        cmd = request.cmd
        self._logger.info("exec_cmd: {}".format(cmd))
        try:
            se = ShellExecutor()
            ret = se._executor(cmd, request.timeout)

            curdt = curdatetime(formatter='%Y%m%d%H%M%S')
            output = '------STDOUT------\n'
            output += ret['stdout'].decode() + '\n\n'
            output += '------STDERR------\n'
            output += ret['stderr'].decode() + '\n\n'
            output += '------EXIT_CODE------\n'
            output += str(ret['retcode']) + '\n\n'
            outfile = LOGS_EXEC_DIR + 'execid_' + str(request.exec_id) + '_' + curdt + '.log'
            with open(outfile, 'w') as f:
                f.write(output)
                f.close()
            #print(response.exit_code)
            #print(exec_id, cmd, timeout)
            self._logger.debug("stdout: " + ret['stdout'].decode())
            self._logger.debug("stderr: " + ret['stderr'].decode())
            self._logger.debug("exit code: " + str(ret['retcode']))
            return api_pb2.ExecResponse(exec_id=exec_id, stdout=ret['stdout'], stderr=ret['stderr'], exit_code=ret['retcode'])
        except Exception as e:
            self._logger.fatal("exec_cmd: {}".format(cmd))
            self._logger.fatal(str(e))
            return api_pb2.ExecResponse(exec_id=exec_id, stdout=b'', stderr=b'Unknown Exception', exit_code=1)

    def StreamExec(self, request, context):
        exec_id = request.exec_id
        cmd = request.cmd
        timeout = request.timeout
        self._logger.debug("exec_cmd: {}".format(cmd))
        self._logger.debug("exec_id: {}".format(exec_id))
        try:
            se = ShellExecutor()
            ret, curdt = se._executor_blocking(cmd, timeout, exec_id)

            with open(LOGS_EXEC_DIR + 'execid_' + str(request.exec_id) + '_' + curdt + '.out', 'r') as out_file:
                while True:
                    line = out_file.readline()
                    if not line:
                        yield api_pb2.ExecStreamResponse(exec_id=exec_id, type=self.OutputType[0], output=line.encode(),
                                                         continued=False, exit_code=ret)
                        break
                    else:
                        yield api_pb2.ExecStreamResponse(exec_id=exec_id, type=self.OutputType[0], output=line.encode(),
                                                         continued=True, exit_code=ret)
            with open(LOGS_EXEC_DIR + 'execid_' + str(request.exec_id) + '_' + curdt + '.err', 'r') as err_file:
                while True:
                    line = err_file.readline()
                    if not line:
                        yield api_pb2.ExecStreamResponse(exec_id=exec_id, type=self.OutputType[1], output=line.encode(),
                                                         continued=False, exit_code=ret)
                        break
                    else:
                        yield api_pb2.ExecStreamResponse(exec_id=exec_id, type=self.OutputType[1], output=line.encode(),
                                                         continued=True, exit_code=ret)
        except Exception as e:
            self._logger.fatal("exec_cmd: {}".format(cmd))
            self._logger.fatal(str(e))




"""
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
"""


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
        self._logger.debug("send: File send service incoming")
        # oct() will return a string type, so use eval() to convert it to int
        access_modes = int(request.access_modes, base=8)
        try:
            uid = pwd.getpwnam(request.owner).pw_uid
        except KeyError as e:
            self._logger.fatal(e)
            self._return_code = self.CODE[4]
            return api_pb2.FileResponse(id=request.id, status=self._return_code, message='Unknown user ' + request.owner)
        try:
            gid = grp.getgrnam(request.group).gr_gid
        except KeyError as e:
            gid = pwd.getpwnam(request.owner).pw_gid
            self._logger.warn(e)
            self._logger.warn('Unknown group ' + request.group + ' use user group instead')
            # self._logger.fatal(e)
            # self._return_code = self.CODE[4]
            # return api_pb2.FileResponse(id=request.id, status=self._return_code, message='Unknown group ' + request.group)

        final_user = request.owner
        final_group = grp.getgrgid(gid).gr_name

        if request.path[-1] == '/':
            full_filename = request.path + request.filename
        else:
            full_filename = request.path + '/' + request.filename
        self._logger.debug("send: file_id: {}, file_name: {}, dest_path: {}, checksum: {}, access_modes: {}, owner: {}, format: {}".format(
            request.id, full_filename, request.path, request.checksum, access_modes, request.owner, request.format))

        tmp_filename = TMP_DIR + request.filename

        if not os.path.exists(request.path):
            self._return_code = self.CODE[1]
            self._logger.warn("send: {}".format(self._return_code))
            try:
                if sudo.run_as_sudo('root', 'mkdir -p ' + request.path).returncode != 0:
                    self._return_code = self.CODE[3]
                    self._logger.error('Write not allowed')
                    return api_pb2.FileResponse(id=request.id, status=self._return_code, message='Write not allowed')
                self._logger.debug("send: create directory: {}".format(request.path))
                self._logger.debug("send: write tmp file: {}".format(tmp_filename))
                with open(tmp_filename, 'wb') as f:
                    f.write(request.content)
                f.close()
                checksum_local = file_hash_md5(tmp_filename)
                self._logger.debug("send: local file md5 checksum: {}".format(checksum_local))
                self._logger.debug("send: remote file md5 checksum: {}".format(request.checksum))
                if checksum_local != request.checksum:
                    self._return_code = self.CODE[2]
                    self._logger.error('File checksum not equally')
                    return api_pb2.FileResponse(id=request.id, status=self._return_code, message='File checksum error')

                self._logger.debug("send: change file mode: {}".format(request.access_modes))
                sudo.run_as_sudo('root', 'chmod ' + str(request.access_modes) + ' ' + tmp_filename)

                self._logger.debug("send: change file owner to: {}, {}".format(request.owner, request.group))
                sudo.run_as_sudo('root', 'chown ' + final_user + ':' + final_group + ' ' + tmp_filename)

                self._return_code = self.CODE[0]
                self._logger.info('File checksum equally, file receive succeed')
                sudo.run_as_sudo('root', 'rm -f ' + full_filename)
                sudo.run_as_sudo('root', 'mv ' + tmp_filename + ' ' + full_filename)

                return api_pb2.FileResponse(id=request.id, status=self._return_code, message='File received successfully')
            except Exception as e:
                self._logger.fatal(e)
                self._return_code = self.CODE[3]
                return api_pb2.FileResponse(id=request.id, status=self._return_code, message='Write not allowed')
        else:
            try:
                self._logger.debug("send: write tmp file: {}".format(tmp_filename))
                with open(tmp_filename, 'wb') as f:
                    f.write(request.content)
                f.close()
                checksum_local = file_hash_md5(tmp_filename)
                self._logger.debug("send: local file md5 checksum: {}".format(checksum_local))
                self._logger.debug("send: remote file md5 checksum: {}".format(request.checksum))
                if checksum_local != request.checksum:
                    self._return_code = self.CODE[2]
                    self._logger.error('File checksum not equally')
                    return api_pb2.FileResponse(id=request.id, status=self._return_code, message='File checksum error')

                self._logger.debug("send: change file mode: {}".format(access_modes))
                sudo.run_as_sudo('root', 'chmod ' + str(access_modes) + ' ' + tmp_filename)

                self._logger.debug("send: change file owner to: {}, {}".format(request.owner, request.group))
                sudo.run_as_sudo('root', 'chown ' + request.owner + ':' + request.group + ' ' + tmp_filename)

                self._return_code = self.CODE[0]
                self._logger.info('File checksum equally, file receive succeed')
                sudo.run_as_sudo('root', 'rm -f ' + full_filename)
                sudo.run_as_sudo('root', 'mv ' + tmp_filename + ' ' + full_filename)

                return api_pb2.FileResponse(id=request.id, status=self._return_code, message='File received successfully')
            except Exception as e:
                self._logger.fatal(e)
                self._return_code = self.CODE[3]
                return api_pb2.FileResponse(id=request.id, status=self._return_code, message='Unknown exception')

    """
    def Send(self, request, context):
        self._logger.debug("send: File send service incoming")
        # oct() will return a string type, so use eval() to convert it to int
        access_modes = eval(oct(int(request.access_modes, base=8)))
        try:
            uid = pwd.getpwnam(request.owner).pw_uid
        except KeyError as e:
            self._logger.fatal(e)
            self._return_code = self.CODE[4]
            return api_pb2.FileResponse(id=request.id, status=self._return_code, message='Unknown user ' + request.owner)
        try:
            gid = grp.getgrnam(request.group).gr_gid
        except KeyError as e:
            gid = pwd.getpwnam(request.owner).pw_gid
            # self._logger.fatal(e)
            # self._return_code = self.CODE[4]
            # return api_pb2.FileResponse(id=request.id, status=self._return_code, message='Unknown group ' + request.group)

        if request.path[-1] == '/':
            full_filename = request.path + request.filename
        else:
            full_filename = request.path + '/' + request.filename

        self._logger.debug("send: file_id: {}, file_name: {}, dest_path: {}, checksum: {}, access_modes: {}, owner: {}, format: {}".format(
            request.id, full_filename, request.path, request.checksum, access_modes, request.owner, request.format))
        if not os.path.exists(request.path):
            self._return_code = self.CODE[1]
            self._logger.warn("send: {}".format(self._return_code))
            try:
                os.mkdir(request.path, 0o755)
                self._logger.debug("send: create directory: {}".format(request.path))
            except OSError as e:
                self._logger.fatal(e)
                self._return_code = self.CODE[3]
                return api_pb2.FileResponse(id=request.id, status=self._return_code, message='Write not allowed')
        else:
            try:
                self._logger.debug("send: write file: {}".format(full_filename))
                with open(full_filename, 'wb') as f:
                    f.write(request.content)
                f.close()
                self._logger.debug("send: change file mode: {}".format(access_modes))
                os.chmod(full_filename, access_modes)
                self._logger.debug("send: change file owner to: {}, {}".format(request.owner, request.group))
                os.chown(full_filename, uid, gid)
                checksum_local = file_hash_md5(full_filename)
                self._logger.debug("send: local file md5 checksum: {}".format(checksum_local))
                self._logger.debug("send: remote file md5 checksum: {}".format(request.checksum))
                if checksum_local != request.checksum:
                    self._return_code = self.CODE[2]
                    self._logger.error('File checksum not equally')
                    return api_pb2.FileResponse(id=request.id, status=self._return_code, message='File checksum error')
                else:
                    self._return_code = self.CODE[0]
                    self._logger.info('File checksum equally, file receive succeed')
                    return api_pb2.FileResponse(id=request.id, status=self._return_code, message='File received successfully')
            except OSError as e:
                self._logger.fatal(e)
                self._return_code = self.CODE[3]
                return api_pb2.FileResponse(id=request.id, status=self._return_code, message='Unknown exception')
    """

    """
    def StreamSend(self, request_iterator, context):
        self._logger.info("stream_send: {}".format(request_iterator))

        for request in request_iterator:
            if request.header:
                self._logger.fatal('Received file header: {}'. format(request.header))
                self._logger.fatal('Received file id: {}'.format(request.header.id))
                self._logger.fatal('Received file name: {}'.format(request.header.filename))
            elif request.chunk:
                yield api_pb2.FileResponse(id=request.header.id, status=api_pb2.FileResponse.OK, message='File received successfully')
        return
    """


class BunnyGrpcServer(Logger):
    def __init__(self):
        Logger.__init__(self)

    def serve(self):
        try:
            MAX_MESSAGE_LENGTH = 1024 * 1024 * 1024
            options = [
                ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)
            ]
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), maximum_concurrent_rpcs=10, options=options)
            api_pb2_grpc.add_ExecServiceServicer_to_server(ExecService(), server)
            self._logger.debug('Starting grpc Exec Service')
            #api_pb2_grpc.add_HeartbeatServiceServicer_to_server(HeartbeatService(), server)
            api_pb2_grpc.add_FileServiceServicer_to_server(FileService(), server)
            self._logger.debug('Starting grpc FileTransfer Service')
            #api_pb2_grpc.add_RegistrationServiceServicer_to_server(RegistrationService(), server)
            #api_pb2_grpc.add_FileServiceServicer_to_server(FileService(), server)
            server.add_insecure_port('[::]:' + str(SERVER_CONFIG['agent']['agent_rpc_port']))
            self._logger.info('Starting bunny grpc server on port ' + str(SERVER_CONFIG['agent']['agent_rpc_port']))
            server.start()
            self._logger.debug('bunny grpc server started')
            server.wait_for_termination()
        except Exception as e:
            self._logger.fatal(e)
            exit(1)


#bgs = BunnyGrpcServer()
#bgs.serve()
