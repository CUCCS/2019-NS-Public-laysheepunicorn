# **Web应用漏洞攻防**

## **一、实验目的**

- 了解常见Web漏洞训练平台；
- 了解 常见Web漏洞的基本原理；
- 掌握 OWASP Top 10及常见Web高危漏洞的漏洞检测、漏洞利用和漏洞修复方法。

## **二、实验环境**

- WebGoat
- Juice Shop

## **三、实验要求**

- 每个实验环境完成不少于5种不同漏洞类型的漏洞利用练习

## **四、实验原理及过程**

## **（一）WebGoat环境的漏洞实验**

1. 环境搭建
    - 使用apt update && apt install docker-compose命令安装docker-compose
        - docker是一种容器技术，作用是用来快速部署服务
        - docker-compose 是一个用户定义和运行多个容器的Docker应用程序。在Compose中你可以使用YAML文件来配置你的应用服务。然后，只需要一个简单的命令，就可以创建并启动你配置的所有服务。
    - git clone <https://github.com/c4pr1c3/ctf-games.git> --recursive  
    使用老师的包安装WebGoat
    - cd ctf-games/owasp/webgoat/  
    进入webgoat所在文件夹
    - service docker restart  
    为了保证不报错再次启动docker-compose
    - docker-compose up -d  
    使用此命令安装和开启WebGoat7.0、8.0
    ![ ](image\安装webgoat.JPG)
    - docker ps查看访问端口及状态，可得7.0通过8087端口进入，8.0通过8088端口进入
    ![ ](image\查看webgoat端口状况.JPG)
    - WebGoat的开启过程
    ![ ](image\webgoat的启动.JPG)
    - 开启WebGoat的界面  
    7.0
    ![ ](image\webgoat7.0界面.JPG)
    8.0
    ![ ](image\webgoat8.0结果是8088端口.JPG)

2. 进行的漏洞实验
    - 缓冲区溢出(Buffer Overflows->Off-by-One Overflows)
        - 原理：向程序输入缓冲区写入使之溢出的内容（通常是超过缓冲区能保存的最大数据量的数据），从而破坏程序运行、趁著中断之际并获取程序乃至系统的控制权。
        - 主要操作方法：将过量的输入数据插入到可修改的注入向量中来溢出缓冲区
        - 实验实现：
            - 目的：我们需要找出已在旅店中已注册VIP客户的姓名房号，使用客户的信息登入系统
            - 方法：使用Burpsuite拦截http-post包大量向其缓冲区中写入数据使隐藏的客户信息因为错误暴露
            - 环境：WebGoat8.0
            - 过程：
            1. 需要登记用户的First Name，Last Name以及Room Number，随意填入数据，点击Submit提交即可。
            2. 需要确认住宿的时间。查看网页源代码，发现在之前中输入的3个参数是hidden input方式。
            3. 选择$9.99 - 24hours选项，点击Accept Terms按钮。
            4. 此时使用Burp拦截GET请求报文。
            5. 将GET请求报文发送到intruder中，设置Attack type为Sniper，分别将last_name，first_name和room_no设置为payload的位置，Payload type选择Character blocks模式，Payload选项随意选择了一个字符2，最小长度为1，最大长度为10000，步长设置为1000。
            6. 开始攻击。攻击后选择最长的查看信息，房间号room_no可以使得程序发生Buffer Overflow错误，从而获取VIP的房间信息。
            7. 将获取到的VIP房间信息填写到输入框中，点击Submit通过实验。
                ![ ](image\缓冲区溢出成功.JPG)
    - 未验证的用户输入
        - 作为攻击者，可以对 HTTP 请求的任何一个部分进行篡改，例如：URL、请求字符串、HTTP 请求头、Cookies、表单域、隐藏域，从而获得对客户端缓存、Cookie、请求编码等的控制，进而实现丰富灵活的 Web 攻击手段。
        - 实验实现：
            - 目的：突破页面检查
            - 方法：提交表单使用Brupsuite使用拦截改掉相关字段，因为相关字段有一定的限制，超出限制就会跳过检查
            - 环境：WebGoat8.0
            - 过程：
            1. 直接点击submit，但是使用burpsuite拦截包，观察到有四个主要字段
                ![ ](image\未验证的用户输入-burp.JPG)
            2. 在burp内任意更改字段的值后forward 
                ![ ](image\未验证的用户输入-forward.JPG)
            3. 实验成功
                ![ ](image\未验证的用户输入成功.JPG)
