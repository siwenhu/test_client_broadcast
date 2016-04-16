# -*- coding: utf-8 -*-
import platform

#系统类型
SYSTYPE = platform.system()

#配置文件的路径
#CONFIG_PATH = "/usr/massclouds/vdi/client/cfg/cdesktop.conf"
CONFIG_PATH = "/opt/ccr-student/cfg/cdesktop.conf"

#日志文件的路径
LOG_PATH = "/opt/morningcloud/massclouds/record.log"

#UBUNTU网络配置文件
NETWORK_CONFIG_UBUNTU = "/etc/network/interfaces"

#CENTOS 6.5配置文件
NETWORK_CONFIG_CENTOS_6_5 = "/etc/sysconfig/network-scripts/ifcfg-eno16777736"

#CENTOS 7.0配置文件
NETWORK_CONFIG_CENTOS_7_0 = "/etc/sysconfig/network-scripts/ifcfg-"

#CENTOS 7.0配置文件
BRIDGER_NETWORK_CONFIG_CENTOS_7_0 = "/etc/sysconfig/network-scripts/ifcfg-br0"

#默认网卡的名称
DEFAULT_NETCARD_NAME = "eno16777736"

#虚拟机数量上限
UPLIMIT = 200

#云主机的用户名和密码
auth = ('root', 'root+-*/root')
#auth = ('root', 'rootroot')

#滚动的类型
SCROLL_TYPE = "slidera"

#tcp监听的端口
SOCKET_PROT = 6001

#广播的监听端口
BROAD_CAST_PORT = 6666

#默认的分辨率
defaultResolution = "1024x768"

#发送request请求的头部
headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 
        'Accept-Encoding': 'gzip, deflate', 
        'X-Requested-With': 'XMLHttpRequest', 
        'Content-Type': 'application/json', 
        'Accept-Language': 'en-US,en;q=0.5', 
        'Cookie': 'username=root; kimchiLang=zh_CN', 
        'X-Requested-With': 'XMLHttpRequest' 
        } 


#系统图片映射
imageMap = {"Windows XP":"windows_xp.png",
            "Windows 7":"windows_7.png",
            "Windows 7 x64":"windows_7x64.png",
            "Windows 8":"windows_8.png",
            "Windows 8 x64":"windows_8x64.png",
            "CentOS" :"centos_6.png",
            "Ubuntu":"ubuntu_12_10.png",
            "RedHat":"rhel_6.png",
            "Linux":"other_linux.png",
            "Red Hat Enterprise Linux":"rhel_6.png",
            "Red Hat Enterprise Linux x64":"rhel_6x64.png",
            "SUSE Linux Enterprise Server 11":"sles_11.png",
            "Ubuntu x64":"ubuntu_12_10.png",
            "Windows 2003":"windows_2003.png",
            "Windows 2003 x64":"windows_2003x64.png",
            "Windows 2008":"windows_2008.png",
            "Windows 2008 R2 x64" : "windows_2008R2x64.png",
            "Windows 2008 x64":"windows_2008x64.png",
            "Windows 2012 x64":"other.png",
            "Other OS":"other.png"
            }


#开发环境类型
DEVELOPED_ENV_TYPE = 0

#执行环境类型
OPERATION_ENV_TYPE = 1

