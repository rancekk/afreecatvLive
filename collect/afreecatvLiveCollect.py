from collect.requestsUtils import requestsUtils
import json
import requests
import cv2
import numpy as np
import logging
import time  # 引入time模块

logger = logging.getLogger('afreecatvLiveCollect')
import sys
import tensorflow as tf
import tf_pose as tp
import tf_pose.common as common


class afreecatvLiveCollect:
    request = requestsUtils()

    def getPlayLiveAPIData(self, bid, bno):
        dataMap = {
            'bid': bid,
            'bno': bno,
            'type': "aid",
            'player_type': "html5",
            'stream_type': "common",
            'quality': "hd",
            'mode': "landing",
        }
        body = self.request.post_main(url="http://live.afreecatv.com/afreeca/player_live_api.php?bjid=dmsco39",
                                      data=dataMap, method="post", header="form-data")
        body = json.loads(body)
        channel = body['CHANNEL']
        aid = channel['AID']
        return aid

    def getViewUrl(self, bno):
        body = self.request.get_main(
            url="http://resourcemanager.afreecatv.com:9090/broad_stream_assign.html?return_type=gcp_cdn&use_co"
                "rs=true&cors_origin_url=play.afreecatv.com&broad_key=" + bno + "-common-hd-hls",
            method="get", )
        body = json.loads(body)

        return body["view_url"]

    def getM3U8File(self, viewUrl, aid):
        body = self.request.get_main(
            url=viewUrl + "?aid=" + aid,
            method="get", )

        ts = body[body.rindex(",") + 3:].strip()
        return ts

    def downTS(self, url, fileName):
        f = requests.get(url=url, proxies=self.request.proxies)
        # 下载文件
        with open(fileName, "ab") as code:
            code.write(f.content)
        f.close()

    # 定义保存图片函数
    def save_image(self, image, name):
        cv2.imwrite(name, image)

    def getVideoCapture(self, file):
        videoCapture = cv2.VideoCapture(file)
        times = 0
        frameFrequency = 10  # 提取视频的频率，每50帧提取一个
        success = True
        list1 = []
        while True:
            times += 1
            res, image = videoCapture.read()
            if not res:
                print('not res , not image')
                break
            if times % frameFrequency == 0:
                self.save_image(image, './temp/' + str(times) + '.jpg')
                list1.append('./temp/' + str(times) + '.jpg')
        videoCapture.release()
        return list1

    def getHummans(self, imagePath, e):

        image = common.read_imgfile(imagePath, None, None)

        humans = e.inference(image, resize_to_default=(1 > 0 and 1 > 0), upsample_size=4.0)
        return humans

    def checkDance(self, humanList):
        hipList = []
        hipThreshold = 2  # 屁股阈值
        danceThreshold = 0.05  # 跳舞阈值
        hipLostCount = 0
        if (len(humanList) < 3):
            return False
        for human in humanList:
            hip = human.body_parts.get(8)
            if (hip is None):
                hipLostCount += 1
                if (hipLostCount >= hipThreshold):
                    return False
            else:
                hipList.append(hip)
            # 统计跳舞时屁股的总差值 预估阈值
        xABSList = 0
        yABSList = 0

        for i in range(1, len(hipList) - 1):
            # if (hipList[i + 1].x < hipList[i].x):
            #     xABSList += abs(hipList[i + 1].x - hipList[i].x)
            # else:
            #     xABSList += abs(hipList[i].x - hipList[i - 1].x)
            # if (hipList[i + 1].y < hipList[i].y):
            #     yABSList += abs(hipList[i + 1].y - hipList[i].y)
            # else:
            #     yABSList += abs(hipList[i].y - hipList[i - 1].y)
            xABSList += abs(hipList[i + 1].x - hipList[i].x)
            yABSList += abs(hipList[i + 1].y - hipList[i].y)
        if xABSList > danceThreshold or yABSList > danceThreshold:
            return True
        else:
            return False
    #检测直播间是否在跳舞 url 直播间地址
    def checkLiveRoomIsDancing(self, url, e):
        strList = str.split(url, "/")
        bid = strList[len(strList) - 2]
        bno = strList[len(strList) - 1]
        aid = self.getPlayLiveAPIData(bid, bno)
        viewUrl = self.getViewUrl(bno)
        file = "./temp/" + str(time.time()) + ".mp4"
        ts = self.getM3U8File(viewUrl, aid)
        self.downTS(viewUrl + ts, file)
        imagePathList = self.getVideoCapture(file)
        humanList = []
        for imagePath in imagePathList:
            humans = self.getHummans(imagePath, e)
            if (len(humans) > 0):
                human = humans[0]
                humanList.append(human)
        return self.checkDance(humanList)
