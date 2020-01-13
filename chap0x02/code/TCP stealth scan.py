#!/usr/bin/python
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  #设置logger用于记录错误
from scapy.layers.inet import IP,UDP, TCP, ICMP
from scapy.all import sr,sr1,RandShort

dst_ip = "172.16.111.144"
src_port = RandShort()
dst_port=80

pkt=IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="S")  # 构建SYN数据包
tcp_stealth_scan_resp = sr1(pkt,timeout=10)  # 发送1个SYN数据包，此变量是接收包
if(str(type(tcp_stealth_scan_resp))=="<type 'NoneType'>"):
    print("Filtered or non-existent")  # 无响应，说明端口处于过滤状态或者目标主机关闭/不存在
elif(tcp_stealth_scan_resp.haslayer(TCP)):
    if(tcp_stealth_scan_resp.getlayer(TCP).flags == 0x12):
        send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="R"),timeout=10)
        print("Open")
    elif (tcp_stealth_scan_resp.getlayer(TCP).flags == 0x14):
        print("Closed")
elif(tcp_stealth_scan_resp.haslayer(ICMP)):
    if(int(tcp_stealth_scan_resp.getlayer(ICMP).type)==3 and int(tcp_stealth_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
        print ("Filtered")