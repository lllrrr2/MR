import asyncio
import json

from utils.common import UserClass, print_trace, print_api_error, TaskClass, get_error_msg, wait


class TylhbUserClass(UserClass):
    def __init__(self, cookie):
        super(TylhbUserClass, self).__init__(cookie)
        self.appname = ""
        self.activity_id = ""
        self.Origin = "https://wqs.jd.com"
        self.referer = "https://wqs.jd.com/"
        self.H5ST_VERSION = "3_1"
        self.help_num = 0
        self.drawChanceNum = 0
        self.invite_code = ''
        self.itemId = ''
        self.can_withdraw = True

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

    async def festivalhb_draw(self):
        try:
            body = {"activeId": "63ef4e50c800b87f7a99e144"}
            opt = {
                "functionId": "festivalhb_draw",
                "body": body,
                "appId": "38c56",
                "params": self.searchParams({}),
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data.get("code", status)
            error_msg = get_error_msg(res_data)
            if code == 0 and res_data.get("data"):
                prize = res_data['data'].get("prize", [{}])[0]
                prize = prize.get("desc", "空气")
                self.printf(f"开红包： {prize}")
            else:
                self.printf(f"开红包失败：{error_msg}")
        except:
            print_trace()

    async def festivalhb_querymyprizelist(self):
        try:
            body = {"activeId": "63ef4e50c800b87f7a99e144", "type": 1}
            opt = {
                "functionId": "festivalhb_querymyprizelist",
                "body": body,
                "appId": "38c56",
                "params": self.searchParams({}),
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data.get("code", status)
            error_msg = get_error_msg(res_data)
            if code == 0 and res_data.get("data"):
                canUseCoinAmount = res_data['data'].get("canUseCoinAmount", 0)
                totalHbAmount = res_data['data'].get("totalHbAmount", 0)
                self.printf(f"现金余额： {canUseCoinAmount}元,共获得红包{totalHbAmount}元")
            else:
                self.printf(f"查询奖品失败：{error_msg}")
        except:
            print_trace()

    async def festivalhb_queryexchangelist(self):
        try:
            body = {"activeId": "63ef4e50c800b87f7a99e144"}
            opt = {
                "functionId": "festivalhb_queryexchangelist",
                "body": body,
                "appId": "38c56",
                "params": self.searchParams({}),
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data.get("code", status)
            error_msg = get_error_msg(res_data)
            if code == 0 and res_data.get("data"):
                self.cash = float(res_data['data'].get("canUseCoinAmount", 0))
                cashExchangeRuleList = res_data['data'].get("cashExchangeRuleList", [])
                can_exchange = sorted(cashExchangeRuleList, key=lambda x: float(x['cashoutAmount']))
                for item in can_exchange:
                    if self.cash < float(item['consumeScore']):
                        continue
                    await self.jxPrmtExchange_exchange(item)
                    if not self.can_withdraw:
                        break
            else:
                self.printf(f"查询提现列表失败[{code}]：{error_msg}")
        except:
            print_trace()

    async def jxPrmtExchange_exchange(self, item):
        try:
            body = {
                "bizCode": "festivalhb",
                "ruleId": item['id'],
            }
            opt = {
                "functionId": "jxPrmtExchange_exchange",
                "body": body,
                "appId": "af89e",
                "searchParams": self.searchParams({
                    "client": "jxh5",
                    "clientVersion": '1.2.5',
                    "functionId": "jxPrmtExchange_exchange",
                    "body": json.dumps(body, separators=(",", ":"))
                }),
                "h5st": True
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data.get("code", status)
            error_msg = get_error_msg(res_data)
            if code == 0 and res_data.get("data"):
                cashoutResult = res_data['data'].get("cashoutResult", {})
                cashoutCode = cashoutResult.get("cashoutCode")
                if cashoutCode == 1:
                    self.cash -= float(item['consumeScore'])
                    self.printf(f"提现[{item.name}]成功")
                else:
                    self.printf(f"提现[{item['name']}]失败[{cashoutCode}]: error_msg")
            else:
                self.printf(f"提现[{item['name']}]失败[{code}]：{error_msg}")
                if "openId为空" in error_msg or "提现进行中" in error_msg:
                    self.can_withdraw = False
        except:
            print_trace()

    async def festivalhb_browse(self, task, itemId):
        try:
            body = {"activeId": "63ef4e50c800b87f7a99e144", "shareId": task['encryptAssignmentId'],
                    "itemId": itemId}
            opt = {
                "functionId": "festivalhb_browse",
                "body": body,
                "appId": "38c56",
                "params": self.searchParams({}),
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data.get("code", status)
            error_msg = get_error_msg(res_data)
            if code == 0 and res_data.get("data"):
                self.printf(f"完成任务[{task['assignmentName']}]成功, 获得{res_data['data'].get('awardChance')}个红包")
            else:
                self.printf(f"完成任务[{task['assignmentName']}]失败[{code}]: {error_msg}")
        except:
            print_trace()

    async def festivalhb_home(self):
        try:
            body = {"activeId": "63ef4e50c800b87f7a99e144"}
            opt = {
                "functionId": "festivalhb_home",
                "body": body,
                "appId": "38c56",
                "params": self.searchParams({})
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            code = res_data.get("code", status)
            if code == 0 and res_data.get("data"):
                drawProgress = res_data['data'].get("drawProgress", {})
                self.drawChanceNum = res_data['data'].get("drawChanceNum", 0)
                hasDrawNum = drawProgress.get("hasDrawNum", 0)
                maxDrawLimitNum = drawProgress.get("maxDrawLimitNum", 0)
                self.printf(f"可开{self.drawChanceNum}个红包, 大红包进度: {hasDrawNum}/{maxDrawLimitNum}")
            else:
                msg = get_error_msg(res_data)
                self.printf(f"进入主页失败: {msg}")
        except:
            print_trace()

    async def main(self):
        if not await self.is_login():
            self.printf("未登录")
            return
        await self.festivalhb_home()
        for i in range(self.drawChanceNum):
            await self.festivalhb_draw()
            await wait(1)
        await self.festivalhb_querymyprizelist()
        await self.festivalhb_queryexchangelist()


if __name__ == '__main__':
    task = TaskClass("task")
    task.name = 'TYLHB'
    task.init_config(TylhbUserClass)
    asyncio.run(task.main("团圆领红包-开红包"))
