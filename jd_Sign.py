# coding=utf-8
'''
new Env('京东集合签到');
export RabbitToken="token值"

'''
import asyncio
import json
import re
from copy import deepcopy
from urllib.parse import quote, unquote

import requests

from utils.common import UserClass, print_trace, print_api_error, TaskClass, printf, get_code, get_error_msg


class SignUserClass(UserClass):
    def __init__(self, cookie):
        super(SignUserClass, self).__init__(cookie)
        self.appname = ""
        self.activity_id = ""
        self.Origin = "https://prodev.m.jd.com"
        self.referer = "https://prodev.m.jd.com/"
        self.sign_list = {
            '【医药馆】': {
                'activity_id': '2KMRByvMg6Z2nwDmQ1StFTtKJc81',
            },
            '【新年换新机】': {
                'activity_id': '2DWXWszt6VvNx4HDctSa4TA7rHh6',
            },
            '【花young】': {
                'activity_id': '2QUxWHx5BSCNtnBDjtt5gZTq7zdZ',
            },
            '【签到瓜分京豆】': {
                'activity_id': '3MFSkPGCDZrP2WPKBRZdiKm9AZ7D',
            },
            '【京东汽车福利中心】': {
                'activity_id': '2u1ZhLtcmRWeBPLf8mWqPRWwvXQV',
            },
            '【京东电器-签到有礼】': {
                'activity_id': '4SWjnZSCTHPYjE5T7j35rxxuMTb6',
            },
            '【男子服饰】': {
                'activity_id': '412SRRXnKE1Q4Y6uJRWVT6XhyseG',
            },
            '【美妆服饰】': {
                'activity_id': '4RBT3H9jmgYg1k2kBnHF8NAHm7m8',
            },
            '【吃喝玩乐】': {
                'activity_id': '3YDEucGmCvu1uNmyq4GHMMgwczjE',
            },
            '【京东图书】': {
                'activity_id': '3SC6rw5iBg66qrXPGmZMqFDwcyXi',
            },
            '【京东生活福利站】': {
                'activity_id': '3fJZ27dqd7iAffkm2QRwc1eZwbK6',
            },
            '【儿童关爱中心】': {
                'activity_id': '2YBtsNRHVGNq1dQJGVCrVPhoMrSv',
            },
            '【拍拍二手签到】': {
                'activity_id': '3S28janPLYmtFxypu37AYAGgivfp',
            },
            '【京东工业品】': {
                'activity_id': '3xj74a5WenijFqCMJJJ2d2qRdobK',
            },
            '【京东男装】': {
                'activity_id': '3h8AMpw8EB48d5c37dMjF1Rpf1Yk',
            },
        }

    async def opt(self, opt):
        await self.set_joyytoken()
        _opt = {
            "method": "post",
            "log": False,
            "api": "client.action",
            "body_param": {
                "appid": "babelh5",
                "sign": "11",
            }
        }
        _opt.update(opt)
        return _opt

    async def qryH5BabelFloors(self):
        opt = {
            'api': '',
            'functionId': 'qryH5BabelFloors',
            'params': {
                'clientVersion': '1.0.0',
                'client': 'wh5',
            },
            'body': {
                "activityId": self.activity_id,
                "paginationParam": "2",
            },
            "body_param": {}
        }
        encryptProjectId, encryptAssignmentId, styleId, moduleId, enc = '', '', '', '', ''
        status, result = await self.jd_api(await self.opt(opt))
        # print(json.dumps(result))
        for item in result['floorList']:
            if not item.get("boardParams"):
                continue
            if not item["boardParams"].get("interaction"):
                continue
            data = json.loads(item["boardParams"]['interaction'])
            styleId = item["styleId"]
            enc = item['enc']
            moduleId = item['moduleId']
            encryptProjectId = data['encryptProjectId']
            encryptAssignmentId = data['encryptAssignmentId']
            break
        else:
            opt['body'][
                "paginationFlrs"] = "[[88841615,88841616,88841617,88841618,90114069,88841619,88841620,88841621,88841629,88841622,88844366,88844367,89663355,88844370,89282848,89076898,88841639,88841642,88841683],[88892037,88841632,88841633,89663176,88841637,88841641,88841643,88841645,88841646,88841647,88841648,88841649,88841650,88841651,88841654,88841655,88841656,88841657,88841659,88841660,88841661,88841662,88841663,88841664,88841665,88841666]]"
            status, result = await self.jd_api(await self.opt(opt))
            for item in result['floorList']:
                if not item.get("boardParams"):
                    continue
                data = json.loads(item["boardParams"]['interaction'])
                styleId = item["styleId"]
                enc = item['enc']
                moduleId = item['moduleId']
                encryptProjectId = data['encryptProjectId']
                encryptAssignmentId = data['encryptAssignmentId']
                break
        return encryptProjectId, encryptAssignmentId, styleId, moduleId, enc

    def log_format(self, body, log_data):
        extParam = {
            "forceBot": 1,
            "businessData": {
                "random": log_data["random"]
            },
            "signStr": log_data["log"]
        }
        body.update({"extParam": extParam})
        body = {
            "body": json.dumps(body, separators=(',', ':'))
        }
        return body

    def html_home(self):
        url = f'https://pro.m.jd.com/mall/active/{self.activity_id}/index.html'
        headers = deepcopy(self.headers)
        headers['Content-Type'] = None
        res = requests.get(url, self.headers)
        pattern = re.findall(r"try\{window\.__ihubData__ *\=(.*?)\}catch\(e\)", res.text)
        if pattern:
            data = json.loads(pattern[0])
            for item in data.get("codeFloors", []):
                boardParams = item.get("boardParams", {})
                activityInfo = data.get("activityInfo", {})
                interaction = boardParams.get("interaction", {})
                if not interaction:
                    continue
                if not self.env.init_data:
                    self.env.init_data = {}
                interaction = json.loads(interaction)
                interaction.update({"title": unquote(activityInfo.get("title"))})
                self.env.init_data.update(
                    {
                        self.activity_id: interaction
                    }
                )
        # try:
        #     encryptProjectId = re.findall(r'encryptProjectId\\":\\"(.*?)\\"', res.text)[0]
        #     encryptAssignmentId = re.findall(r'encryptAssignmentId\\":\\"(.*?)\\"', res.text)[0]
        # except:
        #     print_trace()
        #     return '', '', '', '', ''
        # try:
        #     styleId = re.findall(r'styleId":"(.*?)"', res.text)[0]
        #     moduleId = re.findall(r'moduleId":(\d+)', res.text)[0]
        #     enc = re.findall(r'enc":"(.*?)"', res.text)[0]
        #     return encryptProjectId, encryptAssignmentId, styleId, moduleId, enc
        # except:
        #     return encryptProjectId, encryptAssignmentId, '00019605', '89737944', 'EE9D28C22E838CDEAB430A4B4CA444F515D98600E45377CAFE2BC6CF024A9D8B1AD6F70E5D536A03FFC12695CBF3FAE209572BBDD414E3DD4B346014069E0FC7'

    async def doInteractiveAssignment(self, data, task):
        try:
            # encryptProjectId, encryptAssignmentId, styleId, moduleId, enc = await self.qryH5BabelFloors()
            ext = task.get("ext", {})
            sign1 = ext.get("sign1", {})
            itemId = sign1.get("itemId", "1")
            body = {
                'sourceCode': 'acetttsign',
                'encryptProjectId': data['encryptProjectId'],
                'encryptAssignmentId': data['encryptAssignmentId'],
                'completionFlag': True,
                'itemId': itemId,
                'activity_id': self.activity_id,
                "template_id": "00019605",
                "floor_id": "80444954",
                "enc": ""
            }
            opt = {
                "functionId": "doInteractiveAssignment",
                "body": body,
                "log": True,
            }
            tips = data['title']
            status, result = await self.jd_api(await self.opt(opt))
            if result and result.get("code") == '0':
                if result.get('subCode') == '0':
                    if result['rewardsInfo'].get('failRewards'):
                        self.printf(f"{tips}\t签到成功，{result['rewardsInfo']['failRewards'][0]['msg']}")
                    elif result['rewardsInfo'].get('successRewards'):
                        if result['rewardsInfo']['successRewards'].get("3"):
                            self.printf(
                                f"{tips}\t签到成功，获得：{result['rewardsInfo']['successRewards']['3'][0]['quantity']} 京豆")
                        elif result['rewardsInfo']['successRewards'].get("10"):
                            data = result['rewardsInfo']['successRewards']['10'][0]
                            self.printf(f"{tips}\t签到成功，获得：{data['usageThreshold']} - {data['quota']} 优惠券")
                    else:
                        self.printf(result)
                else:
                    msg = result['msg']
                    if "火爆" in msg:
                        self.black = True
                    elif "环境异常" in msg:
                        self.black = True
                    self.printf(f"{tips}\t签到失败，{msg}")
            else:
                msg = result.get('msg', '')
                if '登陆失败' in msg:
                    self.valid = False
                    self.can_help = False
                    self.need_help = False
                if msg:
                    self.printf(msg)
                print_api_error(opt, status)
        except:
            print_trace()

    async def queryInteractiveInfo(self, data):
        try:
            body = {
                'sourceCode': 'acetttsign',
                'encryptProjectId': data['encryptProjectId'],
                'encryptAssigmentIds': [data['encryptAssignmentId']],
                "ext": {"rewardEncryptAssignmentId": data['encryptAssignmentId'],
                        "timesEncryptAssignmentId": data['encryptAssignmentId'], "needNum": 50}
            }
            opt = {
                "functionId": "queryInteractiveInfo",
                "body": body,
                "log": False,
            }
            status, result = await self.jd_api(await self.opt(opt))
            # code = get_code(result, status)
            code = result.get("code")
            error_msg = get_error_msg(result)
            if code == '0':
                subCode = result.get("subCode", -1)
                if subCode == '0':
                    for task in result.get("assignmentList"):
                        ext = task.get("ext", {})
                        extraType = ext.get("extraType", {})
                        if "sign" not in extraType:
                            continue
                        if task.get("completionFlag"):
                            self.printf(f"{data['title']}: 已签到")
                            continue
                        await self.doInteractiveAssignment(data, task)
                else:
                    self.printf(f"查询活动[{data['title']}]失败[{subCode}]: {error_msg}")
            else:
                self.printf(f"查询活动[{data['title']}]失败[{code}]: {error_msg}")
        except:
            print_trace()

    async def main(self):
        if not await self.is_login():
            self.printf("未登录")
            return
        for k, v in self.sign_list.items():
            activity_id = v['activity_id']
            self.appname = f"babel_{activity_id}"
            self.activity_id = v['activity_id']
            if not self.env.init_data or not self.env.init_data.get(self.activity_id):
                self.html_home()
            if not self.env.init_data or not self.env.init_data.get(self.activity_id):
                self.printf(f"{k}: 查询活动失败")
                continue
            await self.set_joyytoken()
            self.env.init_data[self.activity_id]['title'] = k
            await self.queryInteractiveInfo(self.env.init_data.get(self.activity_id))
        printf('')


if __name__ == '__main__':
    task = TaskClass("task")
    task.name = 'SIGN'
    task.init_config(SignUserClass)
    asyncio.run(task.main("集合签到"))
