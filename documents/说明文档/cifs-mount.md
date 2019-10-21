# 在Ubuntu上安装buffalo TeraStation网络硬盘

## 安装需要的软件包
```
sudo apt update
sudo apt install cifs-utils
```
## 一次mount
```
sudo mount -t cifs -o rw,vers=1.0,username=username,password=password,uid=linuxuser //[TeraStation IP]/share /mnt/share
```

## 编辑fstab，自动mount
在fstab文件中添加一行
```
//[TeraStation IP]/share /mnt/share auto rw,vers=1.0,username=username,password=password,uid=linuxuser 0 0
```

## 常见问题

如果出现network unreachable错误，说明网络还未准备好，此时试图mount网络文件系统会发生错误，**严重时可能让Ubuntu启动时进入emergency mode**。

此时有两种解决方案：

1. /etc/fstab文件改为

```
//[TeraStation IP]/share /mnt/share auto rw,vers=1.0,username=username,password=password,uid=linuxuser,_netdev 0 0
```

2. 注释掉fstab的自动mount，在应用的start-all.sh中启动应用服务之前加入

```
until ping -nq -c3 [TeraStation IP]; do
   # Waiting for network
   sleep 1
done
mount -t cifs -o rw,vers=1.0,username=username,password=password,uid=linuxuser //[TeraStation IP]/share /mnt/share
```
