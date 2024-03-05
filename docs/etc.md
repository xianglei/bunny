# 创建ssl key和cert(自签发不可用, 仅供开发测试)
```bash
cd ssl; openssl req -x509 -newkey rsa:4096 -nodes -keyout server.key -out server.crt -days 36500
```
