'''
new Env('发财挖宝');
export RabbitToken="token值"
export FCWB_CK_REVERSE="1 或 2 或 3"
export FCWB_HELP_PIN="1~3或pin1,pin2,pin3或者ALL"
export FCWB_MAX_HELP_NUM=30
export FCWB_READ_FILE_CK="默认false" # ck文件为FCWB_ck.txt，格式为一行一个ck

变量:
RabbitToken： 机器人给你发的token
FCWB_HELP_PIN：设置车头
FCWB_CK_REVERSE：1：正序，2：反序，3：乱序
FCWB_MAX_HELP_NUM：每个队伍的人数
FCWB_READ_FILE_CK：读取ck文件，默认false，ck文件为FCWB_ck.txt，格式为一行一个ck

log剩余次数大于5000方可使用
'''
import asyncio
import json
import random

from utils.common import UserClass, printf, print_api_error, print_trace, TaskClass, wait, randomWait

linkId = "pTTvJeSTrpthgk9ASBVGsw"

chunkConf = {
    1: '优惠券',
    2: '红包',
    3: '现金',
    4: '炸弹',
}


class FcwbUserClass(UserClass):
    def __init__(self, cookie):
        super(FcwbUserClass, self).__init__(cookie)
        self.curRound = ""
        self.inviteCode = ""
        self.inviter = ""
        self.blood = 1000
        self._help_num = 0
        self.roundStop = False
        self.needNum = 0
        self.minBlood = 0
        self.UA = self.lite_UA
        self.stopFlag = False
        self.Origin = "https://bnzf.jd.com"
        self.referer = "https://bnzf.jd.com/?activityId=pTTvJeSTrpthgk9ASBVGsw&inviterId=&inviterCode=&utm_user=plusmember&ad_od=share&utm_source=androidapp&utm_medium=appshare&utm_campaign=t_335139774&utm_term=Wxfriends&lng=106.477132&lat=29.502772&sid=84c83c76030880654e4e98b6bcda688w&un_area=4_50952_106_0"

    # def init(self):
    #     self.ua = self.default_jsb_ua
    #     headers = {
    #         "Cookie": self.cookie,
    #         "User-Agent": self.ua,
    #         'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    #         "Origin": "https://bnzf.jd.com",
    #         "referer": "https://bnzf.jd.com/?activityId=pTTvJeSTrpthgk9ASBVGsw&inviterId=&inviterCode=&utm_user=plusmember&ad_od=share&utm_source=androidapp&utm_medium=appshare&utm_campaign=t_335139774&utm_term=Wxfriends&lng=106.477132&lat=29.502772&sid=84c83c76030880654e4e98b6bcda688w&un_area=4_50952_106_0"
    #     }
    #     self.headers = headers

    async def happyDigHelpList(self):
        try:
            body = {
                "pageNum": 1,
                "pageSize": 50,
                "linkId": linkId
            }
            opt = {
                "functionId": "happyDigHelpList",
                "body": body,
                "appId": "ce6c2",
                "searchParams": self.searchParams({
                    "functionId": "happyDigHelpList",
                    "body": json.dumps(body, separators=(",", ":"))
                })
            }
            status, data = await self.jd_api(self.opt(opt))
            if status == 200:
                if data["success"]:
                    pass
                    self.help_num = data['data'].get('personNum', 0)
                else:
                    self.black = True
            else:
                print_api_error(opt, status)
                self.black = True
        except:
            print_trace()

    def opt(self, opt):
        _opt = {
            "method": "get",
            "client": "ios",
            "clientVersion": "3.9.0",
            "appid": "activities_platform",
            "h5st": True,
        }
        _opt.update(opt)
        return _opt

    def searchParams(self, searchParams):
        _searchParams = {
            "client": "iOS",
            "clientVersion": "3.9.0",
            "appid": "activities_platform",
        }
        _searchParams.update(searchParams)
        return _searchParams

    async def home(self):
        body = {
            "linkId": linkId
        }
        opt = {
            "functionId": "happyDigHome",
            "body": body,
            "appId": "ce6c2",
            "searchParams": self.searchParams({
                "functionId": "happyDigHome",
                "body": json.dumps(body, separators=(",", ":"))
            })
        }
        status, res_data = await self.jd_api(self.opt(opt))
        if res_data.get('code') == 0:
            if self.help_num < self.MAX_HELP_NUM:
                self.printf(f"未完成助力，至少留下一点血")
                self.minBlood = 1
            await self.apTaskList()
            for item in res_data["data"]["roundList"]:
                if item['state'] == 1:
                    self.printf(
                        f"关卡[{item['round']}] -- 已完成，已获得{item.get('cashAmount') or 0}现金，{item.get('redAmount') or 0}红包")
                else:
                    self.printf(
                        f"关卡[{item['round']}] -- 未完成，已获得{item.get('cashAmount') or 0}现金，{item.get('redAmount') or 0}红包")
            for item in res_data["data"]["roundList"]:
                if item['state'] == 1:
                    continue
                if self.stopFlag:
                    break
                if self.blood <= self.minBlood:
                    break
                await self.prepareDig({"round": item['round']})
            await self.spring_reward_list()
        else:
            self.black = True

    async def spring_reward_list(self):
        try:
            body = {
                "linkId": linkId,
                "pageNum": 1,
                "pageSize": 10,
            }
            opt = {
                "functionId": "spring_reward_list",
                "body": body,
                "appId": "ce6c2",
                "searchParams": self.searchParams({
                    "functionId": "spring_reward_list",
                    "body": json.dumps(body, separators=(",", ":"))
                })
            }
            status, result = await self.jd_api(self.opt(opt))
            if result.get('code') == 0:
                withdrawList = [item for item in result['data']['items'] if
                                item["prizeType"] == 4 and item["state"] == 0]
                length = len(withdrawList)
                counter = 1
                for item in withdrawList:
                    await self.CashWithDraw(item)
                    if counter == length:
                        break
                    counter += 1
                    await randomWait(8, 5)
            else:
                msg = result.get("errMsg", "")
                msg = result.get("message", msg)
                msg = result.get("echo", msg)
                if '未登录' in msg:
                    self.valid = False
                elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                    self.can_help = False
                    self.black = True
                self.printf(f"查询奖励列表失败\t{msg}")
                print_api_error(opt, status)
        except:
            print_trace()

    async def CashWithDraw(self, item):
        try:
            body = {
                "businessSource": "happyDiggerH5Cash",
                "linkId": linkId,
                "base": {
                    "id": item['id'],
                    "business": "happyDigger",
                    "poolBaseId": item['poolBaseId'],
                    "prizeGroupId": item['prizeGroupId'],
                    "prizeBaseId": item['prizeBaseId'],
                    "prizeType": item['prizeType'],
                }
            }
            opt = {
                "functionId": "apCashWithDraw",
                "body": body,
                "appId": "ce6c2",
                "method": 'POST',
                "searchParams": self.searchParams({
                    "functionId": "happyDigHome",
                    "body": json.dumps(body, separators=(",", ":"))
                })
            }
            status, result = await self.jd_api(self.opt(opt))
            if result.get('code') == 0:
                self.printf(f"提现{item['amount']}元: {result['data'].get('message', '成功')}")
            else:
                msg = result.get("errMsg", "")
                msg = result.get("message", msg)
                msg = result.get("echo", msg)
                if '未登录' in msg:
                    self.valid = False
                elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                    self.can_help = False
                    self.black = True
                self.printf(f"查询奖励列表失败\t{msg}")
                print_api_error(opt, status)
        except:
            print_trace()

    async def prepareDig(self, paramIn):
        try:
            body = {
                "linkId": linkId,
                "round": paramIn['round'],
            }
            opt = {
                "functionId": "happyDigHome",
                "body": body,
                "appId": "ce6c2",
                "searchParams": self.searchParams({
                    "functionId": "happyDigHome",
                    "body": json.dumps(body, separators=(",", ":"))
                })
            }
            status, result = await self.jd_api(self.opt(opt))
            if result.get('code') == 0:
                self.roundStop = False
                self.blood = result['data']['blood']
                self.printf(f"开始第{paramIn['round']}关，血量: {self.blood}")
                for item in result['data']['roundList']:
                    if not item["chunks"]:
                        continue
                    chunkList = [chunks for chunks in item["chunks"] if not chunks["state"]]
                    random.shuffle(chunkList)
                    chunkListLen = len(chunkList)
                    counter = 1
                    for chunk in chunkList:
                        if self.blood <= self.minBlood:
                            self.printf(f"血量不足，退出")
                            break
                        param = {
                            "round": paramIn['round'],
                            "rowIdx": chunk['rowIdx'],
                            "colIdx": chunk['colIdx']
                        }
                        await randomWait(1, 1)
                        await self.happyDigDo(param)
                        counter += 1
                        if self.stopFlag:
                            break
                        if self.roundStop:
                            break
            else:
                msg = result.get("errMsg", "")
                msg = result.get("message", msg)
                msg = result.get("echo", msg)
                if '未登录' in msg:
                    self.valid = False
                elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                    self.can_help = False
                    self.black = True
                self.printf(f"查询挖宝进度失败\t{msg}")
                print_api_error(opt, status)
        except:
            print_trace()

    async def happyDigDo(self, paramIn):
        try:
            body = {
                "round": paramIn['round'],
                "rowIdx": paramIn['rowIdx'],
                "colIdx": paramIn['colIdx'],
                "linkId": linkId
            }
            opt = {
                "functionId": "happyDigDo",
                "body": body,
                "appId": "f7674",
                "searchParams": self.searchParams({
                    "functionId": "happyDigDo",
                    "body": json.dumps(body, separators=(",", ":"))
                })
            }
            status, result = await self.jd_api(self.opt(opt))
            if result.get('code') == 0:
                strs = chunkConf[result['data']['chunk']['type']]
                self.printf(
                    f"({paramIn['rowIdx']},{paramIn['colIdx']})挖到了{result['data']['chunk'].get('value', '')}{strs}")
                if result['data']['chunk']['type'] == 1:
                    self.printf(f"出现优惠券，不挖了")
                    self.stopFlag = True
                if result['data']['chunk']['type'] == 4:
                    self.blood -= 1
                    self.printf(f"血量：{self.blood}")
                if result['data'].get('lastPrize'):
                    self.roundStop = True
                    self.printf(
                        f"关卡[{paramIn['round']}]已完成，获得了{result['data']['cashAmount']}现金，{result['data']['redAmount']}红包")
            else:
                msg = result.get("errMsg", "")
                msg = result.get("message", msg)
                msg = result.get("echo", msg)
                if '未登录' in msg:
                    self.stopFlag = True
                    self.valid = False
                elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                    self.can_help = False
                    self.black = True
                    self.stopFlag = True
                self.printf(f"挖宝({paramIn['rowIdx']},{paramIn['colIdx']})失败\t{msg}")
                print_api_error(opt, status)
        except:
            print_trace()

    async def doTask(self, task):
        body = {
            "linkId": linkId,
            "taskType": task['taskType'],
            "taskId": task['id'],
            "channel": 4,
            "itemId": task.get('itemId', task.get('taskSourceUrl', '')),
            "checkVersion": True
        }
        opt = {
            "functionId": "apDoTask",
            "body": body,
            "appId": "ce6c2",
            "searchParams": self.searchParams({
                "functionId": "apDoTask",
                "body": json.dumps(body, separators=(",", ":"))
            })
        }
        status, result = await self.jd_api(self.opt(opt))
        if result.get('code') == 0:
            self.needNum -= 1
            self.printf(f"完成任务[{task.get('itemName', task.get('taskShowTitle'))}]成功")
        else:
            msg = result.get("errMsg", "")
            msg = result.get("message", msg)
            msg = result.get("echo", msg)
            if '未登录' in msg:
                self.valid = False
            elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                self.can_help = False
                self.black = True
            self.printf(f"完成任务失败\t{msg}")
            print_api_error(opt, status)

    async def TaskDetail(self, task):
        try:
            body = {
                "linkId": linkId,
                "taskType": task['taskType'],
                "taskId": task['id'],
                "channel": 4,
            }
            opt = {
                "functionId": "apTaskDetail",
                "body": body,
                "appId": "ce6c2",
                "searchParams": self.searchParams({
                    "functionId": "apTaskDetail",
                    "body": json.dumps(body, separators=(",", ":"))
                })
            }
            status, result = await self.jd_api(self.opt(opt))
            if result.get('code') == 0:
                needNum = result['data']['status']['finishNeed'] - result['data']['status']['userFinishedTimes']
                doNum = 0
                for param in result['data']['taskItemList']:
                    if doNum >= needNum:
                        break
                    param.update(task)
                    await self.taskTimeRecord(param)
                    await self.doTask(param)
                    doNum += 1
                self.printf(f"完成任务[{task.get('itemName', task.get('taskShowTitle'))}]成功")
            else:
                msg = result.get("errMsg", "")
                msg = result.get("message", msg)
                msg = result.get("echo", msg)
                if '未登录' in msg:
                    self.valid = False
                elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                    self.can_help = False
                    self.black = True
                self.printf(f"查询任务[{task['taskShowTitle']}]失败\t{msg}")
                print_api_error(opt, status)
        except:
            print_trace()

    async def taskTimeRecord(self, task):
        try:
            body = {
                "linkId": linkId,
                "taskId": task['id'],
            }
            opt = {
                "functionId": "apTaskTimeRecord",
                "body": body,
                "appId": "ce6c2",
                "searchParams": self.searchParams({
                    "functionId": "apTaskTimeRecord",
                    "body": json.dumps(body, separators=(",", ":"))
                })
            }
            status, result = await self.jd_api(self.opt(opt))
            if result.get('code') == 0:
                self.printf(f"开始任务[{task.get('itemName', task.get('taskShowTitle'))}]，需要等待{result['data']['timePeriod']}秒")
                await wait(result['data'].get('timePeriod', 0))
            else:
                msg = result.get("errMsg", "")
                msg = result.get("message", msg)
                msg = result.get("echo", msg)
                if '未登录' in msg:
                    self.valid = False
                elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                    self.can_help = False
                    self.black = True
                self.printf(f"开始任务[{task.get('itemName', task.get('taskShowTitle'))}]失败\t{msg}")
                print_api_error(opt, status)
        except:
            print_trace()

    async def apTaskList(self):
        try:
            body = {
                "linkId": linkId
            }
            opt = {
                "functionId": "apTaskList",
                "body": body,
                "appId": "ce6c2",
                "searchParams": self.searchParams({
                    "functionId": "apTaskList",
                    "body": json.dumps(body, separators=(",", ":"))
                })
            }
            status, result = await self.jd_api(self.opt(opt))
            if result.get('success'):
                for item in result['data']:
                    if item['taskFinished']:
                        self.printf(
                            f"任务[{item['taskShowTitle']}] -- 已完成，{item['taskDoTimes']}/{item['taskLimitTimes']}")
                    else:
                        self.printf(
                            f"任务[{item['taskShowTitle']}] -- 未完成，{item['taskDoTimes']}/{item['taskLimitTimes']}")
                    if not item['taskFinished'] and "BROWSE_CHANNEL" in item['taskType']:
                        if item.get('taskSourceUrl'):
                            await self.doTask(item)
                        else:
                            await self.TaskDetail(item)
            else:
                msg = result.get("errMsg", "")
                msg = result.get("message", msg)
                msg = result.get("echo", msg)
                if '未登录' in msg:
                    self.valid = False
                elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                    self.can_help = False
                    self.black = True
                self.printf(f"查询挖宝任务失败\t{msg}")
                print_api_error(opt, status)
        except:
            print_trace()

    async def main(self):
        if not await self.is_login():
            self.printf("未登录")
            return
        await self.happyDigHelpList()
        await self.home()
        printf("\n")


if __name__ == '__main__':
    task = TaskClass("task")
    task.MAX_HELP_NUM = 40
    task.name = 'FCWB'
    task.init_config(FcwbUserClass)
    asyncio.run(task.main("发财挖宝-任务"))
