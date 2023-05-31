'''
new Env('邀好友抽现金-V2');
cron: 6 6 6 6 6 python3 jd_cash_100_v2.py
export RabbitToken="token值"

'''
import asyncio
import json

from utils.common import UserClass, print_trace, TaskClass, wait, randomWait, printf, get_error_msg

prize_conf = {
    '1': '优惠券',
    '2': '红包',
    '4': '现金',
}

linkId = "c6Bkpjp7dYcvQwO9-PR7-g"


class Cash100UserClass(UserClass):
    def __init__(self, cookie):
        super(Cash100UserClass, self).__init__(cookie)
        self.appname = ""
        self.activity_id = ""
        self.Origin = "https://prodev.m.jd.com"
        self.referer = "https://prodev.m.jd.com/"
        self.H5ST_VERSION = "4_1"
        self.invite_code = ''
        self.draw_num = 0
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

    async def init(self):
        pass

    async def inviteFissionHome(self):
        try:
            body = {"linkId": linkId, "inviter": ""}
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
                self.draw_num = res_data['data'].get("prizeNum", 0)
                self.printf(f"可以抽奖{self.draw_num}次")
                self.black = False
                if not self.invite_code:
                    self.need_help = False
                else:
                    self.need_help = True
            else:
                msg = get_error_msg(res_data)
                self.printf(f"进入主页失败: {msg}")
        except:
            print_trace()

    async def inviteFissionBeforeHome(self):
        try:
            body = {"linkId": linkId, "isJdApp": True,
                    "inviter": ""}
            opt = {
                "functionId": "inviteFissionBeforeHome",
                "body": body,
                "appId": "c02c6",
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
                    users = data.get("users", [])
                else:
                    pass
                    # self.printf_help(f"----->  {inviter.Name}:\t助力失败：{str(res_data)}", inviter)
            else:
                msg = get_error_msg(res_data)
                # self.printf_help(f"----->  {}:\t助力失败：{msg}", inviter)
        except:
            print_trace()

    async def inviteFissionDrawPrize(self):
        try:
            body = {"linkId": linkId}
            opt = {
                "functionId": "inviteFissionDrawPrize",
                "body": body,
                "appId": "c02c6",
                "searchParams": self.searchParams({
                    "functionId": "inviteFissionDrawPrize",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data.get("code", status)
            if code == 0 and res_data.get("data"):
                if res_data['data'].get("bigPrizeFlg"):
                    big_str = "开启大红包"
                else:
                    big_str = "抽奖"
                self.printf(
                    f'{big_str}: {res_data["data"].get("prizeValue", 0)}元{prize_conf[str(res_data["data"].get("prizeType", 0))]}')
            else:
                msg = get_error_msg(res_data)
                self.printf(f"抽奖失败: {msg}")
            return res_data
        except:
            print_trace()
            return res_data

    async def superRedBagList(self, pageNum):
        try:
            body = {"linkId": linkId, "pageNum": pageNum, "pageSize": 100, "business": "fission"}
            opt = {
                "functionId": "superRedBagList",
                "body": body,
                "appId": "f2b1d",
                "searchParams": self.searchParams({
                    "functionId": "superRedBagList",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data.get("code", status)
            if code == 0 and res_data.get("data"):
                if items := res_data['data'].get("items", []):
                    for item in items:
                        if item['prizeType'] == 4 and (item["state"] == 0 or item['state'] == 2):
                            if not await self.apCashWithDraw(item):
                                await self.apRecompenseDrawPrize(item)
                            await randomWait(4, 2)
            else:
                msg = get_error_msg(res_data)
                self.printf(f"查询提现列表失败: {msg}")
            return res_data
        except:
            print_trace()
            return {}

    async def apCashWithDraw(self, item):
        success = False
        try:
            body = {"linkId": linkId, "businessSource": "NONE",
                    "base": {"id": item['id'], "business": "fission", "poolBaseId": item['poolBaseId'],
                             "prizeGroupId": item['prizeGroupId'],
                             "prizeBaseId": item['prizeBaseId'], "prizeType": 4}}
            opt = {
                "functionId": "apCashWithDraw",
                "body": body,
                "appId": "8c6ae",
                "method": "post",
                "searchParams": self.searchParams({
                    "functionId": "apCashWithDraw",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data.get("code", status)
            if code == 0 and res_data.get("data"):
                if res_data['data'].get("status") == '1000':
                    error_msg = get_error_msg(res_data['data'])
                    self.printf(error_msg)
                elif res_data['data'].get("status") == '310':
                    error_msg = get_error_msg(res_data['data'])
                    self.printf(f"提现[{item['amount']}现金({item['prizeConfigName']})]: {error_msg}")
                    success = True
                elif res_data['data'].get("status") == '50056':
                    error_msg = get_error_msg(res_data['data'])
                    self.printf(f"提现[{item['amount']}现金({item['prizeConfigName']})]失败: {error_msg}")
                elif res_data['data'].get("status") == '50058':
                    error_msg = get_error_msg(res_data['data'])
                    self.printf(f"提现[{item['amount']}现金({item['prizeConfigName']})]失败: {error_msg}")
                elif res_data['data'].get("status") == '50059':
                    error_msg = get_error_msg(res_data['data'])
                    self.printf(f"提现[{item['amount']}现金({item['prizeConfigName']})]失败: {error_msg}")
                else:
                    self.printf(str(res_data))
            else:
                msg = get_error_msg(res_data)
                self.printf(f"提现失败: {msg}")
        except:
            print_trace()
        return success

    async def apRecompenseDrawPrize(self, item):
        try:
            body = {
                "linkId": linkId,
                "businessSource": "fission",
                "drawRecordId": item['id'],
                "business": "fission",
                "poolId": item['poolBaseId'],
                "prizeGroupId": item['prizeGroupId'],
                "prizeId": item["prizeBaseId"],
            }
            opt = {
                "functionId": "apRecompenseDrawPrize",
                "body": body,
                "appId": "8c6ae",
                "method": "post",
                "searchParams": self.searchParams({
                    "functionId": "apRecompenseDrawPrize",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data.get("code", status)
            if code == 0 and res_data.get("data"):
                self.printf(f"兑换[{item['amount']}红包({item['prizeConfigName']})]成功")
            else:
                msg = get_error_msg(res_data)
                self.printf(f"兑换[{item['amount']}红包({item['prizeConfigName']})]失败: {msg}")
        except:
            print_trace()

    async def main(self):
        if not await self.is_login():
            self.printf("未登录")
            return
        await self.inviteFissionBeforeHome()
        await self.inviteFissionHome()
        while True:
            res_data = await self.inviteFissionDrawPrize()
            code = res_data.get("code")
            msg = get_error_msg(res_data)
            await wait(1)
            if msg == "活动太火爆，请稍后重试~":
                continue
            if code != 0:
                break
        pageNum = 1
        while True:
            res_data = await self.superRedBagList(pageNum)
            if res_data.get("data", {}).get("hasMore", {}):
                pageNum = pageNum + 1
                await self.superRedBagList(pageNum)
            else:
                break


if __name__ == '__main__':
    task = TaskClass("task")
    task.name = 'Cash100_V2'
    task.init_config(Cash100UserClass)
    asyncio.run(task.main("邀好友抽现金-V2"))
