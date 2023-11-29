#!/usr/bin/env python3
# coding: utf-8
import os

import daemon
import sys
import threading
import signal

import psutil
from daemon import pidfile
# from .grpc_server import *
from .thrift_server import *
from .cp_server import *
# from grpc_client import *
from .utils import *


def exception_callback(e):
    # handle the exception
    print("Caught an exception in thread:", e)


class BunnyDaemon(Logger):
    def __init__(self):
        Logger.__init__(self)
        # self.grpc_server = BunnyGrpcServer()
        self.cp_server = BunnyCherrypyServer()
        self.thrift_server = BunnyThriftServer()

    # def _run_grpc_server(self):
    #     self.grpc_server.serve()

    def _run_thrift_server(self):
        self.thrift_server.serve()

    def _run_cp_server(self):
        self.cp_server.start()

    def start(self):
        if not self._check_proc_alive():
            try:
                with daemon.DaemonContext(working_directory=BASE_DIR,
                                          umask=0o002,
                                          pidfile=pidfile.TimeoutPIDLockFile(BASE_DIR + 'run/bunny.pid'),
                                          stdout=self._logger.info(sys.stdout),
                                          stderr=self._logger.error(sys.stderr)
                                          ):
                    self._logger.info("Starting Bunny...")
                    self._logger.info("Starting Cherrypy server...")
                    self._logger.info("Starting gRPC server...")

                    threads = []
                    # for i in range(4):
                    #     grpc_server_thread = threading.Thread(target=self._run_grpc_server)
                    #     threads.append(grpc_server_thread)
                    #     grpc_server_thread.daemon = True
                    #     grpc_server_thread.start()
                    thrift_server_thread = threading.Thread(target=self._run_thrift_server)
                    threads.append(thrift_server_thread)
                    thrift_server_thread.daemon = True
                    thrift_server_thread.start()
                    cherrypy_thread = threading.Thread(target=self._run_cp_server)
                    threads.append(cherrypy_thread)
                    cherrypy_thread.daemon = True
                    cherrypy_thread.start()
                    for t in threads:
                        t.join()

                    '''
                    grpc_thread = threading.Thread(target=self._run_grpc_server)
                    cherrypy_thread = threading.Thread(target=self._run_cp_server)
                    threads = [grpc_thread, cherrypy_thread]
                    for t in threads:
                        t.daemon = True
                        t.start()
                    t.join()
                    '''
            except Exception as e:
                self._logger.fatal(e)
                self.stop()
                exit(1)
        else:
            self._logger.info("Bunny is not exit correctly or already started.")
            self._logger.info("Please check pid file: " + BASE_DIR + 'run/bunny.pid')
            self._logger.info("If you are sure that Bunny is not running, please restart Bunny.")
            #try:
            #    os.remove(BASE_DIR + 'run/bunny.pid')
            #except Exception as e:
            #    self._logger.fatal(e)
            #    exit(1)

    def stop(self, pid=BASE_DIR + 'run/bunny.pid'):
        try:
            self._logger.info("Stopping Bunny...")
            self._logger.info("Stopping CherryPy server...")
            cherrypy.engine.stop()
            cherrypy.engine.exit()
            self._logger.info("CherryPy server stopped...")
            self._logger.info("Stopping thrift server...")
            with open(pid, 'r') as f:
                pid = int(f.read())
            try:
                os.remove(BASE_DIR + 'run/bunny.pid')
                self._logger.info("pid file removed...")
            except OSError as e:
                self._logger.fatal(e)
            self._logger.info("thrift server stopped...")
            try:
                self._logger.info("Bunny Agent Server stopped...")
                os.kill(pid, signal.SIGTERM)
            except OSError as e:
                self._logger.fatal(e)
        except Exception as e:
            self._logger.fatal(e)
            exit(1)

    def restart(self, pid=BASE_DIR + 'run/bunny.pid'):
        self.stop(pid)
        self.start()
        return 'Bunny restarted.'

    def status(self):
        if os.path.exists(BASE_DIR + 'run/bunny.pid'):
            with open(BASE_DIR + 'run/bunny.pid', 'r') as f:
                pid = f.read()

            return 'Bunny is running on pid ' + pid
        else:
            return 'Bunny is not running.'

    def _check_proc_alive(self):
        if os.path.exists(BASE_DIR + 'run/bunny.pid'):
            with open(BASE_DIR + 'run/bunny.pid', 'r') as f:
                pid = f.read()
                print('pid: ' + pid)
            if psutil.pid_exists(int(pid)):
                print('Bunny is running on pid ' + pid)
                return True
            else:
                try:
                    os.kill(int(pid), 0)
                except OSError as e:
                    print(e)
                    try:
                        os.remove(BASE_DIR + 'run/bunny.pid')
                    except OSError as e:
                        print(e)
                    return False
        else:
            print('Bunny is not running.')
            return False








