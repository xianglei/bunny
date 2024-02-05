#!/usr/bin/env python3
# coding: utf-8

import os
import platform

def get_os_info():
    os_info = {}
    os_info['os_name'] = platform.system()
    os_info['os_release'] = platform.release()
    os_info['os_version'] = platform.version()
    os_info['os_arch'] = platform.machine()
    os_info['os_hostname'] = platform.node()
    os_info['os_platform'] = platform.platform()
    os_info['os_processor'] = platform.processor()
    os_info['os_cpu_count'] = os.cpu_count()
    return os_info

print(get_os_info())
