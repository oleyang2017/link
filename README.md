# link
一个开源的物联网平台

## 如何使用
```
docker-compose up -d
cd link 
python manager runserver
```

## 主要功能
- 设备管理
- 设备控制
- 触发器
- 数据图表

## 前端
目前只有微信小程序，未来会有web端
现在微信小程序限制越来越多，后面可能会使用flutter来写移动端

## 后端
主服务使用Django构建，通过grpc与emqx的钩子函数实现调用，触发器使用celery异步的方式处理。

## 项目进度
后端 20%
前端 15%
