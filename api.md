# HTTP接口
1. GET /status
    - 描述: 获取服务状态
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
            {
              "installer": "
