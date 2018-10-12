# coding=utf-8

from __future__ import print_function  # 将print语句替换为print函数
import logging
import time
from datetime import datetime
import threading
import random
import json
import config  # 获取并发时间


class Work(object):
    def __init__(self, open_id, gid, user_id, tcp_gate, rec_conduit, mahjong,desk_id_queue):
        self.tcp_gate = tcp_gate  # tcp client
        self.BEGIN = config.Initconf.BEGINSTR  # 并发开始时间
        self.rec_conduit = rec_conduit  # 接收服务器消息队列
        self.user_id = user_id  # 用户user_id
        self.open_id = open_id
        self.gid = gid
        self.mahjong = mahjong  # 麻将管理器
        self.rand_num = random.randint(1, 3)
        self.desk_id_queue = desk_id_queue


    #####################金币场#########################
    # 金币场报名
    def jinbi_join(self):
        # 请求加入金币场信息
        c2smsg = config.Initconf.send_join_jinbi
        self.tcp_gate.send_socket(c2smsg)
        logging.warning(str(self.open_id) + '-----------------开始报名金币场')
        counts = 0
        while True:
            s2cmsg_rce = self.rec_conduit.get()
            # logging.info("收到消息" + str(s2cmsg_rce))   # 打开日志查询错误
            self.is_rec_error(s2cmsg_rce)
            if s2cmsg_rce['m_msgId'] == config.Initconf.get_join_jinbi['m_msgId'] \
                    and s2cmsg_rce['m_errorCode'] == config.Initconf.get_join_jinbi['m_errorCode']:
                logging.warn(str(self.open_id) + '---------------报名金币场成功--------------')
                time.sleep(1)
                break
            counts += 1
            if counts >= 20:
                logging.warn(str(self.open_id) + '-----------报名金币场失败------------')
                return
    def is_rec_error(self, s2cmsg_rce):
        """
        判断响应的数据是否有误
        :param s2cmsg_rce:
        :return:
        """
        if 0 != int(s2cmsg_rce.get("m_errorCode", 0)) and 27 != int(s2cmsg_rce.get("m_msgId", 0)):
            logging.warn(str(self.open_id) + "----出现异常")
            logging.warn(str(self.open_id) + "rev----" + str(s2cmsg_rce))

    ###################比赛场####################
    # 比赛场报名
    def bisai_join(self):
        # 请求加入比赛场信息
        c2smsg = config.Initconf.send_join_bisai
        self.tcp_gate.send_socket(c2smsg)
        logging.warning(str(self.open_id) + '---------------开始报名比赛场')
        counts = 0
        while True:
            s2cmsg_rce = self.rec_conduit.get()
            # logging.info("收到消息" + str(s2cmsg_rce))   # 打开日志查询错误
            self.is_rec_error(s2cmsg_rce)
            if s2cmsg_rce['m_msgId'] == config.Initconf.get_join_bisai['m_msgId'] \
                    and s2cmsg_rce['m_errorCode'] == config.Initconf.get_join_bisai['m_errorCode']:
                logging.warn(str(self.open_id) + '---------------报名比赛场成功--------------')
                time.sleep(1)
                break
            counts += 1
            if counts >= 20:
                logging.warn(str(self.open_id) + '-----------报名比赛场失败------------')
                return

    def start_test(self,desk_id_queue):
        # 启动心跳
        keep = threading.Timer(4, self.tcp_gate.sendHeartbeat)
        keep.start()
        # 具体的测试内容
        # 定时触发脚本
        # while True:
        #     time.sleep(1)
        #     soss = str(datetime.now())
        #     ss = soss.split('.')
        #     if self.BEGIN in ss[0]:
        #         self.test_jinbi()
        #         break
        #self.jinbi_join()  # 金币场报名
        self.bisai_join()  # 比赛场报名
        time.sleep(2)
        self.tcp_gate.close_socket()
