# HTTP接口
1. GET /status
    - 描述: 获取服务状态, system, cpu, memory, network, storage等信息集合,具体内容参看下面的system等接口返回
    - 请求参数: 无
    - 返回参数: 
        - status: 服务状态
    - 示例:
        - 请求: GET /ping
        - 返回: 
            ```json
            {
              "ping": "pong"
            }
            ```

2. GET /installer
    - 描述: 获取安装器
    - 请求参数: 无
    - 返回参数: 
        - installer: 安装器
    - 示例:
        - 请求: GET /installer
        - 返回: 
            ```json
            { "pkg_manager": "yum" }
            ```
3. GET /system
    - 描述: 获取操作系统信息
    - 请求参数: 无
    - 返回参数: 
        - system: 系统信息
    - 示例:
        - 请求: GET /system
        - 返回: 
            ```json
            { 
              "architecture": [ "64bit", "ELF" ], 
              "boot_time": 1708846144.0, 
              "hostname": "node2", 
              "ip": "10.10.10.12", 
              "kernel_release": "4.18.0-348.el8.x86_64", 
              "machine": "x86_64", 
              "node": "node2", 
              "os_codename": "n/a", 
              "os_id": "centos", 
              "os_like": "rhel fedora", 
              "os_version_build_numer": "", 
              "os_version_id": "8", 
              "os_version_major": "8", 
              "os_version_minor": "", 
              "platform": "Linux-4.18.0-348.el8.x86_64-x86_64-with-glibc2.28", 
              "processor": "x86_64", 
              "system": "Linux", 
              "uname": [ "Linux", "node2", "4.18.0-348.el8.x86_64", "#1 SMP Tue Oct 19 15:14:17 UTC 2021", "x86_64", "x86_64" ], 
              "users": [ 
                { "host": "10.10.10.200", "name": "root", "pid": 6332, "started": 1708861558.0, "terminal": "pts/0" }, 
                { "host": "10.10.10.226", "name": "root", "pid": 242058, "started": 1709532084.0, "terminal": "pts/1" }, 
                { "host": "10.10.10.226", "name": "root", "pid": 242128, "started": 1709532154.0, "terminal": "pts/2" } 
              ], 
              "version": "#1 SMP Tue Oct 19 15:14:17 UTC 2021" 
            }
            ```

4. GET /network
    - 描述: 获取网络信息
    - 请求参数: 无
    - 返回参数: 
        - network: 网络信息
    - 示例:
        - 请求: GET /network
        - 返回: 
          ```json
            { 
              "net_if_addrs": 
              { "eno1": [ 
                  { "bytes_recv": 1605779352, "bytes_sent": 632437148, "dropin": 0, "dropout": 0, "errin": 0, "errout": 0, "packets_recv": 3901864, "packets_sent": 3381306 }, 
                  { "address": "10.10.10.12", "broadcast": "10.10.10.255", "family": 2, "netmask": "255.255.255.0", "ptp": null }, 
                  { "address": "fe80::ae1f:6bff:fed7:c7b2%eno1", "broadcast": null, "family": 10, "netmask": "ffff:ffff:ffff:ffff::", "ptp": null }, 
                  { "address": "ac:1f:6b:d7:c7:b2", "broadcast": "ff:ff:ff:ff:ff:ff", "family": 17, "netmask": null, "ptp": null }
                ], 
                "eno2": [ 
                  { "bytes_recv": 0, "bytes_sent": 0, "dropin": 0, "dropout": 0, "errin": 0, "errout": 0, "packets_recv": 0, "packets_sent": 0 }, 
                  { "address": "ac:1f:6b:d7:c7:b3", "broadcast": "ff:ff:ff:ff:ff:ff", "family": 17, "netmask": null, "ptp": null } 
                ], 
                "fqdn": "node2", 
                "hostname": "node2", 
                "ip": "10.10.10.12", 
                "lo": [ 
                  { "bytes_recv": 16081799993, "bytes_sent": 16081799993, "dropin": 0, "dropout": 0, "errin": 0, "errout": 0, "packets_recv": 577828, "packets_sent": 577828 }, 
                  { "address": "127.0.0.1", "broadcast": null, "family": 2, "netmask": "255.0.0.0", "ptp": null }, 
                  { "address": "::1", "broadcast": null, "family": 10, "netmask": "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff", "ptp": null }, 
                  { "address": "00:00:00:00:00:00", "broadcast": null, "family": 17, "netmask": null, "ptp": null } 
                ], 
                "virbr0": [ 
                  { "bytes_recv": 0, "bytes_sent": 0, "dropin": 0, "dropout": 0, "errin": 0, "errout": 0, "packets_recv": 0, "packets_sent": 0 }, 
                  { "address": "192.168.122.1", "broadcast": "192.168.122.255", "family": 2, "netmask": "255.255.255.0", "ptp": null }, 
                  { "address": "52:54:00:6a:05:7d", "broadcast": "ff:ff:ff:ff:ff:ff", "family": 17, "netmask": null, "ptp": null } 
                ], 
                "virbr0-nic": [ 
                  { "bytes_recv": 0, "bytes_sent": 0, "dropin": 0, "dropout": 0, "errin": 0, "errout": 0, "packets_recv": 0, "packets_sent": 0 }, 
                  { "address": "52:54:00:6a:05:7d", "broadcast": "ff:ff:ff:ff:ff:ff", "family": 17, "netmask": null, "ptp": null } 
                ] 
              } 
            }
          ```
5. GET /storage
    - 描述: 获取存储信息
    - 请求参数: 无
    - 返回参数: 
        - storage: 存储信息
    - 示例:
        - 请求: GET /storage
        - 返回: 
          ```json
            { "disk_partitions": 
              [ 
                  { 
                  "device": "/dev/sda4", 
                  "disk_io_counters": { 
                    "busy_time": 243584, 
                    "read_bytes": 9502294528,   
                    "read_count": 120129, 
                    "read_time": 132313, 
                    "write_bytes": 49698377728, 
                    "write_count": 472487, 
                    "write_time": 701235 
                  }, 
                  "disk_usage":{ 
                    "free": 43106791424, 
                    "percent": 42.6, 
                    "total": 75125227520, 
                    "used": 32018436096 
                  }, 
                  "fstype": "xfs", 
                  "maxfile": 255, 
                  "maxpath": 4096, 
                  "mountpoint": "/", 
                  "opts": "rw,relatime,attr2,inode64,logbufs=8,logbsize=32k,noquota" 
                }, { 
                  "device": "/dev/sda5", 
                  "disk_io_counters": { 
                    "busy_time": 1885, 
                    "read_bytes": 75538944, 
                    "read_count": 5937, 
                    "read_time": 1384, 
                    "write_bytes": 2097152, 
                    "write_count": 3, 
                    "write_time": 9 
                  }, "disk_usage":{ 
                    "free": 357397684224, 
                    "percent": 10.4, 
                    "total": 398747480064, 
                    "used": 41349795840  
                  }, 
                  "fstype": "xfs", 
                  "maxfile": 255, 
                  "maxpath": 4096, 
                  "mountpoint": "/home", 
                  "opts": "rw,relatime,attr2,inode64,logbufs=8,logbsize=32k,noquota" 
                }], 
                "total_disk_io_counters": { 
                  "busy_time": 247838, 
                  "read_bytes": 9633629184, 
                  "read_count": 133235, 
                  "read_time": 135099, 
                  "write_bytes": 49702609920, 
                  "write_count": 572507, 
                  "write_time": 704339 
                } 
            }
          ```

6. GET /memory
    - 描述: 获取内存信息
    - 请求参数: 无
    - 返回参数: 
        - memory: 内存信息
    - 示例:
        - 请求: GET /memory
        - 返回: 
          ```json
            { 
              "swap_memory": { 
                "free": 4294963200, 
                "percent": 0.0, 
                "sin": 0, 
                "sout": 0, 
                "total": 4294963200, 
                "used": 0 
              }, 
              "virtual_memory": { 
                "active": 5591728128, 
                "available": 126658609152, 
                "buffers": 4001792, 
                "cached": 10649530368, 
                "free": 117257375744, 
                "inactive": 7452119040, 
                "percent": 5.9, 
                "shared": 22073344, 
                "slab": 564768768, 
                "total": 134539161600, 
                "used": 6628253696 
              } 
            }
          ```

7. GET /cpu
    - 描述: 获取CPU信息
    - 请求参数: 无
    - 返回参数: 
        - cpu: CPU信息
    - 示例:
        - 请求: GET /cpu
        - 返回: 
          ```json
            { 
              "cpu_count": 20, 
              "cpu_percent": 0.1, 
              "cpu_percent_percpu": [ 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.0, 0.1, 0.0, 0.0, 0.1, 0.1, 0.1, 0.1 ], 
              "cpu_stats": { 
                "ctx_switches": 299293719, 
                "interrupts": 173328839, 
                "soft_interrupts": 72778528, 
                "syscalls": 0 
              }, 
              "cpu_times": { 
                "cores": [ 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687177.97, "iowait": 1.09, "irq": 48.99, "nice": 1.37, "softirq": 57.6, "steal": 0.0, "system": 362.3, "user": 106.66 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 686741.04, "iowait": 5.99, "irq": 192.76, "nice": 10.13, "softirq": 19.62, "steal": 0.0, "system": 157.52, "user": 689.97 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687048.1, "iowait": 1.57, "irq": 69.13, "nice": 4.13, "softirq": 16.81, "steal": 0.0, "system": 216.16, "user": 468.33 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687338.45, "iowait": 1.33, "irq": 60.74, "nice": 3.19, "softirq": 16.38, "steal": 0.0, "system": 128.98, "user": 278.38 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687173.03, "iowait": 1.95, "irq": 54.87, "nice": 12.18, "softirq": 17.27, "steal": 0.0, "system": 118.98, "user": 465.28 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687316.23, "iowait": 0.97, "irq": 50.56, "nice": 4.69, "softirq": 15.71, "steal": 0.0, "system": 122.93, "user": 334.53 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687413.09, "iowait": 0.62, "irq": 50.98, "nice": 16.11, "softirq": 9.28, "steal": 0.0, "system": 111.37, "user": 242.69 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687380.36, "iowait": 2.8, "irq": 47.49, "nice": 3.4, "softirq": 21.99, "steal": 0.0, "system": 110.13, "user": 279.4 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687361.32, "iowait": 4.66, "irq": 47.05, "nice": 9.26, "softirq": 15.54, "steal": 0.0, "system": 101.76, "user": 307.68 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687403.92, "iowait": 1.07, "irq": 41.01, "nice": 4.9, "softirq": 16.84, "steal": 0.0, "system": 137.65, "user": 242.82 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687522.03, "iowait": 2.51, "irq": 33.41, "nice": 1.83, "softirq": 13.91, "steal": 0.0, "system": 75.71, "user": 218.89 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687377.88, "iowait": 1.57, "irq": 43.35, "nice": 1.32, "softirq": 24.79, "steal": 0.0, "system": 130.69, "user": 281.8 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687474.71, "iowait": 0.78, "irq": 47.76, "nice": 2.77, "softirq": 26.16, "steal": 0.0, "system": 104.79, "user": 195.35 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687368.16, "iowait": 2.33, "irq": 44.58, "nice": 4.27, "softirq": 61.05, "steal": 0.0, "system": 112.21, "user": 267.86 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687424.75, "iowait": 2.37, "irq": 46.9, "nice": 2.88, "softirq": 19.05, "steal": 0.0, "system": 98.15, "user": 262.81 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687478.98, "iowait": 1.55, "irq": 45.4, "nice": 5.0, "softirq": 15.07, "steal": 0.0, "system": 93.12, "user": 214.08 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687475.76, "iowait": 0.47, "irq": 49.01, "nice": 7.16, "softirq": 19.85, "steal": 0.0, "system": 99.98, "user": 197.0 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687448.32, "iowait": 0.24, "irq": 42.95, "nice": 3.29, "softirq": 15.58, "steal": 0.0, "system": 108.81, "user": 242.11 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687102.19, "iowait": 0.83, "irq": 46.08, "nice": 4.07, "softirq": 11.11, "steal": 0.0, "system": 104.88, "user": 590.47 }, 
                  { "guest": 0.0, "guest_nice": 0.0, "idle": 687517.45, "iowait": 2.46, "irq": 41.02, "nice": 3.18, "softirq": 15.04, "steal": 0.0, "system": 108.73, "user": 174.4 } 
                ], 
                "idle": 13746543.84, 
                "iowait": 37.24, 
                "system": 2604.94, 
                "user": 6060.61 
              } 
            }
          ```

8. GET /services
    - 描述: 获取服务状态
    - 请求参数: services: 服务名列表, 逗号分割, 如 /services?services=namenode,datanode,resourcemanager,nodemanager
    - 返回参数: 
      - services: 服务状态
      ```json
      [ 
        { "pid": 11453, "service": "google", "status": true }, 
        { "pid": 80142, "service": "netbiosd", "status": true } 
      ]
      ```
      - 如没有给出参数, 返回数组service null
      ```json
      [{"service": null}]
      ```

9. GET /service
    - 描述: 获取服务状态
    - 请求参数: service: 单个参数服务名关键字如 /service?service=namenode
    - 返回参数:
      - services: 服务状态
      ```json
      { "pid": 11453, "service": "google", "status": true }
      ```
      - 如没有给出参数, 返回service null
      ```json
      {"service": null}
      ```

# GRPC接口
1. Exec
    - 描述: 阻塞执行命令并返回结果
    - 请求参数: 
        - command: 命令
    - 返回参数: 
        - result: 执行结果
    - 示例:
        - 请求: 
          - request.exec_id: 执行id, 全局唯一, 建议uuid
          - request.cmd: 执行命令 例如 "ls /"
        - 返回: 
          - response.exec_id: 执行id
          - response.stdout: 标准输出
          - response.stderr: 标准错误输出
          - response.exit_code: 退出码

2. StreamExec
    - 描述: 非阻塞执行命令并实时流式返回结果(目前为阻塞执行,流式返回)
    - 请求参数: 
        - request.exec_id: 执行id, 全局唯一, 建议uuid
        - request.cmd: 命令
        - request.timeout: 超时时间
    - 返回参数: 
        - exec_id: 执行id
        - type: 枚举类型, 0: 标准输出, 1: 标准错误输出
        - output: 输出行
        - continued: 有内容则为true, 否则为false, 相当于EOF
        - exit_code: 退出码 
    - 示例:
        - 请求: 
          - request.exec_id: 执行id, 全局唯一, 建议uuid
          - request.cmd: 执行命令 例如 "ls /"
          - request.timeout: 超时时间, 默认 300
        - 返回: 
          - yield api_pb2.ExecStreamResponse(exec_id=exec_id, type=self.OutputType[1], output=line.encode(), continued=False, exit_code=ret)

# Thrift接口
1. FileService
   - 描述: 文件服务
   - 方法
     - Send
       - 描述: 发送文件
       - 请求参数: 
         - 结构体 FileRequest
           - string id: 文件id
           - string filename: 文件名
           - string path: 文件路径
           - string checksum: 文件校验码(md5sum)
           - binary content: 文件内容(base64编码)
           - string access_modes: 文件权限(664, 755 字符串)
           - string owner: 文件所有者
           - string group: 文件所属组
           - FileFormat format: 文件格式
       - 返回参数: 
         - string id: 文件id
         - Code status: 返回状态
         - string message: 返回消息
       - 枚举 FileFormat
         - JSON: 0
         - INI: 1
         - XML: 2
         - YAML: 3
         - BASH: 4
       - 枚举 Code
         - OK: 0
         - DIR_NOT_EXISTS: 1
         - CONTENT_CHECKSUM_ERROR: 2
         - WRITE_NOT_ALLOWED: 3
         - UNKNOWN_ERROR: 4






