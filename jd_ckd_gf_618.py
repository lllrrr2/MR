'''
new Env('全民拆快递-瓜分-2023');
cron 0 20 * * * python jd_ckd_game_618.py
export RabbitToken="token值"

变量:
RabbitToken： 机器人给你发的token

log剩余次数大于5000方可使用
'''
import asyncio
import json

from utils.common import UserClass, printf, print_api_error, print_trace, TaskClass, get_error_msg


class CKDGFUserClass(UserClass):
    def __init__(self, cookie):
        super(CKDGFUserClass, self).__init__(cookie)
        self.inviteCode = ""
        self.appname = "50180"
        self._help_num = None
        self._error = 0
        self.H5ST_VERSION = "4_1"
        self.Origin = "https://wbbny.m.jd.com"
        self.referer = "https://wbbny.m.jd.com/"
        self.ua = self.ep_UA

    async def opt(self, opt):
        # await self.set_shshshfpb()
        await self.set_joyytoken()
        await self.set_joyytokenb()
        # await self.set_shshshfpb()
        _opt = {
            "method": "post",
            "log": False,
            "body_param": {
                "appid": "signed_wh5",
                "client": "apple",
                "clientVersion": "11.4.0",
                "functionId": opt['functionId'],
                "joylog": "",
                "x-api-eid-token": "",
            }
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
            "appid": "signed_wh5",
        }
        _searchParams.update(searchParams)
        return _searchParams

    async def main(self):
        # await self.promote_mainDivideRedPacket()
        await self.promote_getHomeData()
        raiseInfo = self.homeData['raiseInfo']
        fullFlag = raiseInfo.get('fullFlag', False)
        if not fullFlag:
            if raiseInfo['buttonStatus'] == 5:
                self.printf(f"已拆快递:{raiseInfo['redInfo']['red']}份")
                await self.promote_mainDivideRedPacket()
            elif raiseInfo['buttonStatus'] in [6]:
                self.printf("已瓜分，等待发放")
                self.printf(f"已瓜分:{raiseInfo['redInfo']['red']}份")
            elif raiseInfo['buttonStatus'] in [4, 7]:
                self.printf(f"已瓜分:{raiseInfo['redInfo']['red']}🧧")
            elif raiseInfo['buttonStatus'] in [1, 3]:
                self.printf(f"等待瓜分大奖\n")
            elif raiseInfo['buttonStatus'] in [2]:
                self.printf(f"您无瓜分资格")
                self.printf(f"已瓜分:{raiseInfo['redInfo']['red']}份")
            elif raiseInfo['buttonStatus'] in [2]:
                self.printf(f"无法瓜分[{raiseInfo['buttonStatus']}]份")

    async def promote_getHomeData(self):
        try:
            body = {}
            opt = {
                "functionId": "promote_getHomeData",
                "body": body,
                "appId": "2a045",
                "searchParams": self.searchParams({
                    "functionId": "promote_getHomeData",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True,
                # "log": True
            }
            status, result = await self.jd_api(await self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    self.homeData = result['data']['result']['homeMainInfo']
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(f"{msg}")
            else:
                msg = get_error_msg(result)
                if '登录' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                elif "环境异常" in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                    self.black = True
                self.printf(msg)
        except:
            print_trace()

    async def promote_mainDivideRedPacket(self) -> None:
        try:
            body = {}
            opt = {
                "functionId": "promote_mainDivideRedPacket",
                "body": body,
                "appId": "2a045",
                "searchParams": self.searchParams({
                    "functionId": "promote_mainDivideRedPacket",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True,
                # "log": True
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data['code']
            if code == 0:
                if res_data.get('data') and res_data['data'].get('bizCode') == 0:
                    try:
                        self.printf(f"瓜分红包：{res_data['data']['result']['value']}🧧")
                    except:
                        self.printf(str(res_data))
                        msg = get_error_msg(res_data)
                        self.printf(f"失败[{code}]: {msg}")
                else:
                    msg = get_error_msg(res_data)
                    self.printf(f"失败[{code}]: {msg}")
            else:
                msg = get_error_msg(res_data)
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                self.printf(f"失败[{code}]: {msg}")
        except:
            print_trace()


if __name__ == '__main__':
    task = TaskClass("task")
    task.name = 'CKD_GF'
    task.need_appck = True
    task.init_config(CKDGFUserClass)
    asyncio.run(task.main("全民拆快递-瓜分-2023"))
