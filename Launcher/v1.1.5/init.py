

import os
from json import loads
from shutil import rmtree
from urllib.request import urlopen
from urllib.error import URLError
import tools
from wget import download
try:
    Updateurl = urlopen(
            r'https://gitee.com/Morbid-zj/yuanShenEx/raw/master/res/Update.json')
    UpdateConfig = loads(Updateurl.read())
except URLError or AttributeError:
    pass
config = {'Path': {'gamePath': tools.GetPath.GetYuanShen()}, 'Account': {'BFu': [{'name': '默认', 'path': ''}], 'GuanFu': [
    {'name': '默认', 'path': ''}]}, 'Plugins': {'刻师傅工具箱': {'downlorad': '', 'path': ''}, '空莹酒馆原神地图': {'downlorad': '', 'path': ''}}, 'Setting': {'run': 1}}

if os.path.exists("./src/Update.json"):
    CheckList = tools.FileOperation.FileToJson("./src/Update.json")


class CheckRes:

    def initdir():
        '''
        description: 初始化文档
        '''
        if not os.path.exists("./src"):
            os.makedirs("./src")

    def checkUpdate():
        '''
        description: 检查更新
        return {True}
        '''
        if os.path.exists("./src/Update.json"):
            if CheckList["version"] != UpdateConfig["version"]:
                rmtree("./src")
                os.makedirs("./src")
                tools.FileOperation.JsonToFile("./src/Update.json" , UpdateConfig)
                return True
            else:
                return True
        else:
            tools.FileOperation.JsonToFile("./src/Update.json" , UpdateConfig)
        return True


    def DownloadFile():
        '''
        description: 下载文件
        return {失败时返回:False}
        '''
        # try:
        CheckList = tools.FileOperation.FileToJson("./src/Update.json")
        for file in CheckList:
            if file == "version":
                pass
            elif not os.path.exists(CheckList[file][0]):
                download(CheckList[file][1] ,CheckList[file][0] )
                print(
                    f"{file}下载成功，地址是{CheckList[file][1]},存放在{CheckList[file][0]}")
        # except:
        #     return False


    def CheckConfig():
        if os.path.exists("./YuanShen.json"):
            pass

class Update:

    def NetworkStut(url):
        """检测是否联网
        Args:
            url (str): 网页链接

        Returns:
            bool: 成功返回True,失败返回False
        """
        res = os.system(f"ping {url} -n 1")
        if res == 0 and CheckRes:
            return True
        else:
            NetWorkfailed = tools.Toast("警告" , "联网失败")
            NetWorkfailed.start()
            return False



def main():
    CheckRes.initdir()
    if Update.NetworkStut("gitee.com"):
        CheckRes.checkUpdate()
    CheckRes.DownloadFile()


    

