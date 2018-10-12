# coding=utf-8
import logging
import sys
# 日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
# 设置日志的显示级别
LOG_LEVEL = logging.WARN

class Initconf(object):
    # -----------------------服务器相关--------------------------#
    IP = ('39.108.221.59', 8001)  # 测试服（用户中心登录ip）
    SERVERID = 13001
    FRAME = 2  # 1第一套架构 2为第二套 四川架构

    ########################机器人相关###########################
    # 机器人相关
    BEGINSTR = '2018'  # 开始并发的时间 #如果精确到分钟就那一分钟执行，精确到天就那一天执行
    RNUM = 20# 机器人个数
    # RSTART_ID = int(sys.argv[1])
    RSTART_ID = 200# 机器人起始id

    JUSTLOGIN = False # 是否只是登录 用于只是登录的一些需求 #用户测试只登陆的情况
    LOGINSPEED = 0.1  # 登录速度
    ISNEWUSER = False  # 是否使用新用户登录 #一般为false。

    ########################金币场相关信息#########################
    # 点击加入金币场  配置信息
    send_join_jinbi = {
        "m_curr_hp_id": 0,
        'm_location': "",
        'm_msgId': 324,
        'm_nMatchID': 2000004,    # 修改金币场matchid
        'm_nType': 0,
    }
    get_join_jinbi = {
        'm_errorCode': 0,
        'm_msgId': 325,
    }
    ########################比赛场相关信息#########################
    # 点击加入比赛场  配置信息
    send_join_bisai = {
        "m_curr_hp_id": 0,
        'm_location': "",
        'm_msgId': 324,
        'm_nMatchID': 2000079,

         # 修改比赛场matchid
        "m_nMatchType" : 2,
        'm_nType': 0,
    }
    get_join_bisai = {
        'm_errorCode': 0,
        'm_msgId': 325,
    }

class Login(object):
    """
    登录的配置信息
    """
    # ----用户中心的配置-------------
    # 用户登录的配置信息
    login_ip_port = "https://apitest.xianlaigame.com"
    login_url = login_ip_port + "/uc/v1/login/local"  # 公网
    login_params = {
        "appId": Initconf.SERVERID,  # int 项目appid，非游戏服务器ID
        "openId": "",  # str 玩家的openid
    }
    # 用户刷新token配置信息
    refresh_url = login_ip_port + "/uc/v1/token"
    refresh_params = {
        "gid": 1,  # int 由游戏编号和玩家id生成的玩家游戏ID
        "refreshToken": ""  # str 用户中心refreshtoken
    }



