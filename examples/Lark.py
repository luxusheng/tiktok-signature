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



'''
飞书推送方法：
读取report文件中"prometheusData.txt"，循环遍历获取需要的值。
使用飞书机器人的接口，拼接后推送text
'''
import json
import random
import requests
import string
import os.path
from Naked.toolshed.shell import muterun_js

def trend():
    referer = "https://www.tiktok.com/"
    url = "https://m.tiktok.com/api/post/item_list/?aid=1988&count=30&secUid=MS4wLjABAAAAOUoQXeHglWcq4ca3MwlckxqAe-RIKQ1zlH9NkQkbLAT_h1_6SDc4zyPdAcVdTWZF&cursor=0"

    h = requests.head(
        url,
        headers={
            "x-secsdk-csrf-version": "1.2.5",
            "x-secsdk-csrf-request": "1"
        },
    )

    csrf_session_id = h.cookies["csrf_session_id"]
    csrf_token = h.headers["X-Ware-Csrf-Token"].split(",")[1]
    t = '/Users/build/.nvm/versions/node/v12.22.4/bin/npm i playwright-chromium'
    os.system(t)
    # response = muterun_js(' '.join([os.path.abspath('browser.js'), "\""+url+"\""]))
    a = '/Users/build/.nvm/versions/node/v12.22.4/bin/node /Users/build/.jenkins/jobs/tiktok_feed/workspace/testing/examples/browser.js "https://m.tiktok.com/api/post/item_list/?aid=1988&count=30&secUid=MS4wLjABAAAAOUoQXeHglWcq4ca3MwlckxqAe-RIKQ1zlH9NkQkbLAT_h1_6SDc4zyPdAcVdTWZF&cursor=0"'
    response = os.popen(a)
    text = response.read()
    text = json.loads(text)

    # the command was successful, handle the standard output
    try:
        # signature = json.loads(response.stdout)
        # print(signature)
        request = requests.get(text['data']['signed_url'], headers={"method": "GET",
                                                                         "accept-encoding": "gzip, deflate",
                                                                         "cookie": "tt_webid_v2=1234567890; csrf_session_id=" + csrf_session_id,
                                                                         "Referer": referer,
                                                                         "user-agent": text['data']['navigator']['user_agent'],
                                                                         "x-secsdk-csrf-token": csrf_token,
                                                                         "Connection": 'close'
                                                                         })

        data = request.text
        data = json.loads(data)
        print(len(data["itemList"]))
        return len(data["itemList"])
    except Exception as e:
        return e



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
