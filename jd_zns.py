'''
new Env('炸年兽-2023');
export RabbitToken="token值"
export ZNS_CK_REVERSE="1 或 2 或 3"
export ZNS_HELP_PIN="1~3或pin1,pin2,pin3或者ALL"
export ZNS_MAX_HELP_NUM=30
export ZNS_READ_FILE_CK="默认false" # ck文件为ZNS_ZD_ck.txt，格式为一行一个ck

变量:
RabbitToken： 机器人给你发的token
ZNS_HELP_PIN：设置车头
ZNS_CK_REVERSE：1：正序，2：反序，3：乱序
ZNS_MAX_HELP_NUM：每个队伍的人数
ZNS_READ_FILE_CK：读取ck文件，默认false，ck文件为ZNS_ZD_ck.txt，格式为一行一个ck

log剩余次数大于5000方可使用
'''
import json

from utils.common import UserClass, print_trace, print_api_error, printf, wait, randomWait, TaskClass


class ZnsUserClass(UserClass):
    def __init__(self, cookie):
        super(ZnsUserClass, self).__init__(cookie)
        self.appname = "50174"
        self._help_num = None
        self.maxLevel = False
        self.secretpInfo = {}
        self.secretp = ""
        self.homeData = {}
        self.homeMainInfo = {}
        self.raiseInfo = {}
        self.signHomeData = {}
        self.taskList = []
        self.lotteryTaskVos = []
        self.fullFlag = False
        self.toTaskFlag = False
        self.Origin = "https://wbbny.m.jd.com"
        self.referer = "https://wbbny.m.jd.com/"

    def opt(self, opt):
        self.set_joyytoken()
        self.set_shshshfpb()
        _opt = {
            "method": "post",
            "log": False,
            # "api": "client.action",
            "body_param": {
                "appid": "signed_wh5",
                "client": "m",
                "clientVersion": "-1",
                "functionId": opt['functionId']
            }
        }
        _opt.update(opt)
        return _opt

    def log_format(self, body, log_data):
        body.update({"log": log_data["log"]})
        body.update({"random": log_data["random"]})
        # body = f"body={json.dumps(body, separators=(',', ':'))}"
        body = {
            "body": json.dumps(body, separators=(',', ':'))
        }
        return body

    def promote_getHomeData(self):
        try:
            opt = {
                "functionId": "promote_getHomeData"
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    self.homeData = result['data']
                    self.secretp = result['data']['result']['homeMainInfo']['secretp']
                    self.secretpInfo[self.pt_pin] = self.secretp
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(f"{msg}")
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                    self.black = True
                self.printf(f"{msg}")
        except:
            print_trace()

    def promote_getMainMsgPopUp(self):
        try:
            body = {"channel": "1"}
            opt = {
                "functionId": "promote_getMainMsgPopUp",
                "body": body,
                "log": True
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    pass
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(f"{msg}")
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(f"{msg}")
        except:
            print_trace()

    def promote_getTaskDetail(self, show_help_code=False, body={}):
        try:
            opt = {
                "functionId": "promote_getTaskDetail",
                "body": body,
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    if show_help_code:
                        self.printf(f"互助码：{result['data']['result'].get('inviteId', '助力已满，获取助力码失败')}\n")
                    self.taskList = result['data']['result'].get('taskVos', [])
                    self.lotteryTaskVos = result['data']['result'].get('lotteryTaskVos', [])
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(f"{msg}")
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(f"{msg}")
        except:
            print_trace()

    def promote_sign(self):
        try:
            body = {}
            opt = {
                "functionId": "promote_sign",
                "body": body,
                "log": True
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    self.toheihao = 0
                    if result['data']['result'].get("redPacketValue"):
                        self.printf(f"签到获得：{result['data']['result']['redPacketValue']} 红包")
                    elif result['data']['result'].get("scoreResult"):
                        self.printf(f"签到获得：{result['data']['result']['scoreResult']['score']} 金币")
                    else:
                        self.printf(f"签到成功")
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(f"签到失败")
                    self.printf(f"{msg}")
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(f"{msg}")
        except:
            print_trace()

    def promote_getSignHomeData(self):
        try:
            body = {}
            opt = {
                "functionId": "promote_getSignHomeData",
                "body": body,
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    self.signHomeData = result['data']['result']
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(msg)
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(msg)
        except:
            print_trace()

    def promote_collectAutoScore(self):
        try:
            body = {}
            opt = {
                "functionId": "promote_collectAutoScore",
                "body": body,
                "log": True
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    self.printf(f"收取成功，获得：{result['data']['result']['produceScore']}")
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(msg)
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(msg)
        except:
            print_trace()

    def promote_getBadgeAward(self, awardToken):
        try:
            body = {"awardToken": awardToken}
            opt = {
                "functionId": "promote_getBadgeAward",
                "body": body,
                "body_param": {
                    "appid": "signed_wh5",
                    "client": "wh5",
                    "clientVersion": "1.0.0",
                }
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    myAwardVos = result['data']['result']['myAwardVos']
                    for i in myAwardVos:
                        if i['type'] == 15:
                            msg = f"获得：{i['pointVo']['score']}金币"
                        elif i['type'] == 1:
                            msg = f"获得：优惠券：{i['couponVo']['usageThreshold']}-{i['couponVo']['quota']}\t{i['couponVo']['useRange']}"
                        else:
                            msg = f"获得：{str(i)}"
                        self.printf(msg)
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(msg)
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(msg)
        except:
            print_trace()

    def promote_getFeedDetail(self, taskId):
        feedDetailInfo = []
        try:
            body = {"taskId": taskId}
            opt = {
                "functionId": "promote_getFeedDetail",
                "body": body,
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    if result['data']['result'].get('addProductVos') and result['data']['result'].get('addProductVos')[0]:
                        feedDetailInfo = result['data']['result'].get('addProductVos')[0]
                    if result['data']['result'].get('taskVos') and result['data']['result'].get('taskVos')[0]:
                        feedDetailInfo = result['data']['result'].get('taskVos')[0]
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(msg)
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(msg)
        except:
            print_trace()
        return feedDetailInfo

    def promote_collectScore(self, body):
        callbackInfo = {}
        try:
            opt = {
                "functionId": "promote_collectScore",
                "body": body,
                "log": True
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                callbackInfo = result
                if result.get("data") and result['data'].get('bizCode') == 0:
                    if result['data']['result'].get("successToast"):
                        self.printf(f"{result['data']['result'].get('successToast')}")
                    elif result['data']['result'].get("score") == '0':
                        self.printf(f"已完成({result['data']['result'].get('times')}/{result['data']['result'].get('maxTimes')})")
                    elif result['data']['result'].get("score", None) is None:
                        pass
                    else:
                        self.printf(f"任务完成，获得{result['data']['result'].get('score')}金币")
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    self.printf(msg)
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(msg)
        except:
            print_trace()
        return callbackInfo

    def promote_getWelfareScore(self):
        try:
            body = {"type": self.shareType}
            opt = {
                "functionId": "promote_getWelfareScore",
                "body": body,
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    if result["data"]["result"]["times"] < result["data"]["result"]["maxTimes"]:
                        self.printf(f'奖励：{result["data"]["result"]["score"]}金币')
                    else:
                        self.printf("分享已达上限")
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    self.printf(f"{msg}")
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(f"{msg}")
        except:
            print_trace()

    def promote_raise(self, scenceId):
        try:
            body = {"scenceId": scenceId}
            opt = {
                "functionId": "promote_raise",
                "body": body,
                "log": True
            }
            status, result = self.jd_api(self.opt(opt))
            if result and result.get("code") == 0:
                if result.get("data") and result['data'].get('bizCode') == 0:
                    self.toheihao = 0
                    self.toTaskFlag = True
                    self.raiseFlag = True
                    card = result["data"]["result"]["levelUpAward"].get("name")
                    couponInfo = result["data"]["result"]["levelUpAward"].get("couponInfo")
                    redNum = result["data"]["result"]["levelUpAward"].get("redNum")
                    type_ = result["data"]["result"]["levelUpAward"]["type"]
                    postcardScore = result["data"]["result"]["levelUpAward"]["postcardScore"]
                    # logger.info(res)
                    if type_ in [1, 2, 4, 5]:
                        if couponInfo:
                            self.printf(
                                f'奖励: 满{float(couponInfo["usageThreshold"])}-{float(couponInfo["quota"])}优惠券, 有效期:{couponInfo["desc"]}')
                        if redNum:
                            self.printf(f'奖励: {redNum}份红包')
                        if postcardScore:
                            self.printf(f'奖励: {postcardScore}金币')
                    elif type_ == 2:
                        self.printf(f'奖励: {card["name"]}')
                    else:
                        printf(str(result))
                else:
                    msg = result['data']['bizMsg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    print_api_error(opt, status)
                    self.printf(f"{msg}")
            else:
                msg = result['msg']
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                self.printf(f"{msg}")
        except:
            print_trace()

    def sceneInfo(self):
        for i in self.raiseInfo['scenceMap']['sceneInfo']:
            if type(i.get("lightCardNum")) == int and type(i.get("totalCardNum")) == int:
                self.printf(f"{i['name']}\t({i.get('lightCardNum')}/{i.get('totalCardNum')})")
                if i.get('lightCardNum') < i.get('totalCardNum'):
                    return i
            else:
                # self.printf(f"{i['name']}\t未解锁")
                pass
        else:
            return {}

    def main(self):
        self.printf("\n开始执行！")
        self.promote_getHomeData()
        if self.black:
            return
        self.promote_getMainMsgPopUp()

        if self.homeData.get("result"):
            self.homeMainInfo = self.homeData['result']['homeMainInfo']
            self.raiseInfo = self.homeMainInfo['raiseInfo']
            self.fullFlag = self.raiseInfo.get('fullFlag', False)
            if not self.fullFlag:
                self.printf(f"分红:{self.raiseInfo['redInfo']['red']}份 金币:{self.raiseInfo['totalScore']} {self.raiseInfo['produceResult']['produceScore']}金币待领取")
            self.printf(f"当前场景\t 解锁状态")
            for i in self.raiseInfo['scenceMap']['sceneInfo']:
                if i.get("lightCardNum") and i.get("totalCardNum"):
                    self.printf(f"{i['name']}\t({i.get('lightCardNum')}/{i.get('totalCardNum')})")
                else:
                    pass
                    # self.printf(f"{i['name']}\t未解锁")
            else:
                self.printf(f"离分红还差: \t{str(self.raiseInfo['scenceMap']['redNum']['nextNum'])}")
            self.promote_collectAutoScore()
        self.promote_getSignHomeData()
        signNum = 0
        for i in self.signHomeData.get('signNodes', {}):
            if i["status"]:
                signNum += 1
        self.printf(f"已累计签到{signNum}/{len(self.signHomeData['signNodes'])}天，还需签到{len(self.signHomeData['signNodes']) - signNum}天")
        if self.signHomeData['todayStatus'] == 0:
            if not self.black:
                self.promote_sign()
            randomWait(1, 1)

        # 满级
        if self.fullFlag == True:
            self.printf(f"已经满级，等待开奖！")
            return

        if not self.black:
            self.promote_getTaskDetail(True)

        if self.lotteryTaskVos and self.lotteryTaskVos[0]:
            self.printf(f"累计任务奖励-当前进度{self.lotteryTaskVos[0]['times']}/{self.lotteryTaskVos[0]['maxTimes']}")
            for i in range(len(self.lotteryTaskVos[0]['badgeAwardVos'])):
                oneTask = self.lotteryTaskVos[0]['badgeAwardVos'][i]
                if oneTask["status"] == 3:
                    awardToken = oneTask['awardToken']
                    self.promote_getBadgeAward(awardToken)
                    randomWait(1, 1)
                if self.black:
                    break

        self.toheihao = 0

        toTaskCount = 0
        while not self.toTaskFlag and toTaskCount < 10:
            toTaskCount += 1
            printf("")
            self.printf(f"开始第{toTaskCount}轮任务")
            self.toTaskFlag = True
            for i in range(len(self.taskList)):
                oneTask = self.taskList[i]
                if oneTask["taskType"] in [5] and oneTask['status'] == 1 and "种草" in oneTask['taskName']:
                    self.printf(f"做任务:\t{oneTask['taskName']}")
                    taskId = oneTask['taskId']
                    feedDetailInfo = self.promote_getFeedDetail(taskId)
                    productList = feedDetailInfo.get("browseShopVo", [])
                    needTime = int(feedDetailInfo.get('maxTimes', 0)) - int(feedDetailInfo.get('times', 0))
                    for j in range(len(productList)):
                        if self.black:
                            break
                        if needTime <= 0:
                            break
                        if productList[j]['status'] != 1:
                            continue
                        oneActivityInfo = productList[j]
                        body = {"taskId": taskId, "taskToken": oneActivityInfo['taskToken']}
                        self.promote_collectScore(body)
                        randomWait(3, 2)
                        needTime -= 1
                        self.toTaskFlag = False

                elif oneTask["taskType"] in [1, 3, 5, 7, 9, 21, 26] and oneTask['status'] == 1:
                    if oneTask.get("shoppingActivityVos"):
                        activityInfoList = oneTask.get("shoppingActivityVos")
                    elif oneTask.get("brandMemberVos"):
                        activityInfoList = oneTask.get("brandMemberVos")
                    elif oneTask.get("followShopVo"):
                        activityInfoList = oneTask.get("followShopVo")
                    elif oneTask.get("browseShopVo"):
                        activityInfoList = oneTask.get("browseShopVo")
                    elif oneTask.get("productInfoVos"):
                        activityInfoList = oneTask.get("productInfoVos")
                    else:
                        activityInfoList = []
                    times = oneTask.get('times', 0)
                    for j in range(len(activityInfoList)):
                        times += 1
                        oneActivityInfo = activityInfoList[j]
                        if oneActivityInfo['status'] != 1 or not oneActivityInfo.get("taskToken"):
                            continue
                        taskname = ""
                        if oneActivityInfo.get('title'):
                            taskname = oneActivityInfo.get('title')
                        if oneActivityInfo.get('taskName'):
                            taskname = oneActivityInfo.get('taskName')
                        if oneActivityInfo.get('shopName'):
                            taskname = oneActivityInfo.get('shopName')
                        if oneActivityInfo.get('skuName'):
                            taskname = oneActivityInfo.get('skuName')
                        if oneTask['taskType'] == 21:
                            channel = oneActivityInfo['memberUrl']
                            if toTaskCount > 1:
                                continue
                        self.toTaskFlag = False
                        self.printf(f"去做任务：{taskname}")
                        waitDuration = oneTask.get('waitDuration', 0)
                        body = {"taskId": oneTask['taskId'], "taskToken": oneActivityInfo['taskToken'], "actionType": 1}
                        callbackInfo = self.promote_collectScore(body)
                        if callbackInfo.get('code') == 0 and callbackInfo['data'] and callbackInfo['data'].get('result') and callbackInfo['data']['result'].get('taskToken'):
                            self.printf(f"等待{waitDuration}s")
                            randomWait(waitDuration, 1)
                            body = {"taskId": oneTask['taskId'], "taskToken": oneActivityInfo['taskToken'],
                                    "actionType": 0}
                            self.promote_collectScore(body)
                        elif callbackInfo.get('code') == 0 and callbackInfo['data'] and callbackInfo['data'].get('result') and callbackInfo['data']['bizCode'] == 0:
                            # self.printf(f"任务完成，获得{callbackInfo['data']['result']['score']}金币")
                            pass
                        if self.black or times >= oneTask["maxTimes"]:
                            break
                        randomWait(3, 2)

                elif oneTask["taskType"] in [2] and oneTask['status'] == 1 and \
                        oneTask['scoreRuleVos'][0]['scoreRuleType'] == 2:
                    self.printf(f"做任务2：{oneTask['taskName']}")
                    taskId = oneTask['taskId']
                    feedDetailInfo = self.promote_getFeedDetail(taskId)
                    productList = {}
                    if feedDetailInfo.get("browseShopVo"):
                        productList = feedDetailInfo.get("browseShopVo", [])
                    if feedDetailInfo.get("productInfoVos"):
                        productList = feedDetailInfo.get("productInfoVos", [])
                    needTime = int(feedDetailInfo.get('maxTimes', 0)) - int(feedDetailInfo.get('times', 0))
                    for j in range(len(productList)):
                        if self.black:
                            break
                        if needTime <= 0:
                            break
                        if productList[j]['status'] != 1:
                            continue
                        taskToken = productList[j]['taskToken']
                        body = {"taskId": taskId, "taskToken": taskToken}
                        self.promote_collectScore(body)
                        randomWait(3, 2)
                        needTime -= 1
                        self.toTaskFlag = False

                elif oneTask["taskType"] in [8] and oneTask['status'] == 1 and \
                        oneTask['scoreRuleVos'][0]['scoreRuleType'] == 2:
                    activityInfoList = oneTask.get('productInfoVos', [])
                    times = oneTask.get('times', 0)
                    for j in range(len(activityInfoList)):
                        times += 1
                        oneActivityInfo = activityInfoList[j]
                        if oneActivityInfo['status'] != 1 or not oneActivityInfo.get("taskToken"):
                            continue
                        taskname = oneActivityInfo['skuName']
                        waitDuration = oneActivityInfo.get('waitDuration', 0)
                        self.printf(f"去做任务4：浏览{taskname}")
                        body = {"taskId": oneTask['taskId'], "taskToken": oneActivityInfo['taskToken'], "actionType": 1}
                        callbackInfo = self.promote_collectScore(body)
                        if callbackInfo['code'] == 0 and callbackInfo['data'] and callbackInfo['data']['result'] and callbackInfo['data']['result'].get('taskToken'):
                            self.printf(f"等待{waitDuration}s")
                            randomWait(waitDuration, 1)
                            body = {"taskId": oneTask['taskId'], "taskToken": oneActivityInfo['taskToken'],
                                    "actionType": 0}
                            self.promote_collectScore(body)
                        if self.black or times >= oneTask["maxTimes"]:
                            break
                        randomWait(3, 2)
                        self.toTaskFlag = False

                elif oneTask['status'] == 3 or '去首页' in oneTask['taskName'] or '打卡' in oneTask['taskName'] or '去APP' in oneTask['taskName']:
                    taskId = oneTask['taskId']
                    oneActivityInfo = oneTask['simpleRecordInfoVo']
                    if taskId and oneActivityInfo:
                        self.printf(f"领取：{oneTask['subTitleName']}")
                        body = {"taskId": oneTask['taskId'], "taskToken": oneActivityInfo['taskToken'],
                                "actionType": 0}
                        self.promote_collectScore(body)
                        randomWait(3, 2)
                        self.toTaskFlag = False

                elif '品牌墙' in oneTask['taskName']:
                    taskId = oneTask['taskId']
                    oneActivityInfo = oneTask['simpleRecordInfoVo']
                    if taskId and oneActivityInfo:
                        self.printf(f"领取：{oneTask['subTitleName']}")
                        body = {"taskId": oneTask['taskId'], "taskToken": oneActivityInfo['taskToken'],
                                "actionType": 1}
                        self.promote_collectScore(body)
                        randomWait(3, 2)
                        body = {"taskId": oneTask['taskId'], "taskToken": oneActivityInfo['taskToken']}
                        self.promote_collectScore(body)
                        randomWait(3, 2)
                        self.toTaskFlag = False

            if self.black:
                break

            if not self.toTaskFlag and toTaskCount <= 100:
                self.promote_getTaskDetail()

            if self.toTaskFlag:
                self.printf(f"任务都做完了")
                break

        ## 微信任务
        self.taskList = []
        if not self.black and not self.maxLevel:
            self.promote_getTaskDetail(body={"appSign": 2})
        if not self.black:
            printf("")
            self.printf(f"去做微信任务")
        for oneTask in self.taskList:
            if oneTask['taskType'] == 2 or oneTask['status'] != 1:
                continue
            activityInfoList = []
            if oneTask.get("shoppingActivityVos"):
                activityInfoList = oneTask.get("shoppingActivityVos")
            if oneTask.get("brandMemberVos"):
                activityInfoList = oneTask.get("brandMemberVos")
            if oneTask.get("followShopVo"):
                activityInfoList = oneTask.get("followShopVo")
            if oneTask.get("browseShopVo"):
                activityInfoList = oneTask.get("browseShopVo")
            times = oneTask.get('times', 0)
            for oneActivityInfo in activityInfoList:
                times += 1
                if oneActivityInfo['status'] != 1 or not oneActivityInfo.get("taskToken"):
                    continue
                taskname = ""
                if oneActivityInfo.get('title'):
                    taskname = oneActivityInfo.get('title')
                if oneActivityInfo.get('taskName'):
                    taskname = oneActivityInfo.get('taskName')
                if oneActivityInfo.get('shopName'):
                    taskname = oneActivityInfo.get('shopName')
                self.printf(f"去做任务：{taskname}")
                waitDuration = oneTask.get('waitDuration', 6)
                body = {"taskId": oneTask['taskId'], "taskToken": oneActivityInfo['taskToken'],
                        "actionType": 1}
                callbackInfo = self.promote_collectScore(body)
                if callbackInfo.get('code') == 0 and callbackInfo['data'] and callbackInfo['data']['success'] and callbackInfo['data']['result'].get('taskToken'):
                    self.printf(f"等待{waitDuration}s")
                    randomWait(waitDuration, 1)
                    body = {"taskId": oneTask['taskId'], "taskToken": oneActivityInfo['taskToken']}
                    self.promote_collectScore(body)

                if self.black or times >= oneTask["maxTimes"]:
                    break
                randomWait(3, 2)
        else:
            self.printf(f"任务都做完了")

        ## 分享任务1
        if not self.black:
            self.printf(f"去做分享任务1")
        shareCount = 0
        self.shareType = 1
        self.shareFlag = True
        while not self.black and self.shareFlag and shareCount < 10:
            self.shareFlag = False
            shareCount += 1
            if not self.black:
                self.promote_getWelfareScore()
            randomWait(3, 2)
        ## 分享任务2
        if not self.black:
            self.printf(f"去做分享任务2")
        shareCount = 0
        self.shareType = 2
        self.shareFlag = True
        while not self.black and self.shareFlag and shareCount < 20:
            self.shareFlag = False
            shareCount += 1
            if not self.black:
                self.promote_getWelfareScore()
            randomWait(3, 2)

        self.promote_getHomeData()

        if self.homeData['result']:
            printf("")
            self.printf("开始升级")
            self.homeMainInfo = self.homeData['result']['homeMainInfo']
            self.raiseInfo = self.homeMainInfo['raiseInfo']
            self.toTaskFlag = True
            self.raiseFlag = True
            self.scenceMap = self.raiseInfo['scenceMap']['sceneInfo']
            sceneInfo = self.sceneInfo()
            self.nextLevelScore = self.raiseInfo['scenceMap']['redNum']['nextLevelScore']
            while int(self.raiseInfo['totalScore']) >= int(self.nextLevelScore) and self.toTaskFlag and self.raiseFlag:
                self.printf(f"当前金币：{self.raiseInfo['totalScore']} 解锁「{sceneInfo['name']}」需要：{self.raiseInfo['scenceMap']['redNum']['nextLevelScore']}")
                self.raiseFlag = False
                self.promote_raise(sceneInfo['scenceId'])
                self.promote_getHomeData()
                self.homeMainInfo = self.homeData['result']['homeMainInfo']
                self.raiseInfo = self.homeMainInfo['raiseInfo']
                self.scenceMap = self.raiseInfo['scenceMap']['sceneInfo']
                sceneInfo = self.sceneInfo()
                self.nextLevelScore = self.raiseInfo['scenceMap']['redNum']['nextLevelScore']
                randomWait(3, 2)
                self.printf(
                    f"分红:{self.raiseInfo['redInfo']['red']}份金币:{self.raiseInfo['totalScore']} {self.raiseInfo['produceResult']['produceScore']}金币待领取")
            else:
                self.printf("升级结束")


if __name__ == '__main__':
    task = TaskClass("task")
    task.name = 'ZNS'
    task.need_appck = True
    task.FORCE_XCX_CK = True
    task.init_config(ZnsUserClass)
    task.main("炸年兽-2023")
