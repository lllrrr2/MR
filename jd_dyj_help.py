'''
new Env('大赢家-助力');
export RabbitToken="token值"
export DYJ_HELP_CK_REVERSE="1 或 2 或 3"
export DYJ_HELP_HELP_PIN="1~3或pin1,pin2,pin3或者ALL"
export DYJ_HELP_MAX_HELP_NUM=30
export DYJ_HELP_READ_FILE_CK="默认false" # ck文件为DYJ_HELP_ck.txt，格式为一行一个ck

变量:
RabbitToken： 机器人给你发的token
DYJ_HELP_HELP_PIN：设置车头
DYJ_HELP_CK_REVERSE：1：正序，2：反序，3：乱序
DYJ_HELP_MAX_HELP_NUM：每个队伍的人数
DYJ_HELP_READ_FILE_CK：读取ck文件，默认false，ck文件为DYJ_HELP_ck.txt，格式为一行一个ck
'''
import json
import time

from utils.common import UserClass, printf, print_api_error, print_trace, TaskClass

linkId = "pTTvJeSTrpthgk9ASBVGsw"


class DyjUserClass(UserClass):
    def __init__(self, cookie):
        super(DyjUserClass, self).__init__(cookie)
        self.curRound = ""
        self.inviteCode = ""
        self.inviter = ""
        self.blood = ""
        self._help_num = None
        self.UA = self.lite_UA
        self.H5ST_VERSION = '400'
        self.task_num = 0
        self.canUseCoinAmount = 0
        self.task_list = []
        self.Origin = "https://wqs.jd.com"
        self.referer = "https://wqs.jd.com/sns/202210/20/make-money-shop/bridge.html?type=sign&activeId=63526d8f5fe613a6adb48f03&bridgeType=sign&sharefromapp=jdltapp&channel=superjd-m-makemoneyking-hudong&utm_source=iosapp&utm_medium=liteshare&utm_campaign=t_335139774&utm_term=Wxfriends&ad_od=share"

    def init(self):
        self.ua = self.default_jsb_ua
        headers = {
            "Cookie": self.cookie,
            "User-Agent": self.ua,
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        }
        self.headers = headers

    def opt(self, opt):
        _opt = {
            "method": "get",
            "appId": "638ee",
            "h5st": True,
            'host': "api.m.jd.com",
        }
        _opt.update(opt)
        return _opt

    def searchParams(self, searchParams):
        _searchParams = {
            "client": "jxh5",
            "clientVersion": "1.2.5",
            "appid": "jdlt_h5",
        }
        _searchParams.update(searchParams)
        return _searchParams

    # @property
    # def cookie(self):
    #     return f"pt_key={self.pt_key}; "

    def GetUserTaskStatusList(self):
        try:
            opt = {
                'h5st': False,
                'host': "wq.jd.com",
                'api': "newtasksys/newtasksys_front/GetUserTaskStatusList",
                'params': {
                    'g_ty': 'h5',
                    'g_tk': '',
                    'appCode': 'ms2362fc9e',
                    'source': 'makemoneyshop',
                    'bizCode': 'makemoneyshop',
                    'sceneval': '2',
                    'callback': '',
                }
            }
            status, data = self.jd_api(self.opt(opt))
            if status == 200:
                if data.get("ret") == 0:
                    userTaskStatusList = data['data']['userTaskStatusList']
                    self.task_list = userTaskStatusList
                    for userTask in userTaskStatusList:
                        if userTask['taskName'] == '邀请好友打卡':
                            self.task_num = userTask.get('realCompletedTimes', 0)
                            self._help_num = userTask.get('realCompletedTimes', 0)
                            now_num = userTask.get('completedTimes', 0)
                            self.MAX_HELP_NUM = userTask.get('configTargetTimes', self.MAX_HELP_NUM)
                            if self._help_num > 0 and now_num != self.MAX_HELP_NUM:
                                self.Award()
                            break
                    else:
                        self._help_num = 0
                else:
                    self._help_num = 0
                    self.black = True
            else:
                self._help_num = 0
                print_api_error(opt, status)
                self.black = True
        except:
            print_trace()

    def DoTask(self, taskId, taskName):
        try:
            opt = {
                'h5st': False,
                'host': "wq.jd.com",
                'api': "newtasksys/newtasksys_front/DoTask",
                'params': {
                    'g_ty': 'h5',
                    'g_tk': '',
                    'appCode': 'ms2362fc9e',
                    'source': 'makemoneyshop',
                    'bizCode': 'makemoneyshop',
                    'sceneval': '2',
                    'taskId': taskId,
                    'callback': '',
                    'h5st': '20230119225600864;5219169360582943;d06f1;tk02wae5f1c1f18nmV9AwaxBqSNxr3f4ns49WBzZerSHVECYiMx7Q+2xvIYDo1uI+W5g6mk9q+6yljxo9Z1bITgaNFUm;ca949ed626665e4dca220401758f3bba6a8a68652c9a3df5353eb2a58ded8aa1;3.1;1674140160864;62f4d401ae05799f14989d31956d3c5f27ba522a81bb61f6036f822a201e8a46c425d839884fb6c550233f3a888e0a531d8be989ced68adf2195cc96c1dfe63a6fe9d2a426fb57ec5d28675c4c85a8c53b0999777f5a4084547ad0bd8a32da959b2455ca72703258c672e7450a8014c32d142cbdfe3b783bbe5384956ac0e3ce3e712b21ce0fb3937fa53c80649dfa95',
                }
            }
            status, data = self.jd_api(self.opt(opt))
            if status == 200:
                if data.get("ret") == 0:
                    self.printf(f"【{taskName}】\t任务完成")
                else:
                    msg = data.get("msg", '')
                    self.printf(f"【{taskName}】\t{msg}")
            else:
                self._help_num = 0
                print_api_error(opt, status)
                self.black = True
        except:
            print_trace()

    def home(self):
        try:
            self.GetUserTaskStatusList()
            for task in self.task_list:
                do_task_type = [1, 2, 5]
                if task['realCompletedTimes'] < task['configTargetTimes'] and task['taskType'] == 2:
                    self.DoTask(task['taskId'], task['taskName'])
                    self.Award(task['taskId'], task['taskName'])
                if task['taskType'] in do_task_type and task['awardStatus'] == 2 and task['realCompletedTimes'] > 0:
                    if task['configTargetTimes'] != task['realCompletedTimes']:
                        for i in range(task['configTargetTimes'] - task['realCompletedTimes']):
                            if not self.Award(task['taskId'], task['taskName']):
                                break
                    else:
                        self.Award(task['taskId'], task['taskName'])
        except:
            print_trace()

    @property
    def help_num(self):
        if self._help_num == None:
            self.GetUserTaskStatusList()
        return self._help_num

    @help_num.setter
    def help_num(self, value):
        self._help_num = value

    def Award(self, taskId='3533', tip='邀请好友打卡'):
        opt = {
            # 'h5st': False,
            'host': "wq.jd.com",
            'appId': 'd06f1',
            'api': "/newtasksys/newtasksys_front/Award",
            'params': {
                'g_ty': 'h5',
                'g_tk': '',
                'appCode': 'ms2362fc9e',
                'source': 'makemoneyshop',
                'bizCode': 'makemoneyshop',
                'sceneval': '2',
                'taskId': taskId,
                'isSecurity': True,
                'callback': '',
                # 'h5st': '20230119225600864;5219169360582943;d06f1;tk02wae5f1c1f18nmV9AwaxBqSNxr3f4ns49WBzZerSHVECYiMx7Q+2xvIYDo1uI+W5g6mk9q+6yljxo9Z1bITgaNFUm;ca949ed626665e4dca220401758f3bba6a8a68652c9a3df5353eb2a58ded8aa1;3.1;1674140160864;62f4d401ae05799f14989d31956d3c5f27ba522a81bb61f6036f822a201e8a46c425d839884fb6c550233f3a888e0a531d8be989ced68adf2195cc96c1dfe63a6fe9d2a426fb57ec5d28675c4c85a8c53b0999777f5a4084547ad0bd8a32da959b2455ca72703258c672e7450a8014c32d142cbdfe3b783bbe5384956ac0e3ce3e712b21ce0fb3937fa53c80649dfa95',
            },
            "searchParams": self.searchParams({
                'g_ty': 'h5',
                'g_tk': '',
                'appCode': 'ms2362fc9e',
                'source': 'makemoneyshop',
                'bizCode': 'makemoneyshop',
                'sceneval': '2',
                'taskId': taskId,
                'isSecurity': True,
                'callback': '',
            })
        }
        status, res_data = self.jd_api(self.opt(opt))
        if res_data.get("ret") == 0:
            self.canUseCoinAmount += int(res_data['data']['prizeInfo']) / 100
            self.printf(f"{tip}获得:\t{int(res_data['data']['prizeInfo']) / 100}")
            return True
        else:
            msg = res_data.get("msg")
            self.printf(f"{tip}失败:\t{msg}")

    def reward(self):
        try:
            for i in range(self.MAX_HELP_NUM):
                self.home()
            self.printf(f"当前营业币:\t{self.canUseCoinAmount}")
        except:
            print_trace()

    def get_invite_code(self):
        try:
            # self.home()
            body = {
                "activeId": '63526d8f5fe613a6adb48f03',
                "isFirst": 1,
                "operType": 1
            }
            opt = {
                "h5st": True,
                "functionId": "makemoneyshop_home",
                "body": body,
                "params": {
                    "client": "jxh5",
                    "clientVersion": "1.2.5",
                    "appid": "jdlt_h5",
                    "g_ty": "h5",
                    "g_tk": "",
                    "appCode": "ms2362fc9e",
                    "source": "makemoneyshop",
                    "isSecurity": "true",
                    "bizCode": "makemoneyshop"
                },
                "searchParams": {
                    "functionId": "makemoneyshop_home",
                    "body": json.dumps(body, separators=(",", ":")),
                }
            }
            status, res_data = self.jd_api(self.opt(opt))
            if res_data.get('code') == 0:
                self.inviteCode = res_data['data']['shareId']
                self.canUseCoinAmount = float(res_data['data']['canUseCoinAmount'])
                self.printf(f"【助力码】:\t{self.inviteCode}")
            else:
                self.need_help = False
                self.black = True
        except:
            print_trace()

    def help(self, inviter):
        try:
            if inviter.help_num >= inviter.MAX_HELP_NUM:
                inviter.need_help = False
                printf(f"车头[{inviter.Name}]\t 助力已满({inviter.help_num}/{inviter.MAX_HELP_NUM})")
                return
            body = {
                "activeId": '63526d8f5fe613a6adb48f03',
                "shareId": inviter.inviteCode,
                "operType": 1
            }
            opt = {
                "functionId": "makemoneyshop_guesthelp",
                "body": body,
                'params': {
                    "loginType": 2,
                    "sceneval": 2
                },
                "searchParams": self.searchParams({
                    "functionId": "makemoneyshop_guesthelp",
                    "body": json.dumps(body, separators=(",", ":")),
                })
            }
            status, res_data = self.jd_api(self.opt(opt))
            code = str(res_data.get('code', status))
            if code == '1009':
                inviter.help_num += 1
                self.can_help = False
                printf(f"\t助力[{inviter.Name}]成功, 已邀请: {inviter.help_num}/{inviter.MAX_HELP_NUM}")
            else:
                msg = res_data.get("msg", "")
                if '未登录' in msg:
                    self.valid = False
                    self.can_help = False
                elif '限制' in msg or '火爆' in msg or '未登录' in msg:
                    self.can_help = False
                if msg == 'success':
                    inviter.help_num += 1
                    self.can_help = False
                    printf(f"\t助力[{inviter.Name}]成功, 已邀请: {inviter.help_num}/{inviter.MAX_HELP_NUM}")
                    return
                printf(f"\t助力失败[{code}]: {msg}")
        except:
            print_trace()


if __name__ == '__main__':
    task = TaskClass("help")
    task.MAX_HELP_NUM = 10
    task.name = 'DYJ_HELP'
    task.init_config(DyjUserClass)
    task.main("大赢家-助力")
