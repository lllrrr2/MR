'''
new Env('炸年兽-膨胀');
export RabbitToken="token值"
export ZNS_PZ_CK_REVERSE="0 或 1 或 2"
export ZNS_PZ_HELP_PIN="1~3或pin1,pin2,pin3或者ALL"
export ZNS_PZ_MAX_HELP_NUM=30
export ZNS_PZ_READ_FILE_CK="默认false" # ck文件为ZNS_ZD_ck.txt，格式为一行一个ck

变量:
RabbitToken： 机器人给你发的token
ZNS_PZ_HELP_PIN：设置车头
ZNS_PZ_CK_REVERSE：0：正序，1：反序，2：乱序
ZNS_PZ_MAX_HELP_NUM：每个队伍的人数
ZNS_PZ_READ_FILE_CK：读取ck文件，默认false，ck文件为ZNS_ZD_ck.txt，格式为一行一个ck

log剩余次数大于5000方可使用
'''
from utils.common import UserClass, printf, print_api_error, print_trace, TaskClass


class ZnsPZUserClass(UserClass):
    def __init__(self, cookie):
        super(ZnsPZUserClass, self).__init__(cookie)
        self.inviteCode = ""
        self.name = "ZNS"
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

    def promote_pk_getMsgPopup(self):
        try:
            body = {}
            opt = {
                "functionId": "promote_pk_getMsgPopup",
                "body": body,
                "need_log": True
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    for item in result['data']['result']:
                        if item and item.get("divideResultVO") and item["divideResultVO"].get("divideValue"):
                            printf(
                                f"开启组队红包咯，分到了{item['divideResultVO']['divideValue']}元，最高膨胀到{item['divideResultVO']['maxInflateAward']}元")
                        else:
                            printf(f"开组队红包失败: {result['msg']}")
                            return ""
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    printf(f"[{self.Name}]\t{msg}")
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                printf(f"[{self.Name}]\t{msg}")
        except:
            print_trace()

    def promote_pk_getAmountForecast(self):
        try:
            body = {}
            opt = {
                "functionId": "promote_pk_getAmountForecast",
                "body": body,
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    pass
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    printf(f"[{self.Name}]\t{msg}")
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                printf(f"[{self.Name}]\t{msg}")
        except:
            print_trace()

    def promote_pk_receiveAward(self):
        try:
            body = {}
            opt = {
                "functionId": "promote_pk_receiveAward",
                "body": body,
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    printf(f"[{self.Name}]\t领取膨胀红包成功: {result['data']['result']['value']}元")
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    printf(f"[{self.Name}]\t{msg}")
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                printf(f"[{self.Name}]\t{msg}")
        except:
            print_trace()

    def get_invite_code(self):
        self.promote_pk_getMsgPopup()
        self.promote_pk_getAmountForecast()
        try:
            body = {}
            opt = {
                "functionId": "promote_pk_getExpandDetail",
                "body": body,
                "need_log": False
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    self.inviteCode = result["data"]["result"].get("inviteId")
                    printf(f"{self.Name}【膨胀邀请码】: \t{self.inviteCode}")
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
                printf(f"[{self.Name}]\t{msg}")
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
                "functionId": "promote_pk_collectPkExpandScore",
                "body": body,
                "log": True
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
                    elif '助力次数' in msg:
                        self.can_help = False
                    elif '火爆' in msg:
                        self.can_help = False
                    elif '邀请过' in msg:
                        pass
                    elif '助力已结束' in msg:
                        inviter.need_help = False
                    elif '足够的助力' in msg:
                        inviter.need_help = False
                        inviter.promote_pk_getAmountForecast()
                        inviter.promote_pk_receiveAward()
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
    task = TaskClass("invite")
    task.MAX_HELP_NUM = 100
    task.name = 'ZNS_PZ'
    task.init_config(ZnsPZUserClass)
    task.main("炸年兽-膨胀")
