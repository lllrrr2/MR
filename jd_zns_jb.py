'''
new Env('炸年兽-金币收集');
export RabbitToken="token值"
export ZNS_CK_REVERSE="1 或 2 或 3"
export ZNS_HELP_PIN="1~3或pin1,pin2,pin3或者ALL"
export ZNS_MAX_HELP_NUM=30
export ZNS_READ_FILE_CK="默认false" # ck文件为ZNS_ZD_ck.txt，格式为一行一个ck

变量:
RabbitToken： 机器人给你发的token
ZNS_HELP_PIN：设置车头
ZNS_CK_REVERSE：1：正序，2：反序，3：乱序
ZNS_MAX_HELP_NUM：每个队伍的人数
ZNS_READ_FILE_CK：读取ck文件，默认false，ck文件为ZNS_ZD_ck.txt，格式为一行一个ck

log剩余次数大于5000方可使用
'''
import json

from utils.common import UserClass, print_trace, print_api_error, printf, wait, randomWait, TaskClass


class ZnsUserClass(UserClass):
    def __init__(self, cookie):
        super(ZnsUserClass, self).__init__(cookie)
        self.force_app_ck = True
        self.appname = "50174"
        self._help_num = None
        self.maxLevel = False
        self.secretpInfo = {}
        self.secretp = ""
        self.homeData = {}
        self.homeMainInfo = {}
        self.raiseInfo = {}
        self.signHomeData = {}
        self.taskList = []
        self.lotteryTaskVos = []
        self.fullFlag = False
        self.toTaskFlag = False
        self.Origin = "https://wbbny.m.jd.com"
        self.referer = "https://wbbny.m.jd.com/"

    def opt(self, opt):
        self.set_joyytoken()
        self.set_shshshfpb()
        _opt = {
            "method": "post",
            "log": False,
            "api": "client.action",
            "body_param": {
                "appid": "signed_wh5",
                "client": "m",
                "clientVersion": "-1",
                "functionId": opt['functionId']
            }
        }
        _opt.update(opt)
        return _opt

    def log_format(self, body, log_data):
        body.update({"log": log_data["log"]})
        body.update({"random": log_data["random"]})
        # body = f"body={json.dumps(body, separators=(',', ':'))}"
        body = {
            "body": json.dumps(body, separators=(',', ':'))
        }
        return body

    def promote_getHomeData(self):
        try:
            opt = {
                "functionId": "promote_getHomeData"
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    self.homeData = result['data']
                    self.secretp = result['data']['result']['homeMainInfo']['secretp']
                    self.secretpInfo[self.pt_pin] = self.secretp
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(f"{msg}")
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                    self.black = True
                self.printf(f"{msg}")
        except:
            print_trace()

    def promote_collectAutoScore(self):
        try:
            body = {}
            opt = {
                "functionId": "promote_collectAutoScore",
                "body": body,
                "log": True
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    self.printf(f"收取成功，获得：{result['data']['result']['produceScore']}")
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(msg)
            else:
                print(result)
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(msg)
        except:
            print_trace()

    def main(self):
        self.promote_getHomeData()
        if self.black:
            return
        self.promote_collectAutoScore()


if __name__ == '__main__':
    task = TaskClass("task")
    task.name = 'ZNS'
    task.init_config(ZnsUserClass)
    task.main("炸年兽-金币收集")
