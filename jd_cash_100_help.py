import asyncio
import json
import re

import aiohttp

from utils.common import UserClass, print_trace, TaskClass, printf, get_error_msg


class Cash100UserClass(UserClass):
    def __init__(self, cookie):
        super(Cash100UserClass, self).__init__(cookie)
        self.appname = ""
        self.activity_id = ""
        self.Origin = "https://prodev.m.jd.com"
        self.referer = "https://prodev.m.jd.com/"
        self.H5ST_VERSION = "3_1"
        self.invite_code = ''

    async def opt(self, opt):
        _opt = {
            "method": "get",
            "api": "",
        }
        _opt.update(opt)
        return _opt

    def searchParams(self, searchParams):
        _searchParams = {
            "client": "iOS",
            "clientVersion": "10.0.4",
            "appid": "activities_platform",
        }
        _searchParams.update(searchParams)
        return _searchParams

    async def help(self, inviter: UserClass):
        try:
            if self.pt_pin == inviter.pt_pin:
                return
            if not await self.is_login():
                self.printf("未登录")
                return
            body = {"linkId": self.env.init_data, "isJdApp": True,
                    "inviter": inviter.invite_code}
            opt = {
                "functionId": "inviteFissionBeforeHome",
                "body": body,
                "appId": "02f8d",
                "searchParams": self.searchParams({
                    "functionId": "inviteFissionBeforeHome",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            self.can_help = False
            if res_data.get("success", False):
                if data := res_data.get("data"):
                    match data.get("helpResult"):
                        case 1:
                            inviter.help_num += 1
                            self.printf_help(f"----->  {inviter.Name}:\t助力成功", inviter)
                        case 6:
                            self.printf_help(f"----->  {inviter.Name}:\t助力过了", inviter)
                        case None:
                            self.printf_help(f"----->  {inviter.Name}:\t助力失败：{str(res_data)}", inviter)
                        case _:
                            self.printf_help(f"----->  {inviter.Name}:\t未知助力结果：{data.get('helpResult')}", inviter)
                else:
                    self.printf_help(f"----->  {inviter.Name}:\t助力失败：{str(res_data)}", inviter)
            else:
                msg = res_data.get("errMsg", None)
                if "火爆" in msg:
                    self.can_help = False
                self.printf_help(f"----->  {inviter.Name}:\t助力失败：{msg}", inviter)
            if inviter.help_num >= inviter.MAX_HELP_NUM:
                inviter.need_help = False
        except:
            print_trace()

    async def get_invite_code(self):
        if not await self.is_login():
            self.printf("未登录")
            return
        try:
            await self.wheelsHome()
            await self.inviteFissionHome()
        except:
            print_trace()

    async def inviteFissionHome(self):
        try:
            body = {"linkId": self.env.init_data, "inviter": "lgoudpmLcroNSzmdyMeyzL05ITAYtXoqcTLLVY7_anc"}
            opt = {
                "functionId": "inviteFissionHome",
                "body": body,
                "appId": "eb67b",
                "searchParams": self.searchParams({
                    "functionId": "inviteFissionHome",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data.get("code", status)
            if code == 0 and res_data.get("data"):
                self.invite_code = res_data['data'].get("inviter", "")
                self.printf(f"助力码为：{self.invite_code}")
                if not self.invite_code:
                    self.need_help = False
                else:
                    self.need_help = True
            else:
                msg = get_error_msg(res_data)
                self.printf(f"进入主页失败: {msg}")
        except:
            print_trace()

    async def init(self):
        for i in range(3):
            url = "https://prodev.m.jd.com/mall/active/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/index.html"
            async with aiohttp.ClientSession() as client:
                headers = {
                    "User-Agent": self.UA
                }
                res = await client.get(url, headers=headers)
                text = await res.text()
                data = re.findall(r"try\{window\.__ihubData__ *\=(.*?)\}catch\(e\)", text)[0]
                data = json.loads(data)
                for one in data.get("codeFloors", []):
                    boardParams = one.get("boardParams", {})
                    linkId = boardParams.get("linkId", "")
                    if linkId:
                        return linkId
                else:
                    printf(f"初始化失败， 第{i+1}次重试")
                    continue
        else:
            printf("初始化失败, 终止程序")
            return ""

    async def wheelsHome(self):
        try:
            body = {"linkId": self.env.init_data}
            opt = {
                "functionId": "wheelsHome",
                "body": body,
                "params": self.searchParams({})
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data.get("code", status)
            if code == 0 and res_data.get("data"):
                self.invite_code = res_data['data'].get("inviter", "")
                self.printf(f"助力码为：{self.invite_code}")
                if not self.invite_code:
                    self.need_help = False
                else:
                    self.need_help = True
            else:
                msg = get_error_msg(res_data)
                self.printf(f"进入主页失败: {msg}")
        except:
            print_trace()


if __name__ == '__main__':
    task = TaskClass("help")
    task.name = 'Cash100_HELP'
    task.MAX_HELP_NUM = 100
    task.init_config(Cash100UserClass)
    asyncio.run(task.main("抽现金赢大礼-助力"))
