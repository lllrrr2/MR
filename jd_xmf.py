'''
new Env('小魔方');
export RabbitToken="token值"
export XMF_CK_REVERSE="1 或 2 或 3"
export XMF_HELP_PIN="1~3或pin1,pin2,pin3或者ALL"
export XMF_MAX_HELP_NUM=30
export XMF_READ_FILE_CK="默认false" # ck文件为ZNS_ZD_ck.txt，格式为一行一个ck

变量:
RabbitToken： 机器人给你发的token
XMF_HELP_PIN：设置车头
XMF_CK_REVERSE：1：正序，2：反序，3：乱序
XMF_MAX_HELP_NUM：每个队伍的人数
XMF_READ_FILE_CK：读取ck文件，默认false，ck文件为XMF_ck.txt或ck.txt，格式为一行一个ck

log剩余次数大于5000方可使用
'''
import asyncio
import json
import os
from urllib.parse import quote

from utils.common import UserClass, printf, print_trace, TaskClass, print_api_error, wait, randomWait

XmfRewardList = os.environ.get("XmfRewardList", '').split(",")


class XMFUserClass(UserClass):
    def __init__(self, cookie):
        super(XMFUserClass, self).__init__(cookie)
        self.inviteCode = ""
        self.appname = "50091"
        self._help_num = None
        self.UA = self.jd_UA
        self.force_app_ck = True
        self.projectId = ''
        self.ProjectPoolId = ''
        self.giftProjectId = ''
        self.giftProjectPoolId = ''
        # self.force_app_ck = True
        self.risk = False
        self.mofang_exchage = True
        self.Origin = "https://h5.m.jd.com"
        self.referer = "https://h5.m.jd.com/pb/010631430/2bf3XEEyWG11pQzPGkKpKX2GxJz2/index.html"

    async def opt(self, opt):
        await self.set_joyytoken()
        # self.set_shshshfpb()
        _opt = {
            "method": "post",
            "api": "client.action",
            "log": False,
            "params": {
                "appid": "content_ecology",
                "client": "wh5",
                "clientVersion": "1.0.0",
            },
        }
        _opt.update(opt)
        return _opt

    def log_format(self, body, log_data):
        extParam = {
            "businessData": {
                "random": log_data['random']
            },
            "signStr": log_data['log'],
            "sceneid": "XMFhPageh5"
        }
        body.update({"extParam": extParam})
        return f"body={quote(json.dumps(body, separators=(',', ':')))}"

    async def getInteractionHomeInfo(self):
        body = {"sign": "u6vtLQ7ztxgykLEr"}
        opt = {
            "functionId": "getInteractionHomeInfo",
            "body": body,
            "log": True
        }
        status, res_data = await self.jd_api(await self.opt(opt))
        if res_data:
            if res_data['result'].get('giftConfig'):
                self.projectId = res_data['result']['taskConfig']['projectId']
                self.ProjectPoolId = res_data['result']['taskConfig']['projectPoolId']
                self.giftProjectId = res_data['result']['giftConfig']['projectId']
                self.giftProjectPoolId = res_data['result']['giftConfig']['projectPoolId']
            else:
                self.printf("获取projectId失败")
        else:
            print_api_error(opt, status)

    async def queryInteractiveInfo(self, reward=False, ext={}):
        try:
            body = {"encryptProjectId": self.projectId, "sourceCode": "acexinpin0823", "ext": ext}
            if reward:
                body = {
                    "encryptProjectId": self.giftProjectId,
                    "sourceCode": "acexinpin0823",
                    "ext": {"couponUsableGetSwitch": "1"}
                }
            opt = {
                "functionId": "queryInteractiveInfo",
                "body": body,
                'log': True
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            # data = json.loads(res.data.decode())
            if res_data:
                return res_data['assignmentList']
            else:
                print_api_error(opt, status)
                return []
        except:
            print_trace()
            return []

    async def doInteractiveAssignment(self, encryptAssignmentId, itemId, actionType=None, ext={}, reward=False,
                                completionFlag=""):
        try:
            body = {
                "encryptProjectId": self.projectId,
                "encryptAssignmentId": encryptAssignmentId,
                "sourceCode": "acexinpin0823",
                "itemId": itemId,
                "actionType": actionType,
                "completionFlag": completionFlag,
                "ext": ext,
            }
            if reward:
                body["encryptProjectId"] = self.giftProjectId
            opt = {
                "functionId": "doInteractiveAssignment",
                "body": body,
                "log": True
            }
            status, res_data = await self.jd_api(await self.opt(opt))
            if res_data:
                if reward and res_data.get("subCode"):
                    if res_data.get("subCode") == "0":
                        if not res_data["rewardsInfo"]["successRewards"].get("3"):
                            self.printf(f"兑换成功")
                        else:
                            prize = res_data["rewardsInfo"]["successRewards"]["3"][0]["rewardName"]
                            self.printf(f"恭喜你抽中：" + prize)
                    elif res_data.get("subCode") == "103":
                        self.printf(f"已经兑换过了")
                    elif res_data.get("subCode") == "1703":
                        self.printf(f"{res_data['msg']}")
                    else:
                        print_api_error(opt, status)
                else:
                    self.printf(f"{res_data['msg']}")
                if res_data['msg'] == "兑换积分不足":
                    self.mofang_exchage = False
                if res_data['msg'] == "未登录":
                    self.mofang_exchage = False
                    self.risk = True
                if "火爆" in res_data['msg']:
                    self.risk = True
                if "风控" in res_data['msg']:
                    self.risk = True
                if "风险" in res_data['msg']:
                    self.risk = True
            else:
                print_api_error(opt, status)
        except:
            print_trace()

    async def main(self):
        if not await self.is_login():
            self.printf("未登录")
            return
        await self.getInteractionHomeInfo()
        if not self.projectId:
            return
        taskList = await self.queryInteractiveInfo()
        if taskList:
            for vo in taskList:
                if vo.get("ext") and vo['ext'].get('extraType') != 'brandMemberList' and vo['ext'].get(
                        'extraType') != 'assistTaskDetail':
                    if vo.get('completionCnt', 0) < vo.get('assignmentTimesLimit', 0):
                        self.printf(
                            f"任务：{vo['assignmentName']}，进度：{vo['completionCnt']}/{vo['assignmentTimesLimit']}，去完成")
                        if self.risk:
                            self.printf(f"黑号了，跳过该账号")
                            return
                        if vo['ext']:
                            if vo['ext']['extraType'] == 'sign1':
                                await self.doInteractiveAssignment(vo['encryptAssignmentId'],
                                                             vo['ext']['sign1']['itemId'])

                        for vi in vo['ext'].get('productsInfo', []):
                            if self.risk:
                                self.printf(f"黑号了，跳过该账号")
                                return
                            if vi['status'] == 1 and vo['completionCnt'] < vo['assignmentTimesLimit']:
                                await self.doInteractiveAssignment(vo['encryptAssignmentId'], vi['itemId'], 1)
                                vo['completionCnt'] += 1
                                await randomWait(3, 3)

                        for vi in vo['ext'].get('shoppingActivity', []):
                            if self.risk:
                                self.printf(f"黑号了，跳过该账号")
                                return
                            if vi['status'] == 1 and vo['completionCnt'] < vo['assignmentTimesLimit']:
                                await self.doInteractiveAssignment(vo['encryptAssignmentId'], vi['advId'], 1)
                                await randomWait(vo['ext']['waitDuration'], 1)
                                if vo['ext']['waitDuration']:
                                    await self.doInteractiveAssignment(vo['encryptAssignmentId'], vi['advId'], 0)
                                vo['completionCnt'] += 1

                        for vi in vo['ext'].get('browseShop', []):
                            if self.risk:
                                self.printf(f"黑号了，跳过该账号")
                                return
                            if vi['status'] == 1 and vo['completionCnt'] < vo['assignmentTimesLimit']:
                                await self.doInteractiveAssignment(vo['encryptAssignmentId'], vi['itemId'], 1)
                                await randomWait(vo['ext']['waitDuration'], 1)
                                if vo['ext']['waitDuration']:
                                    await self.doInteractiveAssignment(vo['encryptAssignmentId'], vi['itemId'], 0)
                                vo['completionCnt'] += 1

                        for vi in vo['ext'].get('addCart', []):
                            if self.risk:
                                self.printf(f"黑号了，跳过该账号")
                                return
                            if vi['status'] == 1 and vo['completionCnt'] < vo['assignmentTimesLimit']:
                                await self.doInteractiveAssignment(vo['encryptAssignmentId'], vi['itemId'], 1)
                                await randomWait(3, 3)
                                vo['completionCnt'] += 1
                        await randomWait(3, 3)
                    else:
                        self.printf(
                            f"任务：{vo['assignmentName']}，进度：{vo['completionCnt']}/{vo['assignmentTimesLimit']}，已完成")
                elif vo.get("ext") and vo['ext'].get('extraType') == 'brandMemberList':
                    pass
                else:
                    if vo.get('completionCnt') is None:
                        self.printf("未登陆")
                        return
                    if vo.get('completionCnt', 0) < vo.get('assignmentTimesLimit', 0):
                        self.printf(
                            f"任务：{vo['assignmentName']}，进度：{vo.get('completionCnt', 0)}/{vo['assignmentTimesLimit']}，去完成")
                        for i in range(vo['assignmentTimesLimit']):
                            await randomWait(3, 3)
                            if vo.get('completionCnt', 0) < vo['assignmentTimesLimit']:
                                await self.doInteractiveAssignment(vo['encryptAssignmentId'], itemId=None, completionFlag=True)
                                vo['completionCnt'] += 1
                    else:
                        self.printf(
                            f"任务：{vo['assignmentName']}，进度：{vo['completionCnt']}/{vo['assignmentTimesLimit']}，已完成")
            else:
                self.printf(f"任务：做任务结束")
        else:
            self.printf(f'没有获取到活动信息')
        self.printf(f"--------->开始魔方兑换")
        res = await self.queryInteractiveInfo(True)
        for item in res:
            if self.risk:
                break
            if item["assignmentName"] == '魔方':
                i = -1
                while not self.risk and self.mofang_exchage:
                    await wait(8)
                    i += 1
                    await self.doInteractiveAssignment(item['encryptAssignmentId'], "", "", {"exchangeNum": 1},
                                                 reward=True)
                self.printf(f"成功兑换魔方数量:\t{i}")
                continue
            await randomWait(3, 3)
            exchange = True
            prize = [prize_item["rewardName"] for prize_item in item['rewards']]
            for prize_msg in prize:
                if "京豆" not in prize_msg:
                    exchange = False
            if not exchange:
                self.printf(f"奖品：{'/'.join(prize)}:\t不兑换")
                continue
            self.printf(f"奖品：{'/'.join(prize)}:\t去兑换")
            if XmfRewardList == ['']:
                await self.doInteractiveAssignment(item["encryptAssignmentId"], itemId='', ext={"exchangeNum": 1}, reward=True)
            else:
                if str(item["exchangeRate"]) in XmfRewardList:
                    await self.doInteractiveAssignment(item["encryptAssignmentId"], itemId='', ext={"exchangeNum": 1}, reward=True)
                else:
                    self.printf(f"设置的不兑换")
        printf("")


if __name__ == '__main__':
    task = TaskClass("task")
    task.name = 'XMF'
    task.init_config(XMFUserClass)
    asyncio.run(task.main("小魔方-任务"))
