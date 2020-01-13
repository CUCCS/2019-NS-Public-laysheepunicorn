# **无线网络嗅探基础**

## **一、实验目的**

- 掌握网络扫描之端口状态探测的基本原理

## **二、实验环境**

- python + scapy
- 2个kali系统虚拟机
- debian作为网关

## **三、实验要求**

- 禁止探测互联网上的 IP ，严格遵守网络安全相关法律法规
- 完成以下扫描技术的编程实现
  - TCP connect scan / TCP stealth scan
  - TCP Xmas scan / TCP fin scan / TCP null scan
  - UDP scan

## **四、实验前期说明**

1. 扫描方法原理
    - TCP connect scan
        - 首先发送一个 SYN 数据包到目标主机的特定端口上，接着我们可以通过接收包的情况对端口的状态进行判断：
            - 如果接收到的是一个 RST/ACK 数据包，通常意味着端口是关闭的并且链接将会被重置；
            - 而如果目标主机没有任何响应则意味着目标主机的端口处于过滤状态；
            - 若接收到SYN/ACK数据包（即检测到端口是开启的），便发送一个 ACK 确认包到目标主机，这样便完成了三次握手连接机制。成功后再终止连接。
    - TCP stealth scan
        - 与 TCP Connect 扫描不同，TCP SYN 扫描并不需要打开一个完整的链接。发送一个SYN包启动三方握手链接机制，并等待响应。
            - 如果我们接收到一个SYN/ACK包表示目标端口是开放的，当得到的是一个SYN/ACK包时通过发送一个 RST 包立即拆除连接；
            - 如果接收到一个RST/ACK包表明目标端口是关闭的；
            - 如果端口是被过滤的状态则没有响应。
    - TCP xmas scan
        - 发送一个TCP包，并对TCP报文头FIN、URG和PUSH标记进行设置。
            - 若是关闭的端口则响应RST报文；
            - 开放或过滤状态下的端口则无任何响应。
    - TCP fin scan
        - 仅发送 FIN 包，它可以直接通过防火墙。
            - 如果端口是关闭的就会回复一个RST包；
            - 如果端口是开放或过滤状态则对FIN包没有任何响应。
    - TCP null scan
        - 发送一个 TCP 数据包，关闭所有 TCP 报文头标记。
            - 只有关闭的端口会发送RST响应。
    - UDP scan
        - UDP是一个无链接的协议，当我们向目标主机的UDP端口发送数据,我们并不能收到一个开放端口的确认信息,或是关闭端口的错误信息。可是，在大多数情况下，当向一个未开放的UDP端口发送数据时,其主机就会返回一个ICMP不可到达(ICMP_PORT_UNREACHABLE)的错误，因此大多数UDP端口扫描的方法就是向各个被扫描的UDP端口发送零字节的UDP数据包
2. 实验网络环境拓扑模拟
    - 在virtual box虚拟机中，网关Debian-Getway设置一个网卡为“内部网络internet1”，其余两台kali虚拟机kali-victim1、kali-attacker的网络均设置为“内部网络internet1”，这样就构建出一个内网网络拓扑结构。
3. 被测试IP的端口状态的模拟(以80端口为例子)
    - 未做任何设置之前在虚拟机内都是关闭状态
    ![ ](image\目标对象端口关闭.JPG)
    - 使用iptables -I INPUT -p tcp(udp) --dport 80 -j REJECT将80端口加入防火墙，模拟过滤状态
    ![ ](image\目标对象端口防火墙过滤.JPG)
    ![ ](image\udp80端口过滤.JPG)
    - 使用nc -lp 80 &打开80端口模拟端口开放(在此之前注意使用iptables -F命令清除预设表filter中的所有规则链的规则、iptables -X命令清除预设表filter中使用者自定链中的规则，保证防火墙不影响端口)
    ![ ](image\目标对象端口开放.JPG)

## **五、实验结果**

1. Tcp connet scan
在目标主机存在的情况下，tcp连接扫描端口有三种状况：

    - 过滤（Filtered）：发送syn数据包最终未得到响应，被防火墙过滤，实际上iptables防火墙会返回一个ICMP不可到达(ICMP_PORT_UNREACHABLE)的错误(这里是与课本的区别)
    ![ ](image\tcp-connect过滤.JPG)
    - 开放（Open）：发送syn数据包接收到的是一个SYN/ACK数据包，即flags==0x12，则说明端口是开放状态的
    ![ ](image\tcp-connect开放.JPG)
    - 关闭（Closed）：发送syn接收到的是一个RST/ACK数据包，即flags==0x14，通常意味着端口是关闭的并且链接将会被重置
    ![ ](image\tcp-connect关闭.JPG)

2. TCP stealth scan
端口扫描的状态和connect scan并无差别，区别只在于这种扫描方式发送方无论收到什么数据包，都会向该端口发送一个RST/ACK包(flag==R和flag==AR的区别。3693)，这样就没有建立一个完整的TCP连接，但是发送方却知道了这个端口是否开放，并且这种扫描并不会在目标系统上产生连接日志

    - 过滤（Filtered）：发送syn数据包最终未得到响应，被防火墙过滤，实际上iptables防火墙会返回一个ICMP不可到达(ICMP_PORT_UNREACHABLE)的错误(这里是与课本的区别)
    ![ ](image\tcp-stealth过滤.JPG)
    - 开放（Open）：发送syn数据包接收到的是一个SYN/ACK数据包，即flags==0x12，则说明端口是开放状态的
    ![ ](image\tcp-stealth开放.JPG)
    - 关闭（Closed）：发送syn接收到的是一个RST/ACK数据包，即flags==0x14，通常意味着端口是关闭的
    ![ ](image\tcp-stealth关闭.JPG)

3. TCP xmas scan
发送一个 TCP 包，并对 TCP 报文头 FIN、URG 和 PUSH 标记进行设置。由于这三个标志位不能被同时设置，所以可以用来判断端口开放。

    - 关闭（Closed）：发送的数据包接收到的是一个RST/ACK数据包，即flags==0x14，通常意味着端口是关闭的
    ![ ](image\tcp-xmas关闭.JPG)
    - 开放（Open）：发送的数据包被丢弃，则说明端口可能是开放状态的
    ![ ](image\tcp-xmas开放.JPG)
    - 过滤（Filtered）：发送的数据包被丢弃，则说明端口可能是过滤状态的
    ![ ](image\tcp-xmas过滤.JPG)

4. TCP fin scan
首先向目标端口发送一个FIN数据包（结束连接）(flag=F)，按照RFC793的规定，目标端口如果是一个关闭的端口，那么将会返回一个RST数据包；如果是一个打开的端口将会忽略这个请求。

    - 关闭（Closed）：发送的数据包接收到的是一个RST/ACK数据包，即flags==0x14，通常意味着端口是关闭的
    ![ ](image\tcp-fin关闭.JPG)
    - 开放（Open）：发送的数据包被丢弃，则说明端口可能是开放状态的
    ![ ](image\tcp-fin开放.JPG)
    - 过滤（Filtered）：发送的数据包被丢弃，则说明端口可能是过滤状态的
    ![ ](image\tcp-fin过滤.JPG)
5. TCP null scan
发送一个不带任何标志位的tcp数据包给目标主机，如果目标端口关闭，那么就会返回一个RST数据包；如果目标端口开放或者过滤则什么都不返回，直接丢弃这个数据包。只对遵守RFC793规定的基于UNIX的主机有效,windows主机无论关闭与否都会返回RST标志位,可用来判断目标操作系统。

    - 关闭（Closed）：发送的数据包接收到的是一个RST/ACK数据包，即flags==0x14，通常意味着端口是关闭的
    ![ ](image\tcp-null关闭.JPG)
    - 开放（Open）：发送的数据包被丢弃，则说明端口可能是开放状态的
    ![ ](image\tcp-null开放.JPG)
    - 过滤（Filtered）：发送的数据包被丢弃，则说明端口可能是过滤状态的
    ![ ](image\tcp-null过滤.JPG)
6. UDP scan
UDP则是无连接的协议，则不会事先建立客户端和服务器之间的通信信道，只要客户端到服务器存在可用信道，就会假设目标是可达的然后向对方发送数据,向各个被扫描的UDP端口发送零字节的UDP数据包

    - 过滤（Filtered）：如果目标返回一个ICMP错误类型(type)3且代码(code)为1、2、9、10或13的数据包，则说明目标端口被服务器过滤了。但是如果服务器没有回复任何的UDP请求，则可以断定目标端口可能是过滤的
    - 开放（Open）：如果目标没有回复任何的UDP请求，则目标端口可能是开放的，如果返回一个UDP数据包，则可以断定目标端口是开放的。
    ![ ](image\udp开放.JPG)
    - 关闭（Closed）：如果目标返回了一个ICMP目标不可达的错误和代码(code)3，则意味着目标端口处于关闭状态
    ![ ](image\udp关闭.JPG)

## **六、实验问题**

1. 一开始在tcp connect scan过滤的验证中，代码没有考虑防火墙ICMP不可达错误的返回，直接按无响应处理，但是发现代码并没有显示出过滤结果，只提示收到了包  
 参考了丁辛夷同学的实验报告更改了代码，进行了抓包，发现即使是过滤也有type==3的ICMP包返回，没有搜到为什么呈现情况不是无响应，而将代码中的目标IP随意更改为内网不存在的IP，才得到了无响应包的结果，为什么iptables防火墙过滤后也会对TCP扫描返回ICMP不可到达(ICMP_PORT_UNREACHABLE)的错误，待查询
2. 如何停止nc的监听  
 目前只知道重启虚拟机一个方法，参考了丁辛夷同学的实验报告，知道可以用ps显示进程，可用kill杀死nc进程
3. UDP扫描在端口处于过滤状态仍然显示closed，说明目标代码(code)为3而不为1、2、9、10或13，不知道原因，待查询
