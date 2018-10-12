# coding=utf-8

import multiprocessing
from multiprocessing import Queue
import user
import time
import logging
import config
import sys

# 老用户从外部获取登录的起始值
# config.Robot.robot_start_id = int(sys.argv[1])


class MyLog(object):
    """
    设置log输出的格式
    """
    def __init__(self):
        # 日志的输出格式
        formatter = logging.Formatter('p:%(process)d %(filename)s l:%(lineno)d  %(asctime)s  %(message)s')
        # formatter = logging.Formatter('%(message)s')
        logger = logging.getLogger()
        # 设置日志的级别
        logger.setLevel(config.LOG_LEVEL)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)


def playstart(r_id,desk_id_queue):
    """
    创建玩家登录和进行测试
    :param r_id:机器人id
    :return:
    """
    # 创建玩家对象
    player = user.GamePlayer(r_id, desk_id_queue)
    # 玩家进行登录
    player.entry()
    # 完成登录，进行测试

class Controller(object):
    def __init__(self):
        # 进程间通信，存储桌子号的消息队列
        self.desk_id_queue = Queue()


    def controller(self):
        """
        负载控制器
        使用多进程创建机器人
        """
        # config.Initconf.RUNTYPE == 2
        index = 0
        while True:
            for r_id in range(config.Initconf.RSTART_ID, (config.Initconf.RSTART_ID + config.Initconf.RNUM)):
            # for r_id in range(config.Robot.robot_start_id, (config.Robot.robot_start_id + config.Robot.robot_num)):
                index += 1
                # 创建进程对象
                start_player = multiprocessing.Process(target=playstart, args=(r_id, self.desk_id_queue))
                # 启动进程
                start_player.start()
                # 设置进程创建启动间隔时间
                time.sleep(config.Initconf.LOGINSPEED)
            if index == config.Initconf.RNUM:
                # logging.info("登录结束")
                break




if __name__ == '__main__':
    # 设置log对象
    log = MyLog()
    # 启动压载器
    start_test = Controller()
    start_test.controller()



