"""
Author  : luxusheng
Time    : 2021/8/24 10:48 上午
version: python3
"""
import os
import json

import jenkins
import requests
import urllib3

from examples.trending import trend

'''
飞书推送方法：
读取report文件中"prometheusData.txt"，循环遍历获取需要的值。
使用飞书机器人的接口，拼接后推送text
'''


def LarkSend():
    result = trend()
    # 飞书推送
    url = "https://open.larksuite.com/open-apis/bot/v2/hook/6b980745-4c12-4e79-98eb-028e18836e6e"
    # url = 'https://open.larksuite.com/open-apis/bot/v2/hook/c7647be4-0d05-4448-9e49-4ea254ac0ac8'  # webhook
    if result == 30:
        con = {"msg_type": "text",
               "content": {
                   "text": "tiktok拉取feed结果"
                              "\n拉取feed成功:"
                              "\n应该拉取feed数量: 30" 
                              "\n实际拉取feed数量:" +str(result)

               }
               }
    else:
        con = {"msg_type": "text",
               "content": {
                   "text": "tiktok拉取feed失败"
                           "\n实际响应:" + result

               }
               }
    requests.packages.urllib3.disable_warnings()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    jd = json.dumps(con)
    # jd = bytes(jd, 'utf-8')
    # requests.post(url=url, data=jd, headers={'Content-Type': 'application/json'})
    requests.request("POST", url, headers={'Content-Type': 'application/json'}, data=jd)



if __name__ == '__main__':
    LarkSend()
