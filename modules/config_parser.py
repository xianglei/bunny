#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
CONFIG_DIR = BASE_DIR + 'conf/'
SCRIPT_DIR = BASE_DIR + 'scripts/'
LOGS_DIR = BASE_DIR + 'logs/'
LOGS_EXEC_DIR = LOGS_DIR + 'exec/'
RUN_DIR = BASE_DIR + 'run/'
TMP_DIR = BASE_DIR + 'tmp/'
DEFAULT_CONFIG = {
    "agent": {
        "bind": "0.0.0.0",
        "agent_rpc_port": 7182,
        # "agent_thrift_port": 7183,
        "agent_http_port": 7181,
        "agent_http_thread_pool": 20,
        "version": "0.0.1",
        "heartbeat_interval": 30,
        "log_level": "INFO",
        "executor_timeout": 300,
        "log_file": "agent.log",
        "log_file_max_size": 209715200,
        "log_file_backup_count": 10,
    },
    "server": {
        "host": "localhost",
        "server_rpc_port": 7182,
        # "server_thrift_port": 7183,
        "server_http_port": 7181,
        "secret": "HeavyMetalWillNeverDie!!!"
    }
}


def compare_dict(dict1, dict2):
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        if len(dict1) != len(dict2):
            return False
        else:
            for key in dict1:
                if key not in dict2:
                    return False
                else:
                    if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                        if not compare_dict(dict1[key], dict2[key]):
                            return False
                    else:
                        if dict1[key] != dict2[key]:
                            return False
            return True
    else:
        return False


def config_parser():
    config_file = CONFIG_DIR + 'bunny.yaml'
    if not os.path.exists(CONFIG_DIR):
        try:
            os.mkdir(CONFIG_DIR, mode=0o664)
        except OSError as e:
            print(e)
    if not os.path.exists(SCRIPT_DIR):
        try:
            os.mkdir(SCRIPT_DIR, mode=0o664)
        except OSError as e:
            print(e)
    if not os.path.exists(LOGS_DIR):
        try:
            os.mkdir(LOGS_DIR, mode=0o664)
        except OSError as e:
            print(e)
    if not os.path.exists(config_file):
        try:
            with open(config_file, encoding='utf-8', mode='w') as f:
                print('Writing default config to %s' % config_file)
                f.write(yaml.dump(DEFAULT_CONFIG))
        except Exception as e:
            print(e)
        finally:
            f.close()

    try:
        with open(config_file, encoding='utf-8', mode='r') as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader)
            if config is not None and compare_dict(config, DEFAULT_CONFIG) is False:
                return config
            else:
                return DEFAULT_CONFIG
    except Exception as e:
        print(e)
        return DEFAULT_CONFIG
    finally:
        f.close()


SERVER_CONFIG = config_parser()

