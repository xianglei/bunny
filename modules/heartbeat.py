#!/usr/bin/env python3
# coding: utf-8

import grpc
import math
from modules.utils import *
from modules.grpc_module import api_pb2_grpc, api_pb2


class Heartbeat(Logger):
    def __init__(self):
        Logger.__init__(self)

    def heartbeat(self):
        while True:
            try:
                channel = grpc.insecure_channel(SERVER_CONFIG['server']['host'] + ':' +
                                                str(SERVER_CONFIG['server']['server_rpc_port']))
                stub = api_pb2_grpc.HeartbeatServiceStub(channel)
                local_millis = math.floor(datetime.datetime.now().timestamp() * 1000)

                response = stub.Heartbeat(api_pb2.HeartbeatRequest(machine_uniq_id="1",
                                                                   timestamp_millis=local_millis,
                                                                   ping="ping"))
                dt = datetime.datetime.fromtimestamp(local_millis/1000).strftime("%d-%m-%Y %H:%M:%S")
                self._logger.info("Heartbeat sent a ping to server {} at time {}".format(SERVER_CONFIG['server']['host'],
                                                                              dt))
                if response.pong == "pong":
                    server_time = response.timestamp_millis
                    self._logger.info("Server responded with a pong at time {}"
                                      .format(datetime.datetime.fromtimestamp(server_time/1000).strftime("%d-%m-%Y %H:%M:%S")))
                    skew = abs(server_time - local_millis)
                    if skew > 30:
                        self._logger.warn("Time skew detected, local time is off by", skew, "milliseconds")
                    else:
                        self._logger.info("Heartbeat successful, time skew is", skew, "milliseconds")
                else:
                    self._logger.fatal("Heartbeat failed, server did not respond with a pong")
                channel.close()
            except Exception as e:
                self._logger.error("Heartbeat failed: {}".format(e))
            time.sleep(int(SERVER_CONFIG['agent']['heartbeat_interval']))
