'''
new Env('拼手速拆快递-游戏');
cron 8,12,17,20 * * * * python jd_ckd_game_618.py
export RabbitToken="token值"

变量:
RabbitToken： 机器人给你发的token

log剩余次数大于5000方可使用
'''
import asyncio
import json

from utils.common import UserClass, printf, print_api_error, print_trace, TaskClass, get_error_msg


class CKDGameUserClass(UserClass):
    def __init__(self, cookie):
        super(CKDGameUserClass, self).__init__(cookie)
        self.inviteCode = ""
        self.appname = "50180"
        self._help_num = None
        self._error = 0
        self.Origin = "https://wbbny.m.jd.com"
        self.referer = "https://wbbny.m.jd.com/"

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value
        if self._error >= 3:
            self.black = True
            self.need_help = False
            self.can_help = False

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
        try:
            if not await self.is_login():
                self.printf("未登录")
                return
            body = {}
            opt = {
                "functionId": "promote_pointplay",
                "body": body,
            }
            status, result = await self.jd_api(await self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0 and result['data']["result"].get('actId'):
                    actId = result['data']["result"].get('actId')
                    await self.promote_pointplay_award(actId)
                else:
                    msg = get_error_msg(result['data'])
                    if '登录' in msg:
                        self.valid = False
                    self.printf(f"请求失败[{status}]:\t {msg}")
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                self.printf(f"{msg}")
        except:
            print_trace()

    async def promote_pointplay_award(self, actId) -> None:
        try:
            body = {
                "actId": actId,
            }
            opt = {
                "functionId": "promote_pointplay_award",
                "body": body,
                "appId": "2a045",
                "searchParams": self.searchParams({
                    "functionId": "promote_collectScore",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True,
                "log": True
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data['code']
            if code == 0:
                if res_data['data'] and res_data['data'].get('bizCode') == 0:
                    self.printf("成功： 奖励一个快递箱")
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
    task.name = 'CKD'
    task.need_appck = True
    task.init_config(CKDGameUserClass)
    asyncio.run(task.main("拼手速拆快递-game"))
