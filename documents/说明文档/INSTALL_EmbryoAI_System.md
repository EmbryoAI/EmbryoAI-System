# EmbryoAI-System 安装说明

## 前提和要求

### 服务器硬件需求

EmbryoAI-System因为要对图像进行大量模式识别和机器学习方面的处理，因此对计算资源要求较高。由于数据库系统也是装在本地服务器上，因此，对于存储资源也有一定的要求。

| 硬件 | 最低配置 | 建议配置 |
| -- | -- | --|
| CPU | Intel Core i5 | Intel Xeon E |
| RAM | 8GiB | 16GiB |
| Hard Drive | SATA 100GB | SSD 200GB |
| Graphics | N/A | Nvidia GTX 1080 |
| LAN | 1 * 100MiB interfaces | 2 * 1000MiB interfaces |
| WAN | 10MiB up/down bandwidth | 100MiB up/down bandwidth |
| Monitor | 19 inchs LED | 22 inchs LED |

### 操作系统

- Ubuntu Desktop 16.04 LTS （推荐）
- CentOS 7.0 with GNome Desktop

请参考网上说明正确安装Ubuntu桌面中文版。设置用户astec（需要密码登录）及system（免密码登录）用户。

### 网络设置

局域网使用C类内网地址段 192.168.40.0/24。因为使用了4G路由器连接internet，因此需要将路由器的地址设置为 192.168.40.1，DHCP开启，分配地址段为 192.168.40.101 - 192.168.40.200，这段地址提供给接入4G无线路由器的其他终端如PC、PAD、移动电话使用。

iBIS应该设定IP地址为 192.168.40.20，NAS硬盘应该设定IP地址为 192.168.40.10，EmbryoAI-System服务器应该设定IP地址为 192.168.40.100。

