#!/usr/bin/env python3
# coding: utf-8

import psutil
import socket
import platform
# import json
from utils import Logger

LOGGER = Logger()


def get_cpu_info():
    cpu_info = {}
    if psutil.LINUX:
        cpu_info['cpu_count'] = psutil.cpu_count()
        cpu_info['cpu_percent'] = psutil.cpu_percent()
        cpu_info['cpu_percent_percpu'] = psutil.cpu_percent(percpu=True)

        cpu_info['cpu_times'] = {}
        cpu_times = psutil.cpu_times()
        cpu_info['cpu_times']['user'] = cpu_times.user
        cpu_info['cpu_times']['system'] = cpu_times.system
        cpu_info['cpu_times']['idle'] = cpu_times.idle
        cpu_info['cpu_times']['iowait'] = cpu_times.iowait
        cpu_info['cpu_times']['cores'] = []
        for per_time in psutil.cpu_times(percpu=True):
            cpu_info['cpu_times']['cores'].append(per_time._asdict())

        cpu_info['cpu_stats'] = {}
        cpu_stats = psutil.cpu_stats()
        cpu_info['cpu_stats']['ctx_switches'] = cpu_stats.ctx_switches
        cpu_info['cpu_stats']['interrupts'] = cpu_stats.interrupts
        cpu_info['cpu_stats']['soft_interrupts'] = cpu_stats.soft_interrupts
        cpu_info['cpu_stats']['syscalls'] = cpu_stats.syscalls
    else:
        raise OSError('OS not supported')

    return cpu_info


def get_memory_info():
    memory_info = {}
    if psutil.LINUX:
        memory_info['virtual_memory'] = {}
        virtual_memory = psutil.virtual_memory()
        memory_info['virtual_memory']['total'] = virtual_memory.total
        memory_info['virtual_memory']['available'] = virtual_memory.available
        memory_info['virtual_memory']['percent'] = virtual_memory.percent
        memory_info['virtual_memory']['used'] = virtual_memory.used
        memory_info['virtual_memory']['free'] = virtual_memory.free
        memory_info['virtual_memory']['active'] = virtual_memory.active
        memory_info['virtual_memory']['inactive'] = virtual_memory.inactive
        memory_info['virtual_memory']['buffers'] = virtual_memory.buffers
        memory_info['virtual_memory']['cached'] = virtual_memory.cached
        memory_info['virtual_memory']['shared'] = virtual_memory.shared
        memory_info['virtual_memory']['slab'] = virtual_memory.slab

        memory_info['swap_memory'] = {}
        swap_memory = psutil.swap_memory()
        memory_info['swap_memory']['total'] = swap_memory.total
        memory_info['swap_memory']['used'] = swap_memory.used
        memory_info['swap_memory']['free'] = swap_memory.free
        memory_info['swap_memory']['percent'] = swap_memory.percent
        memory_info['swap_memory']['sin'] = swap_memory.sin
        memory_info['swap_memory']['sout'] = swap_memory.sout
    else:
        raise OSError('OS not supported')
    return memory_info


def get_disk_info():
    disk_info = {}
    if psutil.LINUX or psutil.MACOS:
        disk_io_counters = psutil.disk_io_counters()
        disk_info['total_disk_io_counters'] = {}
        disk_info['total_disk_io_counters']['read_count'] = disk_io_counters.read_count
        disk_info['total_disk_io_counters']['write_count'] = disk_io_counters.write_count
        disk_info['total_disk_io_counters']['read_bytes'] = disk_io_counters.read_bytes
        disk_info['total_disk_io_counters']['write_bytes'] = disk_io_counters.write_bytes
        disk_info['total_disk_io_counters']['read_time'] = disk_io_counters.read_time
        disk_info['total_disk_io_counters']['write_time'] = disk_io_counters.write_time
        #disk_info['total_disk_io_counters']['read_merged_count'] = disk_io_counters.read_merged_count
        #disk_info['total_disk_io_counters']['write_merged_count'] = disk_io_counters.write_merged_count
        disk_info['total_disk_io_counters']['busy_time'] = disk_io_counters.busy_time

        disk_partitions = psutil.disk_partitions()
        disk_info['disk_partitions'] = []
        for disk_partition in disk_partitions:
            disk_info['disk_partitions'].append(disk_partition._asdict())
            disk_usage = psutil.disk_usage(disk_partition.mountpoint)
            try:
                disk_io_counters = psutil.disk_io_counters(perdisk=True)[disk_partition.device.split('/')[-1]]
            except KeyError:
                disk_io_counters = None

            if disk_io_counters is not None \
                    and \
                    disk_info['disk_partitions'][-1]['device'].split('/')[-1] == disk_partition.device.split('/')[-1]:
                disk_info['disk_partitions'][-1]['disk_io_counters'] = {}
                disk_info['disk_partitions'][-1]['disk_io_counters']['read_count'] = \
                    disk_io_counters.read_count
                disk_info['disk_partitions'][-1]['disk_io_counters']['write_count'] = \
                    disk_io_counters.write_count
                disk_info['disk_partitions'][-1]['disk_io_counters']['read_bytes'] = \
                    disk_io_counters.read_bytes
                disk_info['disk_partitions'][-1]['disk_io_counters']['write_bytes'] = \
                    disk_io_counters.write_bytes
                disk_info['disk_partitions'][-1]['disk_io_counters']['read_time'] = \
                    disk_io_counters.read_time
                disk_info['disk_partitions'][-1]['disk_io_counters']['write_time'] = \
                    disk_io_counters.write_time
                # disk_info['disk_partitions'][-1]['disk_io_counters']['read_merged_count'] = \
                # disk_io_counters.read_merged_count
                # disk_info['disk_partitions'][-1]['disk_io_counters']['write_merged_count'] = \
                # disk_io_counters.write_merged_count
                disk_info['disk_partitions'][-1]['disk_io_counters']['busy_time'] = disk_io_counters.busy_time
            disk_info['disk_partitions'][-1]['disk_usage'] = {}
            disk_info['disk_partitions'][-1]['disk_usage']['total'] = disk_usage.total
            disk_info['disk_partitions'][-1]['disk_usage']['used'] = disk_usage.used
            disk_info['disk_partitions'][-1]['disk_usage']['free'] = disk_usage.free
            disk_info['disk_partitions'][-1]['disk_usage']['percent'] = disk_usage.percent
    else:
        raise OSError('OS not supported')
    return disk_info


def get_net_if_info():
    net_if_info = {}
    if psutil.LINUX:
        net_if_info['net_if_addrs'] = {}
        net_if_info['net_if_addrs']['hostname'] = socket.gethostname()
        net_if_info['net_if_addrs']['fqdn'] = socket.getfqdn()
        net_if_info['net_if_addrs']['ip'] = socket.gethostbyname(net_if_info['net_if_addrs']['hostname'])
        net_if_addrs = psutil.net_if_addrs()
        for net_if_name, net_if_addrs in net_if_addrs.items():
            net_if_info['net_if_addrs'][net_if_name] = []
            net_io_counters = psutil.net_io_counters(pernic=True)[net_if_name]
            net_if_info['net_if_addrs'][net_if_name].append(net_io_counters._asdict())
            for net_if_addr in net_if_addrs:
                net_if_info['net_if_addrs'][net_if_name].append(net_if_addr._asdict())
    return net_if_info


def get_system_info():
    system_info = {}
    if psutil.LINUX:
        system_info['boot_time'] = psutil.boot_time()
        system_info['machine'] = platform.machine()
        system_info['node'] = platform.node()
        system_info['architecture'] = list(platform.architecture())
        system_info['platform'] = platform.platform()
        system_info['processor'] = platform.processor()
        system_info['release'] = platform.release()
        system_info['system'] = platform.system()
        system_info['uname'] = list(platform.uname())
        system_info['version'] = platform.version()
        system_info['hostname'] = socket.gethostname()
        try:
            system_info['ip'] = socket.gethostbyname(system_info['hostname'])
        except socket.gaierror:
            system_info['ip'] = ''
        system_info['users'] = []
        for user in psutil.users():
            system_info['users'].append(user._asdict())
    else:
        raise OSError('OS not supported')
    return system_info


def retrieve_info():
    info = {}
    info['cpu_info'] = get_cpu_info()
    info['memory_info'] = get_memory_info()
    info['disk_info'] = get_disk_info()
    info['net_if_info'] = get_net_if_info()
    return info



