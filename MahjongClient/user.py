# coding=utf-8
import msgpack
import socket
import hashlib
import Queue
import threading
import time
import struct
import logging
import json
import requests
import config  # 配置信息
from work import Work  # 测试逻辑

# 禁用安全请求警告
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Mahjong(object):
    """
    麻将管理器，打牌逻辑需要使用
    """
    def __init__(self):
        self._my_pos = None  # 玩家位置
        self._my_card = None
        self._my_ting = False
        self._my_state = None
        self._my_type = None
        self._my_que = False
        self._my_tang = False

    def set_card(self, card):  # 初始化手牌
        self._my_card = card

    def pop_card(self, p_card):  # 删除手牌
        self._my_card.remove(p_card)
        self._my_card.sort()

    def add_card(self, a_card):  # 添加手牌
        self._my_card.append(a_card)

    def set_ting(self, boolean):
        self._my_ting = boolean

    def set_que(self, boolean):
        self._my_que = boolean

    def set_play_state(self, num):
        self._my_state = num

    def set_pos(self, _pos):  # 初始化位置
        self._my_pos = _pos

    def set_play_type(self, playtype):
        self._my_type = playtype

    def set_tang(self, boolean):
        self._my_tang = boolean

    def get_card(self):
        return self._my_card

    def get_pos(self):
        return self._my_pos

    def get_play_state(self):
        return self._my_state

    def get_ting(self):
        return self._my_ting

    def get_que(self):
        return self._my_que

    def get_play_type(self):
        return self._my_type

    def get_tang(self):
        return self._my_tang


class TCPClient(object):
    """
    TCP长连接对象
    """
    @staticmethod
    def head_pack(heard_msg):
        tm = int(time.time())
        heard = {
            "len": len(heard_msg),
            "check_sum": 100,
            "tm": tm,
            "msgid": 1 * (tm % 10000 + 1)
        }
        # 把任意数据类型转换为bytes
        messaged = struct.pack("HHII", heard['len'], heard['check_sum'], heard['tm'], heard['msgid'])
        return messaged

    def __init__(self):
        # 创建一个tcp客户端
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置超时时间
        self._socket.settimeout(10)
        self.flag_bit = 0

    def set_socket(self, _addrs):
        """
        与服务器建立连接
        :param _addrs: 服务器IP+port
        :return:
        """
        self._socket.connect(_addrs)

    def send_socket(self, msg):
        """"
        对发送的消息体进行打包
        发送打包后的 msg_date 和 msg_head bytes对象
        """
        # 消息处理后发送
        # packb方法 把一个dict封装为一个bytes对象
        msg_date = msgpack.packb(msg)
        # 发送消息的结构信息的bytes对象
        msg_head = self.head_pack(msg_date)
        time.sleep(0.1)
        self._socket.send(msg_head)
        self._socket.send(msg_date)
        # logging.warning('send--' + str(msg))

    def rec_socket_Login(self, _rec_queue):
        while 1:
            _rec = self._socket.recv(1024)
            if _rec:
                # 对bytes对象进行解析，并去除前12个
                _rec_msg = msgpack.unpackb(_rec[12:])
                # logging.warning(_rec_msg)
                _rec_queue.put(_rec_msg)
                break
                # 接收数据包处理

    def rec_socket_gate(self, _rec_queue):
        # 定义一个空的字节数组
        bodybuffer = bytes()
        # 死循环收消息
        while 1:
            if self.flag_bit == 0:
                try:
                    # 阻塞接收数据
                    _rec = self._socket.recv(1024)
                    if _rec:
                        bodybuffer += _rec
                        while 1:
                            if len(bodybuffer) < 12:
                                break
                            # 获取消息头信息
                            aa = struct.unpack('HHII', bodybuffer[:12])
                            # 获取消息的长度信息
                            bodysize = aa[0]
                            if len(bodybuffer) < 12 + bodysize:
                                break
                            # 获取消息体的内容
                            body = bodybuffer[12:12 + bodysize]

                            try:
                                # 解包消息体
                                _rec_msg = msgpack.unpackb(body)
                                # logging.info('recv--' + str(_rec_msg))
                                _rec_queue.put(_rec_msg)
                            except:
                                print("解析失败 ")
                            finally:
                                # 置空消息体
                                bodybuffer = bodybuffer[12 + bodysize:]
                except socket.timeout:
                    logging.info('断开连接')
                    self.setfig()
            else:
                break

    def close_socket(self):
        self._socket.close()

    def setfig(self):
        self.flag_bit = 2

    def sendHeartbeat(self):
        global keep
        C_2_S_msg = {
            'm_msgId': 15
        }
        self.send_socket(C_2_S_msg)
        logging.debug('发送心跳包')
        keep = threading.Timer(3, self.sendHeartbeat)
        keep.start()


def request(login_url, login_params, open_id):
    """
    登录/注册用户中心，用户不存在，是注册，存在，是登录。
    :return:
    """
    # 更新open_id
    login_params["openId"] = open_id
    # 公有API需要携带以下自定义头部，私有API无需携带。
    headers = {
        "X-QP-AppId": "13001",  # str 客户端（应用包）的唯一标识, 询问开发
        "X-QP-Timestamp": str(int(time.time())),  # str 请求的时间戳，值为当前时间的秒数
        "X-QP-Nonce": str(int(time.time()) * 1000),  # str 请求唯一标识。暂时为时间戳值, 毫秒数
    }
    sign = signature(params=headers, method="GET", url=login_url, data=login_params)
    headers["X-QP-Signature"] = sign
    requests.packages.urllib3.disable_warnings()   # 禁用安全请求警告
    res = requests.get(url=login_url, params=login_params, verify=False, headers=headers)
    return res


def refresh_token(user_info):
    """
    刷新用户的token
    :return:
    """
    login_ip_port = "https://apitest.xianlaigame.com"
    # login_ip_port = "https://120.25.201.130:88"
    login_url = login_ip_port + "/uc/v1/token"  # 公网
    login_params = {
        "gid": user_info["gid"],  # int 由游戏编号和玩家id生成的玩家游戏ID
        "refreshToken": user_info["token"],  # str 用户中心refreshtoken
    }
    # 公有API需要携带以下自定义头部，私有API无需携带。
    headers = {
        "X-QP-AppId": "13001",  # str 客户端（应用包）的唯一标识, 询问开发
        "X-QP-Timestamp": str(int(time.time())),   # str 请求的时间戳，值为当前时间的秒数
        "X-QP-Nonce": str(int(time.time())*1000),   # str 请求唯一标识。暂时为时间戳值, 毫秒数
    }
    sign = signature(params=headers, method="GET", url=login_url)
    headers["X-QP-Signature"] = sign
    headers["X-QP-Gid"] = str(user_info["gid"])
    headers["X-QP-Token"] = user_info["token"]
    requests.packages.urllib3.disable_warnings()   # 禁用安全请求警告
    res = requests.get(url=login_url, params=login_params, verify=False, headers=headers)
    return res

def format_str(params, symbol, join_str):
    src_str = join_str.join(
        k + symbol + str(params[k]) for k in sorted(params.keys()))
    return src_str


def signature(params, method, url, data=None):
    """
    获取请求签名
    :param params:  请求头
    :param method:
    :param url:
    :param data: 请求查询参数
    :return:
    """
    headers_str = format_str(params=params, symbol=":", join_str="")
    data_str = format_str(params=data, symbol="=", join_str="&")
    sign_str = str(method).upper() + headers_str + url + "?" + data_str + "3c6e0b8a9c15224a8228b9a98ca1531d"
    return sign_md5(sign_str)

def sign_md5(sign_str):
    """
    对签名进行md5加密
    String sign = MD5(strToSign)
    :param sign_str:
    :return:
    """
    hash_md5 = hashlib.md5()
    # hash_md5.update(str(sign_str).encode("utf-8"))  # py3
    hash_md5.update(sign_str)  # py2
    sign = hash_md5.hexdigest()
    return sign


class GamePlayer(object):
    """
    玩家类
    """
    def __init__(self, r_id,desk_id_queue):
        """
        初始化玩家类
        :param r_id: 玩家的open_id
        """
        self.open_id = r_id  # 玩家的open_id
        # self.addr = config.Gate_conf.gate_addr  # gate服务器的地址
        self.addr = config.Initconf.IP  # gate服务器的地址
        self.tcp_gate = TCPClient()  # gate TCP客户端
        self.rec_conduit = Queue.Queue()  # 接收服务器消息队列
        self.mahjong = Mahjong()  # 麻将管理器,处理打牌逻辑
        self.login_url = config.Login.login_url  # 用户中心的请求url
        self.login_params = config.Login.login_params  # 用户中心的查询参数
        self.desk_id_queue = desk_id_queue


    def login_user_center(self):
        """
        登录用户中心，获取登录信息
        :return: user_info
        """
        response = request(self.login_url, self.login_params, self.open_id)
        if 200 == response.status_code and 0 == response.json()["errCode"]:
            logging.info(str(self.login_params["openId"]) + "-----用户中心----登录成功")
            user_info = {
                "accessToken": response.json()["data"]["accessToken"],
                "gid": response.json()["data"]["gid"],
                "userId": response.json()["data"]["userId"],
                "refreshToken": response.json()["data"]["refreshToken"],
            }
            # logging.error(user_info['gid'])    # 获取用户userid
            return user_info
        else:
            logging.info("用户中心登录失败, 失败原因，errCode:{errCode}, errDesc:{errDesc}".format(
                errCode=response.json()["errCode"],
                errDesc=response.json()["errDesc"]
            ))

    def token_update(self, user_info):
        """
        刷新token信息
        :param user_info:
        :return:
        """
        response = refresh_token(user_info)
        if 200 == response.status_code and 0 == response.json()["errCode"]:
            print json.dumps(response.json(), ensure_ascii=False, indent=4)
            user_info["token"] = response.json()["data"]["accessToken"]
            return user_info
        else:
            logging.info("刷新token失败, 失败原因，errCode:{errCode}, errDesc:{errDesc}".format(
                errCode=response.json()["errCode"],
                errDesc=response.json()["errDesc"]
            ))

    def entry(self):
        """
        进行登录及执行测试
        :return:
        """
        # 连接用户中心
        user_info = self.login_user_center()
        # 连接gate_server
        self.tcp_gate.set_socket(self.addr)
        # 1. 发送8号消息
        c2s_msg_8 = {
            'm_msgId': 8,  # int
            "m_userId": user_info["gid"],  # int
            # "m_gid": user_info["gid"],  # int
            "m_accessToken": user_info["accessToken"],  # str
        }
        self.tcp_gate.send_socket(c2s_msg_8)
        # print(c2s_msg_8)
        logging.info("发送完成8号消息")
        # 启用消息队列接收消息
        s2c_rec = threading.Thread(target=self.tcp_gate.rec_socket_gate, args=(self.rec_conduit,))
        s2c_rec.setDaemon(True)
        s2c_rec.start()

        # 2. 收到9号消息 获取新的token
        s2c_msg_9 = self.rec_conduit.get()
        if 9 == s2c_msg_9["m_msgId"] and 0 == s2c_msg_9["m_errCode"]:
            # logging.info("收到9号消息:{msg}".format(msg=s2c_msg_9))
            logging.info("收到9号消息")
        else:
            logging.info("收到9号消息有误:{msg}".format(msg=s2c_msg_9))

        # 3. 发送11号消息登录
        c2s_msg_11 = {
            'm_nAppId': config.Initconf.SERVERID,  # int
            'm_id': user_info["gid"],  # int
            'm_md5': "",
            'm_msgId': 11,  # int
            'm_seed': 0
        }
        self.tcp_gate.send_socket(c2s_msg_11)
        logging.warning(str(self.open_id) + '------------号用户登录完成！')

        if not config.Initconf.JUSTLOGIN:
            worker = Work(self.open_id, user_info["gid"], user_info["userId"], self.tcp_gate, self.rec_conduit, self.mahjong,self.desk_id_queue)
            # 测试逻辑
            worker.start_test(self.desk_id_queue)

