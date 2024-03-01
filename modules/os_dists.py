#!/usr/bin/env python3
# coding: utf-8

import os
import platform
import distro


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
    os_info['os_id'] = distro.info()['id']
    os_info['os_version_id'] = distro.info()['version']
    os_info['os_like'] = distro.info()['like']
    os_info['os_codename'] = distro.info()['codename']
    os_info['os_version_major'] = distro.info()['version_parts']['major']
    os_info['os_version_minor'] = distro.info()['version_parts']['minor']
    os_info['os_version_build_numer'] = distro.info()['version_parts']['build_number']
    return os_info


print(get_os_info())
