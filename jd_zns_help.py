'''
new Env('炸年兽-助力');
export RabbitToken="token值"
export ZNS_HELP_CK_REVERSE="0 或 1 或 2"
export ZNS_HELP_HELP_PIN="1~3或pin1,pin2,pin3或者ALL"
export ZNS_HELP_MAX_HELP_NUM=8
export ZNS_HELP_READ_FILE_CK="默认false" # ck文件为ZNS_HELP_ck.txt，格式为一行一个ck

变量:
RabbitToken： 机器人给你发的token
ZNS_HELP_HELP_PIN：设置车头
ZNS_HELP_CK_REVERSE：0：正序，1：反序，2：乱序
ZNS_HELP_MAX_HELP_NUM：最大助力数
ZNS_HELP_READ_FILE_CK：读取ck文件，默认false，ck文件为ZNS_HELP_ck.txt，格式为一行一个ck

log剩余次数大于5000方可使用
'''
from utils.common import UserClass, printf, print_api_error, print_trace, TaskClass


class ZnsHelpUserClass(UserClass):
    def __init__(self, cookie):
        super(ZnsHelpUserClass, self).__init__(cookie)
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
                "functionId": "promote_getTaskDetail",
                "body": body,
                "need_log": False
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    self.help_num = result['data']['result']['taskVos'][0]['times']
                    self.inviteCode = result['data']['result']['inviteId']
                    printf(f"{self.Name}【助力码】: \t{self.inviteCode}")
                else:
                    msg = result['data'].get("bizMsg", "")
                    if '未登录' in msg:
                        self.valid = False
                        self.can_help = False
                    elif '助力次数用完啦' in msg:
                        self.can_help = False
                    elif '火爆' in msg:
                        self.need_help = False
                        self.can_help = False
                    elif '邀请过' in msg:
                        pass
                    elif '好友人气爆棚了' in msg:
                        self.can_help = False
                    print_api_error(opt, status)
                    print(result)
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                printf(F"[{self.Name}]\t{msg}")
        except:
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
                "functionId": "promote_collectScore",
                "body": body,
            }
            status, res_data = self.jd_api(self.opt(opt))
            code = res_data['code']
            if code == 0:
                if res_data['data'].get("bizCode") == 0:
                    inviter.help_num += 1
                    printf(f"\t助力[{inviter.Name}]成功, 已邀请: {inviter.help_num}/{inviter.MAX_HELP_NUM}")
                else:
                    msg = res_data['data'].get("bizMsg", "")
                    if '未登录' in msg:
                        self.valid = False
                        self.can_help = False
                    elif '次数用完啦' in msg:
                        self.can_help = False
                    elif '火爆' in msg:
                        pass
                    elif '邀请过' in msg:
                        pass
                    elif '好友人气爆棚了' in msg:
                        inviter.need_help = False
                    printf(f"\t助力失败[{code}]: {msg}")
            else:
                msg = res_data['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                printf(F"[{self.Name}]\t{msg}")
        except:
            print_trace()


if __name__ == '__main__':
    task = TaskClass("help")
    task.MAX_HELP_NUM = 8
    task.name = 'ZNS_HELP'
    task.init_config(ZnsHelpUserClass)
    task.main("炸年兽-助力")
