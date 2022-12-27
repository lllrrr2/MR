'''
new Env('炸年兽-组队');
export RabbitToken="token值"
export ZNS_ZD_CK_REVERSE="1 或 2 或 3"
export ZNS_ZD_HELP_PIN="1~3或pin1,pin2,pin3或者ALL"
export ZNS_ZD_MAX_HELP_NUM=30
export ZNS_ZD_READ_FILE_CK="默认false" # ck文件为ZNS_ZD_ck.txt，格式为一行一个ck

变量:
RabbitToken： 机器人给你发的token
ZNS_ZD_HELP_PIN：设置车头
ZNS_ZD_CK_REVERSE：1：正序，2：反序，3：乱序
ZNS_ZD_MAX_HELP_NUM：每个队伍的人数
ZNS_ZD_READ_FILE_CK：读取ck文件，默认false，ck文件为ZNS_ZD_ck.txt，格式为一行一个ck

log剩余次数大于5000方可使用
'''
import json

from utils.common import UserClass, printf, print_api_error, print_trace, TaskClass


class ZnsZDUserClass(UserClass):
    def __init__(self, cookie):
        super(ZnsZDUserClass, self).__init__(cookie)
        self.inviteCode = ""
        self.force_app_ck = True
        self.appname = "50174"
        self._help_num = None
        self.Origin = "https://h5.m.jd.com"
        self.referer = "https://h5.m.jd.com/"

    def opt(self, opt):
        self.set_joyytoken()
        self.set_shshshfpb()
        _opt = {
            "method": "post",
            "log": True,
            "params": {
                "appid": "signed_wh5",
                "client": "m",
                "clientVersion": "-1",
                "osVersion": "-1",
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

    @property
    def help_num(self):
        if self._help_num == None:
            self._help_num = 0
        return self._help_num

    @help_num.setter
    def help_num(self, value):
        self._help_num = value

    def get_invite_code(self):
        try:
            body = {}
            opt = {
                "functionId": "promote_pk_getHomeData",
                "body": body,
                "need_log": False
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    self.help_num = result['data']['result']['groupInfo']['groupNum']
                    self.inviteCode = result['data']['result']['groupInfo']['groupJoinInviteId']
                    self.printf(f"【当前队伍】: \t{result['data']['result']['groupInfo']['groupName']}")
                    self.printf(f"【助力码】: \t{self.inviteCode}")
                    self.need_help = True
                else:
                    self.need_help = False
                    print_api_error(opt, status)
                    print(result)
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(f"{msg}")
        except:
            self.need_help = False
            print_trace()

    def help(self, inviter):
        try:
            if inviter.help_num >= inviter.MAX_HELP_NUM:
                inviter.need_help = False
                printf(f"车头[{inviter.Name}]\t 助力已满({inviter.help_num}/{inviter.MAX_HELP_NUM})")
                return
            body = {
                "actionType": 0,
                "inviteId": inviter.inviteCode,
            }
            opt = {
                "functionId": "promote_pk_joinGroup",
                "body": body,
            }
            status, res_data = self.jd_api(self.opt(opt))
            code = res_data['code']
            if code == 0:
                if res_data['data'].get("bizCode") == 0:
                    inviter.help_num += 1
                    self.printf(f"助力[{inviter.Name}]成功({inviter.help_num}/{inviter.MAX_HELP_NUM})")
                else:
                    msg = res_data['data'].get("bizMsg", "")
                    if '未登录' in msg:
                        self.valid = False
                        self.can_help = False
                    elif '已经有团队' in msg:
                        self.can_help = False
                    elif '火爆' in msg:
                        self.can_help = False
                    elif '邀请过' in msg:
                        pass
                    elif '满员' in msg:
                        inviter.need_help = False
                    self.printf(f"助力失败[{code}]: {msg}")
            else:
                msg = res_data['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                self.printf(f"\t{msg}")
        except:
            print_trace()


if __name__ == '__main__':
    task = TaskClass("help")
    task.MAX_HELP_NUM = 30
    task.name = 'ZNS_ZD'
    task.init_config(ZnsZDUserClass)
    task.main("炸年兽-组队")
