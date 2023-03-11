import asyncio
import json

from utils.common import UserClass, print_trace, print_api_error, TaskClass, get_error_msg


class TylhbUserClass(UserClass):
    def __init__(self, cookie):
        super(TylhbUserClass, self).__init__(cookie)
        self.appname = ""
        self.activity_id = ""
        self.Origin = "https://wqs.jd.com"
        self.referer = "https://wqs.jd.com/"
        self.H5ST_VERSION = "3_1"
        self.help_num = 0
        self.invite_code = ''
        self.itemId = ''

    async def opt(self, opt):
        _opt = {
            "method": "get",
            "api": "",
        }
        _opt.update(opt)
        return _opt

    def searchParams(self, searchParams):
        _searchParams = {
            "client": "cs_h5",
            "clientVersion": "1.0",
            "appid": "cs_h5",
        }
        _searchParams.update(searchParams)
        return _searchParams

    async def help(self, inviter: UserClass):
        try:
            if not await self.is_login():
                self.printf("未登录")
                return
            if self.pt_pin == inviter.pt_pin:
                return
            body = {"activeId": "63ef4e50c800b87f7a99e144", "shareId": inviter.invite_code,
                    "itemId": inviter.itemId}
            opt = {
                "functionId": "festivalhb_help",
                "body": body,
                "appId": "38c56",
                "searchParams": self.searchParams({
                    "functionId": "festivalhb_help",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data.get("code", status)
            error_msg = get_error_msg(res_data)
            if code == 0 and res_data.get("data"):
                inviter.help_num += 1
                self.can_help = False
                self.printf_help(f"----->  {inviter.Name}:\t助力成功", inviter)
            elif code == 103:
                inviter.need_help = False
                self.printf_help(f"----->  {inviter.Name}:\t助力失败：{error_msg}", inviter)
            elif code in [108, 13]:
                self.can_help = False
                self.printf_help(f"----->  {inviter.Name}:\t助力失败：{error_msg}", inviter)
            else:
                self.printf_help(f"----->  {inviter.Name}:\t助力失败[{code}]：{error_msg}", inviter)
            if inviter.help_num >= inviter.MAX_HELP_NUM:
                inviter.need_help = False
        except:
            print_trace()

    async def festivalhb_home(self):
        try:
            body = {"activeId": "63ef4e50c800b87f7a99e144"}
            opt = {
                "functionId": "festivalhb_home",
                "body": body,
                "appId": "38c56",
                "params": self.searchParams({}),
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data.get("code", status)
            if code == 0 and res_data.get("data"):
                if helpTask := res_data['data'].get("helpTask"):
                    self.MAX_HELP_NUM = helpTask.get('assignmentTimesLimit', 0)
                    self.help_num = helpTask.get('completionCnt', 0)
                    self.invite_code = res_data['data'].get("shareId", "")
                    self.itemId = helpTask.get("itemId", "")
                    self.printf(f"助力码为：{self.invite_code}")
                    self.printf(f"已邀请： {self.help_num}/{self.MAX_HELP_NUM}")
                if not self.invite_code:
                    self.need_help = False
                else:
                    self.need_help = True
            else:
                msg = get_error_msg(res_data)
                self.printf(f"进入主页失败: {msg}")
        except:
            print_trace()

    async def get_invite_code(self):
        if not await self.is_login():
            self.printf("未登录")
            return
        try:
            await self.festivalhb_home()
        except:
            print_trace()


if __name__ == '__main__':
    task = TaskClass("help")
    task.name = 'TYLHB_HELP'
    task.init_config(TylhbUserClass)
    asyncio.run(task.main("团圆领红包-助力"))
