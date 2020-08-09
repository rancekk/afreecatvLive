# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# 定时采集主播直播片段 通过采集视频帧判断主播是否已经开始跳舞
# 鼻子= 0
# 脖子= 1
# R肩= 2
# R肘= 3
# R手腕= 4
# L肩= 5
# L肘= 6
# L手腕= 7
# 臀围= 8
# R膝盖= 9
# R脚踝= 10
# 臀围= 11
# L膝盖= 12
# L脚踝= 13
# R眼= 14
# L眼= 15
# R耳= 16
# L耳朵= 17
# 背景= 18
from collect.afreecatvLiveCollect import afreecatvLiveCollect
import time  # 引入time模块
import logging

from collect.BJ import BJ
from threading import Timer
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

logger = logging.getLogger('TfPoseEstimatorRun')


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def start():
    bj1 = BJ()
    bj1.bid = "gusdk2362"
    bj1.bno = "225995131"

    bj2 = BJ()
    bj2.bid = "sbde5447"
    bj2.bno = "225997362"

    list1 = [bj1, bj2]
    af = afreecatvLiveCollect()

    e = initTS()
    url = "http://play.afreecatv.com/dmsco39/225998901"
    print(af.checkLiveRoomIsDancing(url, e) == 1)
    # print(af.getHummans(imagePath, e))
    # print("\r\n")
    # for bj in list1:
    #     aid = af.getPlayLiveAPIData(bj.bid, bj.bno)
    #     viewUrl = af.getViewUrl(bj.bno)
    #     file = "C:\\Users\\25082\\Downloads\\afreecaLive2\\" + str(time.time()) + ".mp4"
    #     t = Timer(2, task, args=(viewUrl, aid, file, af))
    #     # 2秒后启动线程
    #     t.start()


def task(viewUrl, aid, file, af):
    ts = af.getM3U8File(viewUrl, aid)
    af.downTS(viewUrl + ts, file)
    t = Timer(2, task, args=(viewUrl, aid, file, af))
    # 2秒后启动线程
    t.start()


def initTS():
    w, h = model_wh("432x368")
    if w == 0 or h == 0:
        e = TfPoseEstimator(get_graph_path("mobilenet_thin"), target_size=(432, 368))
    else:
        e = TfPoseEstimator(get_graph_path("mobilenet_thin"), target_size=(w, h))
    return e


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # start()
    af = afreecatvLiveCollect()

    e = initTS()
    url = "http://play.afreecatv.com/wpejrve/225974428"
    print(af.checkLiveRoomIsDancing(url, e))
    print_hi('123')
    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
