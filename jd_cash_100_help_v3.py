'''
new Env('邀好友抽现金-助力-v3');
cron: 6 6 6 6 6 python3 jd_cash_100_help_v3.py
export RabbitToken="token值"

'''
import asyncio
import json

from utils.common import UserClass, print_trace, TaskClass, get_error_msg

# linkId = "s9UT-99Aj2UjWRkU5k1Ksg"
linkId = "3orGfh1YkwNLksxOcN8zWQ"


class Cash100UserClass(UserClass):
    def __init__(self, cookie):
        super(Cash100UserClass, self).__init__(cookie)
        self.appname = ""
        self.activity_id = ""
        self.Origin = "https://prodev.m.jd.com"
        self.referer = "https://prodev.m.jd.com/"
        self.H5ST_VERSION = "4_1"
        self.invite_code = ''
        self.ua = self.ep_UA

    async def opt(self, opt):
        _opt = {
            "method": "get",
            "api": "api",
        }
        _opt.update(opt)
        return _opt

    def searchParams(self, searchParams):
        _searchParams = {
            "client": "apple",
            "clientVersion": "11.4.0",
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
            body = {"linkId": linkId, "isJdApp": True,
                    "inviter": inviter.invite_code}
            opt = {
                "method": "get",
                "functionId": "inviteFissionhelp",
                "body": body,
                "appId": "c5389",
                "searchParams": self.searchParams({
                    "functionId": "inviteFissionhelp",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            self.can_help = False
            if status == 200 and res_data.get("success", False):
                if data := res_data.get("data"):
                    helpResult = data.get("helpResult")
                    if helpResult == 1:
                        inviter.help_num += 1
                        self.printf_help(f"----->  {inviter.Name}:\t助力成功", inviter)
                    elif helpResult == 6:
                        self.printf_help(f"----->  {inviter.Name}:\t助力过了", inviter)
                    elif helpResult == 2:
                        self.printf_help(f"----->  {inviter.Name}:\t活动太火爆", inviter)
                    elif helpResult == 3:
                        self.printf_help(f"----->  {inviter.Name}:\t没有助力次数了", inviter)
                    elif helpResult is None:
                        self.printf_help(f"----->  {inviter.Name}:\t助力失败：{str(res_data)}", inviter)
                    else:
                        self.printf_help(
                            f"----->  {inviter.Name}:\t未知助力结果[{data.get('helpResult')}]：{str(res_data)}", inviter)
                else:
                    self.printf_help(f"----->  {inviter.Name}:\t助力失败[{status}]：{str(res_data)}", inviter)
            else:
                msg = get_error_msg(res_data)
                if "火爆" in msg:
                    self.can_help = False
                self.printf_help(f"----->  {inviter.Name}:\t助力失败：{msg}", inviter)
            if inviter.help_num >= inviter.MAX_HELP_NUM:
                inviter.need_help = False
        except:
            print_trace()

    # async def help(self, inviter: UserClass):
    #     try:
    #         if self.pt_pin == inviter.pt_pin:
    #             return
    #         if not await self.is_login():
    #             self.printf("未登录")
    #             return
    #         body = {"linkId": linkId, "isJdApp": True,
    #                 "inviter": inviter.invite_code}
    #         opt = {
    #             "method": "get",
    #             "functionId": "inviteFissionBeforeHome",
    #             "body": body,
    #             "appId": "02f8d",
    #             "searchParams": self.searchParams({
    #                 "functionId": "inviteFissionBeforeHome",
    #                 "body": json.dumps(body, separators=(",", ":"))
    #             }),
    #             "h5st": True
    #         }
    #         status, res_data = await self.jd_api(await self.opt(opt))
    #         self.can_help = False
    #         if status == 200 and res_data.get("success", False):
    #             if data := res_data.get("data"):
    #                 helpResult = data.get("helpResult")
    #                 if helpResult == 1:
    #                     inviter.help_num += 1
    #                     self.printf_help(f"----->  {inviter.Name}:\t助力成功", inviter)
    #                 elif helpResult == 6:
    #                     self.printf_help(f"----->  {inviter.Name}:\t助力过了", inviter)
    #                 elif helpResult == 2:
    #                     self.printf_help(f"----->  {inviter.Name}:\t活动太火爆", inviter)
    #                 elif helpResult == 3:
    #                     self.printf_help(f"----->  {inviter.Name}:\t没有助力次数了", inviter)
    #                 elif helpResult is None:
    #                     self.printf_help(f"----->  {inviter.Name}:\t助力失败：{str(res_data)}", inviter)
    #                 else:
    #                     self.printf_help(
    #                         f"----->  {inviter.Name}:\t未知助力结果[{data.get('helpResult')}]：{str(res_data)}", inviter)
    #             else:
    #                 self.printf_help(f"----->  {inviter.Name}:\t助力失败[{status}]：{str(res_data)}", inviter)
    #         else:
    #             print(res_data)
    #             msg = get_error_msg(res_data)
    #             if "火爆" in msg:
    #                 self.can_help = False
    #             self.printf_help(f"----->  {inviter.Name}:\t助力失败：{msg}", inviter)
    #         if inviter.help_num >= inviter.MAX_HELP_NUM:
    #             inviter.need_help = False
    #     except:
    #         print_trace()

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
            body = {"linkId": linkId, "inviter": "lgoudpmLcroNSzmdyMeyzL05ITAYtXoqcTLLVY7_anc"}
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

    async def wheelsHome(self):
        try:
            body = {"linkId": linkId}
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
    task.MAX_HELP_NUM = 300
    task.init_config(Cash100UserClass)
    asyncio.run(task.main("抽现金赢大礼-助力"))
