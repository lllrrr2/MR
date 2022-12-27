'''
new Env('发财挖宝-助力');
export RabbitToken="token值"
export FCWB_HELP_CK_REVERSE="1 或 2 或 3"
export FCWB_HELP_HELP_PIN="1~3或pin1,pin2,pin3或者ALL"
export FCWB_HELP_MAX_HELP_NUM=30
export FCWB_HELP_READ_FILE_CK="默认false" # ck文件为ZNS_ZD_ck.txt，格式为一行一个ck

变量:
RabbitToken： 机器人给你发的token
FCWB_HELP_HELP_PIN：设置车头
FCWB_HELP_CK_REVERSE：1：正序，2：反序，3：乱序
FCWB_HELP_MAX_HELP_NUM：每个队伍的人数
FCWB_HELP_READ_FILE_CK：读取ck文件，默认false，ck文件为ZNS_ZD_ck.txt，格式为一行一个ck

log剩余次数大于5000方可使用
'''

from utils.common import UserClass, printf, print_api_error, print_trace, TaskClass

linkId = "pTTvJeSTrpthgk9ASBVGsw"


class FcwbUserClass(UserClass):
    def __init__(self, cookie):
        super(FcwbUserClass, self).__init__(cookie)
        self.curRound = ""
        self.inviteCode = ""
        self.inviter = ""
        self.blood = ""
        self._help_num = None
        self.UA = self.lite_UA
        self.Origin = "https://bnzf.jd.com"
        self.referer = "https://bnzf.jd.com/?activityId=pTTvJeSTrpthgk9ASBVGsw&inviterId=&inviterCode=&utm_user=plusmember&ad_od=share&utm_source=androidapp&utm_medium=appshare&utm_campaign=t_335139774&utm_term=Wxfriends&lng=106.477132&lat=29.502772&sid=84c83c76030880654e4e98b6bcda688w&un_area=4_50952_106_0"

    def init(self):
        self.ua = self.default_jsb_ua
        headers = {
            "Cookie": self.cookie,
            "User-Agent": self.ua,
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://bnzf.jd.com",
            "referer": "https://bnzf.jd.com/?activityId=pTTvJeSTrpthgk9ASBVGsw&inviterId=&inviterCode=&utm_user=plusmember&ad_od=share&utm_source=androidapp&utm_medium=appshare&utm_campaign=t_335139774&utm_term=Wxfriends&lng=106.477132&lat=29.502772&sid=84c83c76030880654e4e98b6bcda688w&un_area=4_50952_106_0"
        }
        self.headers = headers

    def opt(self, opt):
        _opt = {
            "method": "get",
            "client": "ios",
            "clientVersion": "3.9.0",
            "appid": "activities_platform",
            "h5st": True,
        }
        _opt.update(opt)
        return _opt

    def home(self):
        body = {
            "linkId": linkId
        }
        opt = {
            "functionId": "happyDigHome",
            "body": body,
            "appId": "ce6c2",
        }
        status, res_data = self.jd_api(self.opt(opt))
        if res_data.get('code') == 0:
            pass
        else:
            self.black = True
            self.valid = False
            self.can_help = False

    @property
    def help_num(self):
        if self._help_num == None:
            body = {
                "pageNum": 1,
                "pageSize": 50,
                "linkId": linkId
            }
            opt = {
                "functionId": "happyDigHelpList",
                "body": body,
                "appId": "ce6c2",
            }
            status, data = self.jd_api(self.opt(opt))
            if status == 200:
                if data["success"]:
                    pass
                    self._help_num = data['data'].get('personNum', 0)
                else:
                    self._help_num = 0
                    self.black = True
            else:
                self._help_num = 0
                print_api_error(opt, status)
                self.black = True
        return self._help_num

    @help_num.setter
    def help_num(self, value):
        self._help_num = value

    def get_invite_code(self):
        body = {
            "linkId": linkId
        }
        opt = {
            "functionId": "happyDigHome",
            "body": body,
            "appId": "ce6c2",
        }
        status, res_data = self.jd_api(self.opt(opt))
        if res_data.get('success'):
            self.curRound = res_data['data']['curRound']
            self.inviteCode = res_data['data']['inviteCode']
            self.inviter = res_data['data']['markedPin']
            self.blood = res_data['data']['blood']
            printf(f"[{self.Name}]【助力码】:\t{res_data['data']['inviteCode']}")
        else:
            self.black = True

    def help(self, inviter):
        try:
            if inviter.help_num >= inviter.MAX_HELP_NUM:
                inviter.need_help = False
                printf(f"车头[{inviter.Name}]\t 助力已满({inviter.help_num}/{inviter.MAX_HELP_NUM})")
                return
            self.home()
            body = {
                "inviter": inviter.inviter,
                "inviteCode": inviter.inviteCode,
                "linkId": linkId,
            }
            opt = {
                "functionId": "happyDigHelp",
                "body": body,
                "appId": "8dd95",
            }
            status, res_data = self.jd_api(self.opt(opt))
            code = str(res_data.get('code', status))
            if code == '0':
                inviter.help_num += 1
                self.can_help = False
                printf(f"\t助力[{inviter.Name}]成功, 已邀请: {inviter.help_num}/{inviter.MAX_HELP_NUM}")
            else:
                msg = res_data.get("errMsg", "")
                if '未登录' in msg:
                    self.valid = False
                    self.can_help = False
                elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                    self.can_help = False
                    self.black = True
                printf(f"\t助力失败[{code}]: {msg}")
        except:
            print_trace()


if __name__ == '__main__':
    task = TaskClass("invite")
    task.MAX_HELP_NUM = 60
    task.name = 'FCWB_HELP'
    task.init_config(FcwbUserClass)
    task.main("发财挖宝-助力")
