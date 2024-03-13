# 此功能agent已完成, 暂未发布
# 添加principal

  - POST /kadmin/principal
  - request json
    ```json
    {
        "admin_principal": "xxxx/admin@EXAMPLE.COM"
        "admin_password": "xxxx",
        "admin_keytab": "/etc/security/xxxx.keytab",
        // admin password或keytab必须给一个, 否则无法认证
        "realm": "EXAMPLE.COM",
        "user": "username to be added",
        "fqdn": "full qualified domain name",
        //fqdn为主机全部域名, 例如: host1.example.com, 可为空, 为空则agent取当前主机名称
    }
    ```
  - response json
    ```json
    {
        "status": "success",
        "message": "principal added",
        "principal": "username"
    }
    ```
    ```json
    {
        "status": "failed",
        "message": "principal add failed",
        "principal": "username"
    }
    ```

# 删除principal

    删除指定principal后需要调用 /kadmin/keytab 接口 DELETE 方法删除对应的keytab文件
  - DELETE /kadmin/principal
  - request json
    ```json
    {
        "admin_principal": "xxxx/admin@EXAMPLE.COM"
        "admin_password": "xxxx",
        "admin_keytab": "/etc/security/xxxx.keytab",
        // admin password或keytab必须给一个, 否则无法认证
        "realm": "EXAMPLE.COM",
        "user": "username to be added",
        "fqdn": "full qualified domain name",
        //fqdn为主机全部域名, 例如: host1.example.com, 可为空, 为空则agent取当前主机名称
    }
    ```
  - response json
    ```json
    {
        "status": "success",
        "message": "principal deleted",
        "principal": "username"
    }
    ```
    ```json
    {
        "status": "failed",
        "message": "principal delete failed",
        "principal": "username"
    }
    ```

# 获取principal列表
  - GET /kadmin/principal
  - request json
    ```json
    {
        "admin_principal": "xxxx/admin@EXAMPLE.COM",
        "admin_password": "xxxx",
        "admin_keytab": "/etc/security/xxxx.keytab",
        // admin password或keytab必须给一个, 否则无法认证
        "realm": "EXAMPLE.COM",
        "keyword": "keyword"
        // keyword为关键字, 可为空, 为空则返回所有principal
    }
    ```
  - response json
    ```json
    {
        "status": "success",
        "message": "principal list",
        "principals": ["aaa/hostname1@A.COM", "aab/hostname2@A.COM", "aaa/hostname3@A.COM"]
    }
    ```

# 创建keytab

    该接口会根据给出的用户名创建一个当前主机或指定主机名的keytab文件, 并将该文件放置在指定路径

  - POST /kadmin/keytab
  - request json
    ```json
    {
        "admin_principal": "xxxx/admin@EXAMPLE.COM",
        "admin_password": "xxxx",
        "admin_keytab": "/etc/security/xxxx.keytab",
        // admin password或keytab必须给一个, 否则无法认证
        "realm": "EXAMPLE.COM",
        "fqdn": "full qualified domain name",
        "keytab_path": "/etc/hadoop/conf/hdfs.keytab"
    }
    ```
  - response json
    ```json
    {
        "status": "success",
        "message": "keytab created",
        "keytab_path": "/etc/hadoop/conf/hdfs.keytab",
        "principal": "username"
    }
    ```
    ```json
    {
        "status": "failed",
        "message": "keytab create failed",
        "keytab_path": "/etc/hadoop/conf/hdfs.keytab",
        "principal": "username"
    }
    ```

# 删除keytab

    该接口会删除指定路径下的keytab文件

  - DELETE /kadmin/keytab
  - request json
    ```json
    {
        "admin_principal": "xxxx/admin@EXAMPLE.COM",
        "admin_password": "xxxx",
        "admin_keytab": "/etc/security/xxxx.keytab",
        // admin password或keytab必须给一个, 否则无法认证
        "realm": "EXAMPLE.COM",
        "keytab_path": "/etc/hadoop/conf/hdfs.keytab"
    }
