#!/usr/bin/env python3
# coding: utf-8

from modules.utils import *
from modules.status import *
from pwd import getpwnam
from modules.thrift_module.api import *
from modules.thrift_module.api.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.TMultiplexedProcessor import TMultiplexedProcessor


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

        # assemble the full path
        if dest_path[-1] == '/':
            full_filename = dest_path + file_name
        else:
            full_filename = dest_path + '/' + file_name

        # check if the dest path exists
        if not os.path.exists(dest_path):
            self._return_code = 1
            self._logger.warn("send: {}".format(self._return_code))
            try:
                os.mkdir(dest_path, 0o755)
            except OSError as e:
                self._logger.fatal(e)
                self._return_code = 4

        # write the file to the dest path
        try:
            with open(full_filename, 'wb') as f:
                f.write(content)
                f.close()
            os.chmod(full_filename, access_mode)
            os.chown(full_filename, uid, gid)
            checksum_local = file_hash_md5(full_filename)
            self._logger.debug("Local checksum: {}".format(checksum_local))
            self._logger.debug("Remote checksum: {}".format(checksum))
            if checksum_local != checksum:
                self._return_code = 2
                self._logger.fatal('File checksum not equally')
            else:
                self._return_code = 0
                self._logger.info('File checksum equally, file receive succeed')
        except OSError as e:
            self._logger.fatal(e)
            self._return_code = 3
        resp = FileResponse(id=file_id, status=self._return_code, message=str(self.CODE[self._return_code]))
        return resp


class BunnyThriftServer(Logger):
    def serve(self):
        file_handler = FileServiceHandler()
        processor = FileService.Processor(file_handler)
        print(SERVER_CONFIG['agent']['agent_thrift_port'])
        transport = TSocket.TServerSocket(host=SERVER_CONFIG['agent']['bind'],
                                          port=SERVER_CONFIG['agent']['agent_thrift_port'])
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        #processor.registerProcessor('ExecService', exec_processor)
        #processor.registerProcessor('FileService', file_processor)
        #processor.registerProcessor('RegistrationService', register_processor)

        server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
        server.setNumThreads(8)
        self._logger.info('Starting bunny thrift server on port ' + str(SERVER_CONFIG['agent']['agent_thrift_port']))
        server.serve()




