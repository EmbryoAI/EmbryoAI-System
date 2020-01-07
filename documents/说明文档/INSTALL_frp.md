# frp在ubuntu上安装使用方法

## 安装及启动sshd服务

打开命令终端，执行命令：

	sudo apt-get install openssh-server

此处需要输入一遍密码。安装完成后，再执行：

	sudo systemctl start sshd

## 获取打包文件
使用打包好的 frp_0.25.1_linux_amd64.tar.gz文件，或者到[这里](https://github.com/fatedier/frp/releases)下载相应打包文件。

## 解压文件

在打包文件目录下，执行命令：

	tar xvf frp_0.25.1_linux_amd64.tar.gz

然后

	cd  frp_0.25.1_linux_amd64

## 修改配置文件

执行命令：

	vim frpc.ini

在编辑器中，将文件内容修改为：

	[common]
	server_addr = 39.104.173.18
	server_port = 7000

	[ssh-a-unique-name] # 每个医院唯一的ssh标签名称
	type = tcp
	local_ip = 127.0.0.1
	local_port = 22
	remote_port = [远程端口号] # 每个医院在服务器上唯一的端口号

其中`[ssh-a-unique-name]`是每个医院唯一的ssh标签名称，由现场工程师分配，并记录整理。
其中远程端口号为开发团队为此台服务器分配的端口号，每个case都不一样，修改前请与开发团队确认。

## 执行frp客户端

执行命令：

	./frpc &

## 附录：已安装医院名单及对应ID和PORT

| 医院名称 | 城市 | 服务器端口号 | SSH标签名称 |
| - | - | - | - |
| 浙江省人民医院 | 杭州 | 10122 | ssh |
| 上海市第九人民医院 | 上海 | 10322 | ssh-shanghai-9yuan |


