'''
new Env('拆快递领红包');
cron: 6 6 6 6 6 python3 jd_ckd_red_618.py
export RabbitToken="token值"

变量:
RabbitToken： 机器人给你发的token

log剩余次数大于5000方可使用
'''
import asyncio
import json
from urllib.parse import quote

from utils.common import UserClass, printf, print_api_error, print_trace, TaskClass, get_error_msg


def refresh_proxy_func(status, result):
    """
    是否切换ip

    :param status: http状态码
    :param result: 请求后的json数据
    :return: bool
    """
    msg = result.get("msg", "")
    if '环境异常' in msg:
        return True
    if not result.get("data"):
        return
    msg = result['data'].get("bizMsg", "")
    if '环境异常' in msg:
        return True


class CKDRedUserClass(UserClass):
    def __init__(self, cookie):
        super(CKDRedUserClass, self).__init__(cookie)
        self.inviteCode = ""
        self.appname = "50180"
        self._help_num = None
        self.secretp = ''
        self.H5ST_VERSION = "4_1"
        self.Origin = "https://wbbny.m.jd.com"
        self.referer = "https://wbbny.m.jd.com/"
        self.ua = self.ep_UA

    async def opt(self, opt):
        await self.set_joyytoken()
        # self.set_shshshfpb()
        _opt = {
            "method": "post",
            "log": False,
            "body_param": {
                "appid": "signed_wh5",
                "client": "apple",
                "clientVersion": "11.4.0",
                "functionId": opt['functionId'],
                "joylog": "",
            },
            "refresh_proxy_func": refresh_proxy_func
        }
        _opt.update(opt)
        return _opt

    def log_format(self, body, log_data):
        log = log_data["log"]
        random = log_data["random"]
        return {"body": json.dumps(body, separators=(',', ':')), "joylog": f"{random}*{log}"}

    def searchParams(self, searchParams):
        _searchParams = {
            "client": "apple",
            "clientVersion": "11.4.0",
            "appid": "interaction_share",
        }
        _searchParams.update(searchParams)
        return _searchParams

    @property
    def help_num(self):
        if self._help_num == None:
            self._help_num = 0
        return self._help_num

    @help_num.setter
    def help_num(self, value):
        self._help_num = value

    async def promote_pk_getMsgPopup(self):
        try:
            body = {}
            opt = {
                "functionId": "promote_pk_getMsgPopup",
                "body": body,
                "appId": "2a045",
                "searchParams": self.searchParams({
                    "functionId": "promote_pk_getMsgPopup",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True,
                "log": True
            }
            status, result = await self.jd_api(await self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    item = result['data']['result']['poplist']
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(msg)
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(msg)
        except:
            print_trace()

    async def promote_getHomeData(self):
        if self.secretp:
            return
        try:
            opt = {
                "functionId": "promote_getHomeData",
                "appid": "interaction_share"
            }
            status, result = await self.jd_api(await self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    self.secretp = result['data']['result']['homeMainInfo']['secretp']
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(msg)
            else:
                msg = get_error_msg(result)
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(msg)
        except:
            print_trace()

    async def promote_pk_receiveAward(self, orderId):
        try:
            body = {"orderId": orderId}
            opt = {
                "functionId": "promote_pk_receiveAward",
                "body": body,
            }
            status, result = await self.jd_api(await self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    awardInfo = result['data']['result'].get("awardInfo", {})
                    couponInfo = awardInfo.get("couponInfo", {})
                    redpacketInfo = awardInfo.get("redpacketInfo", {})
                    if couponInfo:
                        self.printf(
                            f"抽到优惠券: {couponInfo['quota']} - {couponInfo['discount']}({couponInfo['limitStr']}),\t使用时间: {couponInfo['desc']}")
                    if redpacketInfo:
                        self.printf(
                            f"抽到红包: {redpacketInfo['value']}元({redpacketInfo['name']}),\t使用时间: {redpacketInfo['desc']}")
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(f"[{self.Name}]\t{msg}")
            else:
                msg = get_error_msg(result)
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(f"{msg}")
        except:
            print_trace()

    async def get_invite_code(self):
        await self.promote_pk_getMsgPopup()
        try:
            if not await self.is_login():
                self.printf("未登录")
                return
            body = {}
            opt = {
                "functionId": "promote_pk_getHomeData",
                "body": body,
                "appId": "2a045",
                "searchParams": self.searchParams({
                    "functionId": "promote_pk_getHomeData",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True,
                "log": False
            }
            status, result = await self.jd_api(await self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    self.inviteCode = result["data"]["result"].get("inviteId")
                    self.printf(f"【助力邀请码】: \t{self.inviteCode}")
                    self.need_help = True
                    self.MAX_HELP_NUM = result["data"]["result"]['needAssistMaxNum']
                    self.help_num = result["data"]["result"]['alreadyAssistNum']
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

    async def help(self, inviter):
        try:
            if not await self.is_login():
                self.printf("未登录")
                return
            # await self.promote_getHomeData()
            if not self.can_help:
                return
            if inviter.help_num >= inviter.MAX_HELP_NUM:
                inviter.need_help = False
                printf(f"车头[{inviter.Name}]\t 助力已满({inviter.help_num}/{inviter.MAX_HELP_NUM})")
                return
            body = {
                "inviteId": inviter.inviteCode,
            }
            opt = {
                "functionId": "promote_pk_assist",
                "appId": "2a045",
                "searchParams": self.searchParams({
                    "functionId": "promote_pk_assist",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True,
                "body": body,
                "log": True
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data['code']
            if code == 0:
                if res_data['data'].get("bizCode") == 0:
                    inviter.help_num += 1
                    self.printf_help(f"助力成功", inviter)
                    self.can_help = False
                else:
                    msg = res_data['data'].get("bizMsg", "")
                    self.can_help = False
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
                        self.can_help = True
                        inviter.need_help = False
                        inviter.promote_pk_getAmountForecast()
                        inviter.promote_pk_receiveAward()
                    self.printf_help(f"助力失败[{code}]: {msg}", inviter)
            else:
                msg = res_data['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf_help(f"助力失败[{code}]: {msg}", inviter)
        except:
            print_trace()

    async def reward(self):
        try:
            body = {}
            opt = {
                "functionId": "promote_pk_getHomeData",
                "body": body,
                "appId": "2a045",
                "searchParams": self.searchParams({
                    "functionId": "promote_pk_getHomeData",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True,
                "log": False
            }
            status, result = await self.jd_api(await self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    red_list = result['data']['result']["redList"]
                    for red in red_list:
                        if red["status"] == 2:
                            await self.promote_pk_receiveAward(red['orderId'])
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


if __name__ == '__main__':
    task = TaskClass("invite")
    task.name = 'CKD_RED'
    task.MAX_HELP_NUM = 20
    task.init_config(CKDRedUserClass)
    asyncio.run(task.main("拆快递领红包"))
