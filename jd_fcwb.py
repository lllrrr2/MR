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

    def init(self):
        self.ua = self.default_jsb_ua
        headers = {
            "Cookie": self.cookie,
            "User-Agent": self.ua,
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://bnzf.jd.com",
            "referer": "https://bnzf.jd.com/?activityId=pTTvJeSTrpthgk9ASBVGsw&inviterId=&inviterCode=&utm_user=plusmember&ad_od=share&utm_source=androidapp&utm_medium=appshare&utm_campaign=t_335139774&utm_term=Wxfriends&lng=106.477132&lat=29.502772&sid=84c83c76030880654e4e98b6bcda688w&un_area=4_50952_106_0"
        }
        self.headers = headers

    @property
    def help_num(self):
        if self.black:
            return 0
        if not self._help_num:
            body = {
                "pageNum": 1,
                "pageSize": 50,
                "linkId": linkId
            }
            opt = {
                "functionId": "happyDigHelpList",
                "body": body,
                "appId": "ce6c2",
            }
            status, data = self.jd_api(self.opt(opt))
            if status == 200:
                if data["success"]:
                    pass
                    self._help_num = data['data'].get('personNum', 0)
                else:
                    self.black = True
            else:
                print_api_error(opt, status)
                self.black = True
        return self._help_num

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

    def home(self):
        body = {
            "linkId": linkId
        }
        opt = {
            "functionId": "happyDigHome",
            "body": body,
            "appId": "ce6c2",
        }
        status, res_data = self.jd_api(self.opt(opt))
        if res_data.get('code') == 0:
            if self.help_num < self.MAX_HELP_NUM:
                printf(f"账号[{self.Name}]未完成助力，至少留下一点血")
                self.minBlood = 1
            self.apTaskList()
            for item in res_data["data"]["roundList"]:
                if item['state'] == 1:
                    printf(f"关卡[{item['round']}] -- 已完成，已获得{item.get('cashAmount', 0)}现金，{item.get('redAmount', 0)}红包")
                else:
                    printf(f"关卡[{item['round']}] -- 未完成，已获得{item.get('cashAmount', 0)}现金，{item.get('redAmount', 0)}红包")
            for item in res_data["data"]["roundList"]:
                if item['state'] == 1:
                    continue
                if self.stopFlag:
                    break
                if self.blood < self.minBlood:
                    break
                self.prepareDig({"round": item['round']})
            self.spring_reward_list()
        else:
            self.black = True

    def spring_reward_list(self):
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
            }
            status, result = self.jd_api(self.opt(opt))
            if result.get('code') == 0:
                withdrawList = [item for item in result['data']['items'] if
                                item["prizeType"] == 4 and item["state"] == 0]
                length = len(withdrawList)
                counter = 1
                for item in withdrawList:
                    self.CashWithDraw(item)
                    if counter == length:
                        break
                    counter += 1
                    randomWait(8, 5)
            else:
                msg = result.get("errMsg", "")
                msg = result.get("message", msg)
                msg = result.get("echo", msg)
                if '未登录' in msg:
                    self.valid = False
                elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                    self.can_help = False
                    self.black = True
                printf(f"{self.Name}:\t查询奖励列表失败\t{msg}")
                print_api_error(opt, status)
        except:
            print_trace()

    def CashWithDraw(self, item):
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
                "method": 'POST'
            }
            status, result = self.jd_api(self.opt(opt))
            if result.get('code') == 0:
                printf(f"[{self.Name}]提现{item['amount']}元: {result['data'].get('message','成功')}")
            else:
                msg = result.get("errMsg", "")
                msg = result.get("message", msg)
                msg = result.get("echo", msg)
                if '未登录' in msg:
                    self.valid = False
                elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                    self.can_help = False
                    self.black = True
                printf(f"{self.Name}:\t查询奖励列表失败\t{msg}")
                print_api_error(opt, status)
        except:
            print_trace()

    def prepareDig(self, paramIn):
        try:
            body = {
                "linkId": linkId,
                "round": paramIn['round'],
            }
            opt = {
                "functionId": "happyDigHome",
                "body": body,
                "appId": "ce6c2",
            }
            status, result = self.jd_api(self.opt(opt))
            if result.get('code') == 0:
                self.roundStop = False
                self.blood = result['data']['blood']
                printf(f"开始第{paramIn['round']}关，血量: {self.blood}")
                for item in result['data']['roundList']:
                    if not item["chunks"]:
                        continue
                    chunkList = [chunks for chunks in item["chunks"] if not chunks["state"]]
                    random.shuffle(chunkList)
                    chunkListLen = len(chunkList)
                    counter = 1
                    for chunk in chunkList:
                        if self.blood <= self.minBlood:
                            printf(f"{self.Name}\t血量不足，退出")
                            break
                        param = {
                            "round": paramIn['round'],
                            "rowIdx": chunk['rowIdx'],
                            "colIdx": chunk['colIdx']
                        }
                        randomWait(1, 1)
                        self.happyDigDo(param)
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
                printf(f"{self.Name}:\t查询挖宝进度失败\t{msg}")
                print_api_error(opt, status)
        except:
            print_trace()

    def happyDigDo(self, paramIn):
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
            }
            status, result = self.jd_api(self.opt(opt))
            if result.get('code') == 0:
                strs = chunkConf[result['data']['chunk']['type']]
                printf(f"({paramIn['rowIdx']},{paramIn['colIdx']})挖到了{result['data']['chunk'].get('value', '')}{strs}")
                if result['data']['chunk']['type'] == 1:
                    printf(f"{self.Name}\t出现优惠券，不挖了")
                    self.stopFlag = True
                if result['data']['chunk']['type'] == 4:
                    self.blood -= 1
                    printf(f"{self.Name}\t血量：{self.blood}")
                if result['data'].get('lastPrize'):
                    self.roundStop = True
                    printf(
                        f"{self.Name}\t关卡[{paramIn['round']}]已完成，获得了{result['data']['cashAmount']}现金，{result['data']['redAmount']}红包")
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
                printf(f"{self.Name}:\t挖宝({paramIn['rowIdx']},{paramIn['colIdx']})失败\t{msg}")
                print_api_error(opt, status)
        except:
            print_trace()

    def doTask(self, task):
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
        }
        status, result = self.jd_api(self.opt(opt))
        if result.get('code') == 0:
            self.needNum -= 1
            printf(f"{self.Name}:\t完成任务[{task.get('itemName', task.get('taskShowTitle'))}]成功")
        else:
            msg = result.get("errMsg", "")
            msg = result.get("message", msg)
            msg = result.get("echo", msg)
            if '未登录' in msg:
                self.valid = False
            elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                self.can_help = False
                self.black = True
            printf(f"{self.Name}:\t完成任务失败\t{msg}")
            print_api_error(opt, status)

    def TaskDetail(self, task):
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
            }
            status, result = self.jd_api(self.opt(opt))
            if result.get('code') == 0:
                self.needNum = result['data']['status']['finishNeed'] - result['data']['status']['userFinishedTimes']
                for param in result['data']['taskItemList']:
                    param.update(task)
                    self.taskTimeRecord(param)
                    self.doTask(param)
                printf(f"{self.Name}:\t完成任务[{task.get('itemName', task.get('taskShowTitle'))}]成功")
            else:
                msg = result.get("errMsg", "")
                msg = result.get("message", msg)
                msg = result.get("echo", msg)
                if '未登录' in msg:
                    self.valid = False
                elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                    self.can_help = False
                    self.black = True
                printf(f"{self.Name}:\t查询任务[{task['taskShowTitle']}]失败\t{msg}")
                print_api_error(opt, status)
        except:
            print_trace()

    def taskTimeRecord(self, task):
        try:
            body = {
                "linkId": linkId,
                "taskId": task['id'],
            }
            opt = {
                "functionId": "apTaskTimeRecord",
                "body": body,
                "appId": "ce6c2",
            }
            status, result = self.jd_api(self.opt(opt))
            if result.get('code') == 0:
                printf(
                    f"{self.Name}:\t开始任务[{task.get('itemName', task.get('taskShowTitle'))}]，需要等待{result['data']['timePeriod']}秒")
                wait(result['data'].get('timePeriod', 0))
            else:
                msg = result.get("errMsg", "")
                msg = result.get("message", msg)
                msg = result.get("echo", msg)
                if '未登录' in msg:
                    self.valid = False
                elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                    self.can_help = False
                    self.black = True
                printf(f"{self.Name}:\t开始任务[{task.get('itemName', task.get('taskShowTitle'))}]失败\t{msg}")
                print_api_error(opt, status)
        except:
            print_trace()

    def apTaskList(self):
        try:
            body = {
                "linkId": linkId
            }
            opt = {
                "functionId": "apTaskList",
                "body": body,
                "appId": "ce6c2",
            }
            status, result = self.jd_api(self.opt(opt))
            if result.get('success'):
                for item in result['data']:
                    if item['taskFinished']:
                        printf(f"任务[{item['taskShowTitle']}] -- 已完成，{item['taskDoTimes']}/{item['taskLimitTimes']}")
                    else:
                        printf(f"任务[{item['taskShowTitle']}] -- 未完成，{item['taskDoTimes']}/{item['taskLimitTimes']}")
                    if not item['taskFinished'] and "BROWSE_CHANNEL" in item['taskType']:
                        if item.get('taskSourceUrl'):
                            self.doTask(item)
                        else:
                            self.TaskDetail(item)
            else:
                msg = result.get("errMsg", "")
                msg = result.get("message", msg)
                msg = result.get("echo", msg)
                if '未登录' in msg:
                    self.valid = False
                elif '上限' in msg or '火爆' in msg or '邀请过' in msg:
                    self.can_help = False
                    self.black = True
                printf(f"{self.Name}:\t查询挖宝任务失败\t{msg}")
                print_api_error(opt, status)
        except:
            print_trace()

    def main(self):
        self.home()
        printf("\n\n")


if __name__ == '__main__':
    task = TaskClass("task")
    task.MAX_HELP_NUM = 40
    task.name = 'FCWB'
    task.init_config(FcwbUserClass)
    task.main("发财挖宝-任务")
