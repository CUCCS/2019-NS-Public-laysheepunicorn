# **基于 VirtualBox 的网络攻防基础环境搭建**

## **一、实验目的**
  
1. 掌握 VirtualBox 虚拟机的安装与使用；
2. 掌握 VirtualBox 的虚拟网络类型和按需配置；
3. 掌握 VirtualBox 的虚拟硬盘多重加载。

## **二、实验环境**

1. VirtualBox 虚拟机
    - 攻击者主机（Attacker）：Kali Rolling 2109.2
    - 网关（Gateway, GW）：Debian Buster
    - 靶机（Victim）：Debian Buster/xp-sp3 / Kali

2. 局域网、互联网环境，实验需要构建的网络拓扑结构如图1所示。
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/1.JPG)

3. 接入条件：Wi-Fi

## **三、实验步骤**

1. 在VirtualBox中一共新建六个虚拟机，如图2所示：
    - 新建两个kali虚拟机，其中一个作为攻击者，命名为KaliAttacker，另一个作为靶机之一；再建立两个Debian虚拟机，其中一个作为网关建立局域网使用，另一个作为靶机之一；建立两个xp-sp3虚拟机，均作为靶机。
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/2.JPG)

2. 对每一台虚拟机的网络进行配置，如图3、图4、图5、图6、图7、图8标注的红框部分所示：
    - 首先配置Kali-Attacker，在虚拟机的设置-网络中启用网卡1的网络链接，将链接方式更改为NAT网络。界面名称选择NatNetwork。（选择NAT网络的原因：是虚拟机访问外网的最好方式）
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/3.JPG)

    - 配置Debian-Gateway，在虚拟机的设置-网络中启用网卡1的网络链接，将链接方式更改为NAT网络。界面名称选择NatNetwork；再启用网卡3、网卡4的网络链接，均将链接方式改为内部网络，其中，网卡3的界面名称改为intnet1，网卡4的界面名称改为intnet2。（使用NAT网络的原因：将网关与攻击者放在同一虚拟网络中；使用内网原因：分别建立局域网intnet1、intnet2以构建实验要求的基本拓扑结构）
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/4.JPG)

    - 配置kali环境的victim1，虚拟机的设置-网络中启用网卡1的网络链接，将链接方式改为内部网络，界面名称改为intnet1。（原因：使kali-victim1只在intnet1的局域网中通过网关访问外部网络）
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/5.JPG)

    - 配置XP系统环境的victim1，虚拟机的设置-网络中启用网卡1的网络链接，将链接方式改为内部网络，界面名称改为intnet1。（原因：使XP-victim1只在intnet1的局域网中通过网关访问外部网络）
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/6.JPG)

    - 配置XP系统环境的victim2，虚拟机的设置-网络中启用网卡1的网络链接，将链接方式改为内部网络，界面名称改为intnet2，再将高级中的控制芯片换为PCnet-Fast III (Am79c973) 。（原因：使XP-victim2只在intnet2的局域网中通过网关访问外部网络；XP的版本太低，要选择适配的网卡驱动）
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/7.JPG)

    - 配置Debian环境的victim2，虚拟机的设置-网络中启用网卡1的网络链接，将链接方式改为内部网络，界面名称改为intnet2。（原因：使XP-victim2只在intnet2的局域网中通过网关访问外部网络）
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/8.JPG)

3. 虚拟机的存储部分，将端口的部分全部设置为多重加载，示例如图9。
    - 步骤：打开虚拟介质管理器，选择对应系统的虚拟盘，将属性中的类型改为多重加载，选择释放虚拟盘，再一次将虚拟盘挂载到虚拟机即可。
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/9.JPG)

    - 设置多重加载的原因：设置同样系统的虚拟机的时候节省重新安装系统的时间。

4. 使用ping命令检测每个网络是否能连接至外网，使用tcpdump抓包命令来证明在内网的靶机连通外部网络需要经过网关。
    - 具体实施步骤：  
    在网关的终端中使用tcpdump -i 对应的网卡名称 -n icmp的命令观察指定的包的流动情况。（先开启抓包器）  
    在靶机终端中使用ping 网关地址 -n（linux命令为-c） 发送包数命令。

## **四、实验结果**

1. 最终构建的网络拓扑结构如图10所示
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/10.JPG)

2. 对网络拓扑结构的逐一验证
    - 靶机可以直接访问攻击者主机。如图11、图12、图13、图14所示。
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/11.JPG)
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/12.JPG)
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/13.JPG)
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/14.JPG)

    - 攻击者主机无法直接访问靶机。如图15、图16、图17、图18所示。
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/15.JPG)
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/16.JPG)
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/17.JPG)
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/18.JPG)

    - 网关可以直接访问攻击者主机和靶机。如图19、图20、图21、图22、图23所示。
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/19.JPG)
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/20.JPG)
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/21.JPG)
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/22.JPG)
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/23.JPG)

    - 靶机的所有对外上下行流量必须经过网关。抓包验证如图24、图25、图26、图27所示。
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/24.JPG)
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/25.JPG)
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/26.JPG)
![Alt text](https://github.com/CUCCS/2019-NS-Public-laysheepunicorn/blob/chap0x01/chap0x01/img/27.JPG)

    - 所有节点均可以访问互联网。  
    据验证，所有靶机可通过网关访问互联网。  
    网关通过NAT网卡直接连接互联网，如图28所示。
    攻击者通过NAT网卡直接连接互联网，如图29所示。

## **五、实验问题总结**

1. 分不清“内部网络”和“网络地址转换（NAT）”导致构建网络拓扑失败。

2. 关闭xp靶机的防火墙就可以使xp靶机被网关访问不被攻击者访问，猜想是网关的防火墙导致的结果，但始终没有研究清楚和验证网关的防火墙和攻击者的关系。

3. 不知道如何更改内网自动分配的ip。
